"""Read-only condition-aware weight analysis, with explicit heuristic uncertainty."""

import argparse
from dataclasses import dataclass
from datetime import date, timedelta
import json
import math
import random
import re
import statistics
import sys

if __package__:
    from .records import selected_sources, tables, row_date, input_arguments, escape
else:
    from records import selected_sources, tables, row_date, input_arguments, escape

KG_PER_LB = 0.45359237
WEIGHT = re.compile(r"^(\d+(?:\.\d+)?)\s*(kg|kgs|kilograms?|lb|lbs|pounds?)?$", re.I)


@dataclass(frozen=True)
class Observation:
    day: date
    kg: float
    reported: str
    time: str
    clothing: str
    intake: str
    bathroom: str
    notes: str
    source: str


def observations_from(sources):
    result = []
    for source in sources:
        for row in tables(source):
            if "weight" not in row or not ("time_context" in row or source.domain == "health"
                    or any(word in row["_heading"].lower() for word in ("bodyweight", "weigh-in"))):
                continue
            raw = row["weight"].strip()
            if raw.lower() in ("", "unknown", "not reported", "not provided"):
                continue
            match = WEIGHT.fullmatch(raw)
            if not match:
                raise ValueError(f"Invalid weight at {row['_source']}")
            unit = (match[2] or row.get("unit", "")).lower()
            if unit not in ("kg", "kgs", "kilogram", "kilograms", "lb", "lbs", "pound", "pounds"):
                raise ValueError(f"Explicit lb or kg required at {row['_source']}")
            if match[2] and row.get("unit"):
                first_kg = match[2].lower().startswith("k")
                second_kg = row["unit"].lower().startswith("k")
                if first_kg != second_kg:
                    raise ValueError(f"Conflicting weight units at {row['_source']}")
            kg = float(match[1]) * (1 if unit.startswith("k") else KG_PER_LB)
            if not math.isfinite(kg) or kg <= 0:
                raise ValueError(f"Invalid weight at {row['_source']}")
            result.append(Observation(row_date(row), kg, f"{match[1]} {unit}",
                row.get("time_context", "unknown"), row.get("clothing", "unknown"),
                row.get("intake", row.get("food_fluid_status", "unknown")),
                row.get("bathroom", row.get("bathroom_status", "unknown")),
                row.get("notes", ""), row["_source"]))
    return result


def conditions(item):
    """Conservative explicit matches; unknowns remain uncertain, not inferred as ideal."""
    intake = item.intake.lower()
    pre = any(term in intake for term in ("pre-intake", "before food and fluid", "before food or water",
                                         "before any food or water", "fasted, no fluids"))
    if "after" in intake or "not fasted" in intake:
        pre = False
    clothing = item.clothing.lower()
    if clothing in ("nude", "naked", "none", "no clothing"):
        clothes = "none"
    elif clothing in ("underwear", "underwear only"):
        clothes = "light"
    elif any(term in clothing for term in ("shirt", "shorts", "gym clothes", "pants")):
        clothes = "clothed"
    else:
        clothes = "unknown"
    bathroom = item.bathroom.lower()
    emptied = any(term in bathroom for term in ("after urination", "post-urination", "after morning urination"))
    if "not " in bathroom or "before " in bathroom:
        emptied = False
    # Never interpret negated or uncertain dehydration text as a diagnosis.
    notes = item.notes.lower()
    dehydration = "dehydrated" in notes and not any(term in notes for term in ("not dehydrated", "no dehydration", "possibly", "unsure", "?"))
    water = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*(ml|l|us fl oz)\s+water\s*", intake)
    water_kg = None
    if water:
        water_kg = float(water[1]) * {"ml": 0.001, "l": 1, "us fl oz": 0.0295735295625}[water[2]]
    return {"pre_intake": pre, "clothing": clothes, "post_urination": emptied,
            "dehydration_reported": dehydration, "water_kg": water_kg}


def sample_offset(item, rng):
    """Generic operational priors in kg; no individual calibration is presumed."""
    flags = conditions(item)
    clothing = {"none": (0, 0, 0), "light": (0, .04, .10),
                "clothed": (.20, .40, .90), "unknown": (0, .30, 1.20)}[flags["clothing"]]
    offset = rng.triangular(clothing[0], clothing[2], clothing[1])
    if flags["water_kg"] is not None:
        offset += flags["water_kg"] * rng.betavariate(2, 1.3)
    elif not flags["pre_intake"]:
        # Broader unknown-intake prior replaces assumptions about a particular breakfast.
        offset += rng.triangular(0, 1.8, .45)
    if not flags["post_urination"]:
        offset += .45 * rng.betavariate(1.5, 3)
    if flags["dehydration_reported"]:
        offset -= rng.triangular(.10, 1.0, .35)
    return offset + rng.gauss(0, .05)


def regression(daily, rng, day_sd, prior_change=0, prior_sd=1.2):
    """Gaussian linear regression; one mean per date, centered on latest date."""
    last = max(daily)
    xs = [(day - last).days for day in sorted(daily)]
    ys = [statistics.mean(daily[day]) for day in sorted(daily)]
    center = statistics.mean(ys)
    ys = [y - center for y in ys]
    variance = day_sd ** 2
    a = len(xs) / variance + 1 / 10000
    b = sum(xs) / variance
    c = sum(x*x for x in xs) / variance + 1 / (prior_sd / 7) ** 2
    q0 = sum(ys) / variance
    q1 = sum(x*y for x, y in zip(xs, ys)) / variance + (prior_change / 7) / (prior_sd / 7) ** 2
    determinant = a*c - b*b
    v00, v01, v11 = c/determinant, -b/determinant, a/determinant
    mean0, mean1 = v00*q0 + v01*q1, v01*q0 + v11*q1
    z0, z1 = rng.gauss(0, 1), rng.gauss(0, 1)
    l00 = math.sqrt(v00)
    l10 = v01 / l00
    return (center + mean0 + l00*z0,
            7 * (mean1 + l10*z0 + math.sqrt(max(v11-l10*l10, 0))*z1))


def summarize(values, factor=1):
    ordered = sorted(value * factor for value in values)
    def q(p):
        position = (len(ordered)-1)*p
        low, high = math.floor(position), math.ceil(position)
        return ordered[low] + (ordered[high]-ordered[low]) * (position-low)
    return {"median": q(.5), "interval_68": [q(.16), q(.84)],
            "interval_90": [q(.05), q(.95)], "interval_95": [q(.025), q(.975)]}


def analyze(observations, *, unit="kg", draws=5000, seed=0, day_sd_kg=.5,
            expected_change=None, expected_sd=None, prior_basis=None):
    if unit not in ("kg", "lb") or not 1000 <= draws <= 50000:
        raise ValueError("Use kg or lb and 1000 through 50000 draws")
    if not math.isfinite(day_sd_kg) or day_sd_kg <= 0:
        raise ValueError("day_sd_kg must be finite and positive")
    if (expected_change is None) != (expected_sd is None):
        raise ValueError("Both expected weekly change and its uncertainty are required")
    if expected_change is not None and (not prior_basis or not math.isfinite(expected_change)
                                       or not math.isfinite(expected_sd) or expected_sd <= 0):
        raise ValueError("A finite prior, positive uncertainty, and explicit prior basis are required")
    if not observations or len({item.day for item in observations}) < 2:
        raise ValueError("At least two distinct observation dates are required; no trend was computed")
    rng = random.Random(seed)
    prior_rng = random.Random(seed + 1)
    factor = 1 if unit == "kg" else 1 / KG_PER_LB
    last = max(item.day for item in observations)
    per_row = [[] for _ in observations]
    latest, levels, changes, informed_levels, informed_changes = [], [], [], [], []
    for _ in range(draws):
        daily = {}
        for i, item in enumerate(observations):
            corrected = item.kg - sample_offset(item, rng)
            per_row[i].append(corrected)
            daily.setdefault(item.day, []).append(corrected)
        latest.append(statistics.mean(daily[last]))
        level, change = regression(daily, rng, day_sd_kg)
        levels.append(level)
        changes.append(change)
        if expected_change is not None:
            # Prior arguments use the selected output unit, not a hidden lb assumption.
            level, change = regression(daily, prior_rng, day_sd_kg,
                                       expected_change/factor, expected_sd/factor)
            informed_levels.append(level)
            informed_changes.append(change)
    def trend(level, change):
        return {"current_level": summarize(level, factor), "weekly_change": summarize(change, factor),
                "probability_decrease": sum(value < 0 for value in change) / len(change)}
    result = {"unit": unit, "as_of": last.isoformat(),
        "window_start": min(item.day for item in observations).isoformat(),
        "day_count": len({item.day for item in observations}), "observation_count": len(observations),
        "latest_measured": [item.reported for item in observations if item.day == last],
        "latest_reference_condition": summarize(latest, factor),
        "scale_only": trend(levels, changes),
        "settings": {"draws": draws, "seed": seed, "day_sd_kg": day_sd_kg,
                     "scale_slope_prior_kg_per_week": {"mean": 0, "sd": 1.2}},
        "observations": [{"date": item.day.isoformat(), "measured": item.reported,
            "conditions": conditions(item), "time_context": item.time, "clothing": item.clothing,
            "intake": item.intake, "bathroom": item.bathroom, "notes": item.notes,
            "reference_condition": summarize(values, factor), "source": item.source}
            for item, values in zip(observations, per_row)],
        "limitations": ["Heuristic model uncertainty, not validated clinical confidence intervals.",
                         "This cannot isolate fat, lean tissue, glycogen, or hydration.",
                         "A linear window and generic condition priors may not fit this person."]}
    if result["day_count"] < 7:
        result["limitations"].append("Fewer than seven observed days; weekly slope is especially uncertain.")
    if informed_levels:
        result["prior_informed"] = {**trend(informed_levels, informed_changes),
             "expected_weekly_change": expected_change, "expected_weekly_sd": expected_sd,
             "basis": prior_basis, "label": "User-supplied prior; not a measured tissue-loss result"}
    return result


def markdown(result):
    lines = [f"# Condition-aware weight analysis: {result['as_of']}",
        f"Units: {result['unit']}; {result['observation_count']} readings across {result['day_count']} dates.",
        f"Latest measured: {', '.join(result['latest_measured'])}",
        "| Date | Measured | Reference estimate | 90% model interval | Source |",
        "|---|---|---|---|---|"]
    for row in result["observations"]:
        summary = row["reference_condition"]
        lines.append(f"| {row['date']} | {row['measured']} | {summary['median']:.2f} | "
                     f"{summary['interval_90'][0]:.2f} to {summary['interval_90'][1]:.2f} | {escape(row['source'])} |")
    for label, summary in (("Latest reference condition", result["latest_reference_condition"]),
                           ("Scale-only level", result["scale_only"]["current_level"]),
                           ("Scale-only weekly change", result["scale_only"]["weekly_change"])):
        lines.append(f"- {label}: {summary['median']:.2f}; 68% {summary['interval_68']}; "
                     f"90% {summary['interval_90']}; 95% {summary['interval_95']}.")
    lines.append(f"- Scale-only probability of decrease: {result['scale_only']['probability_decrease']:.1%}.")
    if "prior_informed" in result:
        lines.append("## Prior-informed result\n\n" + json.dumps(result["prior_informed"], indent=2))
    lines.extend(["## Assumptions and limitations", json.dumps(result["settings"], indent=2)])
    lines.extend("- " + value for value in result["limitations"])
    lines.append("Inspect conditions and per-reading results with --format json before interpreting unusual readings.")
    return "\n\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    input_arguments(parser)
    parser.add_argument("--as-of", type=date.fromisoformat)
    parser.add_argument("--window-days", type=int, default=21)
    parser.add_argument("--unit", choices=("kg", "lb"), default="kg")
    parser.add_argument("--draws", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--day-sd-kg", type=float, default=.5)
    parser.add_argument("--expected-weekly-change", type=float)
    parser.add_argument("--expected-weekly-sd", type=float)
    parser.add_argument("--prior-basis")
    args = parser.parse_args()
    try:
        if args.window_days < 2:
            raise ValueError("window-days must be at least two")
        items = observations_from(selected_sources(args.workspace, args.notebook))
        end = args.as_of or max((item.day for item in items), default=date.today())
        start = end - timedelta(days=args.window_days-1)
        items = [item for item in items if start <= item.day <= end]
        result = analyze(items, unit=args.unit, draws=args.draws, seed=args.seed,
            day_sd_kg=args.day_sd_kg, expected_change=args.expected_weekly_change,
            expected_sd=args.expected_weekly_sd, prior_basis=args.prior_basis)
        result["requested_as_of"] = end.isoformat()
    except (OSError, ValueError) as error:
        print(f"Weight analysis stopped: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, allow_nan=False) if args.format == "json" else markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
