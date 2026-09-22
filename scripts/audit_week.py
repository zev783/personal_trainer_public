"""Read-only weekly evidence audit and workload accounting for folder or notebook records."""

import argparse
from datetime import date, timedelta
import json
import statistics
import sys

if __package__:
    from .records import selected_sources, tables, row_date, input_arguments, number, frontmatter, escape
    from .analyze_weight_history import observations_from, conditions
else:
    from records import selected_sources, tables, row_date, input_arguments, number, frontmatter, escape
    from analyze_weight_history import observations_from, conditions

ACTUAL = {"completed", "partial"}
CLOSED = {"complete", "completed", "closed", "final"}


def workload_row(row):
    status = row.get("status", "unknown").lower()
    category = row.get("category", "unknown").lower()
    required = row.get("required", "unknown").lower()
    if status not in ACTUAL | {"planned", "skipped", "unknown"}:
        raise ValueError(f"Invalid workload status at {row['_source']}")
    if category not in {"conditioning", "strength", "other", "unknown"}:
        raise ValueError(f"Invalid category at {row['_source']}")
    if required not in {"yes", "no", "conditional", "unknown"}:
        raise ValueError(f"Invalid required/optional flag at {row['_source']}")
    fields = {name: number(row.get(name, ""), name) for name in (
        "active_min", "min_low", "min_high", "distance_km", "race_specific_min", "elapsed_min")}
    active, low, high = fields["active_min"], fields["min_low"], fields["min_high"]
    if (low is None) != (high is None):
        raise ValueError(f"Supply both range endpoints at {row['_source']}")
    if low is not None and (active is None or not low <= active <= high):
        raise ValueError(f"Workload central value must fall within its range at {row['_source']}")
    evidence = row.get("evidence", "unknown").lower()
    if evidence not in {"measured", "reported", "inferred", "projected", "unknown"}:
        raise ValueError(f"Invalid evidence type at {row['_source']}")
    if status in ACTUAL and evidence == "projected":
        raise ValueError("Projected work cannot be counted as completed")
    if evidence == "inferred" and not row.get("assumptions", "").strip():
        raise ValueError("Inferred workload needs its assumptions")
    zones = {f"z{i}": number(row.get(f"z{i}", ""), f"z{i}") for i in range(1, 6)}
    classified = sum(value for value in zones.values() if value is not None)
    if classified and (category != "conditioning" or active is None or classified > active + 1e-6):
        raise ValueError(f"Zone minutes exceed or do not belong to conditioning activity at {row['_source']}")
    if fields["race_specific_min"] is not None and (active is None or fields["race_specific_min"] > active):
        raise ValueError("Race-specific minutes are an overlapping subset of active minutes")
    explicit_unknown = number(row.get("unclassified_min", ""), "unclassified_min")
    unclassified = active-classified if category == "conditioning" and active is not None else None
    if explicit_unknown is not None and (unclassified is None or abs(explicit_unknown-unclassified) > 1e-6):
        raise ValueError("Zone plus unclassified minutes must equal active conditioning minutes")
    if active is not None and fields["elapsed_min"] is not None and active > fields["elapsed_min"]:
        raise ValueError("Active minutes cannot exceed the elapsed time of the same non-overlapping segment")
    identifier = row.get("id", "").strip()
    if not identifier:
        raise ValueError("Each workload segment needs a unique ID")
    return {"date": row_date(row).isoformat(), "id": identifier, "status": status,
            "plan_status": row.get("plan_status", "unknown").lower(),
            "plan_version": row.get("plan_version", "unknown"),
            "category": category, "required": required, "modality": row.get("modality", "unknown"),
            "evidence": evidence, "assumptions": row.get("assumptions", ""),
            "zones": zones, "unclassified_min": unclassified, "source": row["_source"], **fields}


def workload_summary(rows):
    def subtotal(name, selected):
        values = [row[name] for row in selected if row[name] is not None]
        return {"known_total": sum(values) if values else None,
                "covered_segments": len(values), "total_segments": len(selected)}
    result = {"segments": len(rows), "active_minutes": subtotal("active_min", rows),
              "distance_km": subtotal("distance_km", rows), "by_category": {}, "by_evidence": {},
              "by_modality": {}}
    for output_key, field in (("by_category", "category"), ("by_evidence", "evidence"), ("by_modality", "modality")):
        for value in sorted({row[field] for row in rows}):
            result[output_key][value] = subtotal("active_min", [row for row in rows if row[field] == value])
    conditioning = [row for row in rows if row["category"] == "conditioning"]
    result["conditioning_zones"] = {f"z{i}": sum(row["zones"][f"z{i}"] or 0 for row in conditioning) for i in range(1, 6)}
    result["conditioning_unclassified_min"] = sum(row["unclassified_min"] or 0 for row in conditioning)
    result["conditioning_segments_missing_active_time"] = sum(row["active_min"] is None for row in conditioning)
    result["race_specific_minutes_subset"] = subtotal("race_specific_min", rows)
    result["range"] = {"low_known": sum(row["min_low"] for row in rows if row["min_low"] is not None),
                       "high_known": sum(row["min_high"] for row in rows if row["min_high"] is not None),
                       "segments_with_range": sum(row["min_low"] is not None for row in rows)}
    return result


def audit(sources, start, as_of):
    end = start + timedelta(days=6)
    rows, nutrition, file_workouts, gaps = [], [], [], []
    coverage = { (start + timedelta(days=i)).isoformat(): set() for i in range(7)}
    seen_ids, seen_days = set(), set()
    for source in sources:
        if source.day and start <= source.day <= end:
            coverage[source.day.isoformat()].add(source.domain)
            if source.domain == "workouts":
                meta = frontmatter(source.text)
                file_workouts.append({"date": source.day.isoformat(), "source": source.name,
                    "status": meta.get("session_status", "unknown"),
                    "reported_elapsed_minutes": meta.get("duration_minutes", "unknown")})
            for line in source.text.splitlines():
                if any(token in line.lower() for token in ("pending", "unresolved", "not reported")):
                    gaps.append({"source": source.name, "text": line.strip()})
        for row in tables(source):
            kind = "workout" if "active_min" in row and "id" in row else "nutrition" if "calories" in row and "status" in row else None
            if not kind:
                continue
            day = row_date(row)
            if not start <= day <= end or (kind == "nutrition" and day > as_of):
                continue
            if kind == "workout":
                item = workload_row(row)
                if item["id"] in seen_ids:
                    raise ValueError(f"Duplicate workload ID {item['id']}; reconcile overlapping records first")
                seen_ids.add(item["id"])
                if day > as_of and item["status"] in ACTUAL:
                    raise ValueError("A future-dated segment cannot already be completed at the requested as-of date")
                rows.append(item)
                if item["status"] in ACTUAL:
                    coverage[day.isoformat()].add("workouts")
            else:
                if day in seen_days:
                    raise ValueError(f"Multiple nutrition daily totals for {day}; reconcile before averaging")
                seen_days.add(day)
                item = {"date": day.isoformat(), "status": row["status"].lower(),
                    "basis": row.get("basis", "unknown"), "source": row["_source"],
                    "target_version": row.get("target_version", "unknown")}
                item.update({name: number(row.get(name, ""), name) for name in
                             ("calories", "protein_g", "carbohydrate_g", "fat_g", "target_calories")})
                item["difference_calories"] = item["calories"]-item["target_calories"] if item["calories"] is not None and item["target_calories"] is not None else None
                nutrition.append(item)
                coverage[day.isoformat()].add("nutrition")
    actual = [row for row in rows if row["status"] in ACTUAL]
    def active_plan(row):
        return row["plan_status"] == "adopted" and row["plan_version"].strip().lower() not in {
            "", "unknown", "not set", "none", "not provided"}
    required = [row for row in rows if row["status"] == "planned" and row["required"] == "yes"
                and date.fromisoformat(row["date"]) >= as_of and active_plan(row)]
    optional = [row for row in rows if row["status"] == "planned" and row["required"] in {"no", "conditional"}
                and date.fromisoformat(row["date"]) >= as_of and active_plan(row)]
    unresolved = [row for row in rows if row["status"] == "unknown" or
                  (row["status"] == "planned" and (row["required"] == "unknown" or date.fromisoformat(row["date"]) < as_of or not active_plan(row)))]
    averages = {}
    for nutrient in ("calories", "protein_g", "carbohydrate_g", "fat_g"):
        eligible = [item[nutrient] for item in nutrition if item["status"] in CLOSED and item[nutrient] is not None]
        averages[nutrient] = {"mean": statistics.mean(eligible) if eligible else None, "days": len(eligible)}
    weights = [item for item in observations_from(sources) if start <= item.day <= min(end, as_of)]
    comparable = {}
    for item in weights:
        coverage[item.day.isoformat()].add("health")
        flags = conditions(item)
        waking = any(token in item.time.lower() for token in ("waking", "morning"))
        if waking and flags["pre_intake"] and flags["post_urination"] and flags["clothing"] in {"none", "light"} and not flags["dehydration_reported"]:
            comparable.setdefault(item.day.isoformat(), []).append(item.kg)
    daily_weights = {day: statistics.mean(values) for day, values in comparable.items()}
    return {"week_start": start.isoformat(), "week_end": end.isoformat(), "as_of": as_of.isoformat(),
        "period_status": "future" if as_of < start else "in-progress" if as_of <= end else "elapsed; record closure not assumed",
        "coverage": [{"date": day, "domains": sorted(domains), "missing_is_not_zero": True} for day, domains in coverage.items()],
        "source_files": [source.name for source in sources if source.day is None or start <= source.day <= end],
        "workout_file_statuses": file_workouts, "workload_rows": rows,
        "completed_workload": workload_summary(actual),
        "remaining_required": workload_summary(required),
        "projected_required_baseline": workload_summary(actual + required),
        "optional_or_conditional_segments": optional,
        "unresolved_segments": unresolved,
        "nutrition": {"days": nutrition, "averages_complete_days_only": averages},
        "comparable_weights": {"daily_means_kg": daily_weights, "days": len(daily_weights),
            "mean_kg": statistics.mean(daily_weights.values()) if daily_weights else None,
            "contextual_readings": len(weights)-sum(len(values) for values in comparable.values())},
        "open_items": gaps[:30], "open_items_total": len(gaps),
        "limitations": ["Structured summaries require the documented tables; narrative-only files show coverage, not inferred numerical totals.",
            "No full-session adherence percentage is inferred from workload segments.",
            "Optional segments are separate alternatives, not automatically additive.",
            "Research, plan adoption, and actual completion remain separate. No files were changed."]}


def markdown(result):
    lines = [f"# Weekly audit: {result['week_start']} through {result['week_end']}",
             f"Status: {result['period_status']}", "## Record coverage", "| Date | Available records |", "|---|---|"]
    lines.extend(f"| {row['date']} | {', '.join(row['domains']) or 'not reported'} |" for row in result["coverage"])
    lines += ["## Workload", "| Segment | Status | Active min | Basis | Source |", "|---|---|---|---|---|"]
    lines.extend(f"| {escape(row['id'])} | {row['status']} | {row['active_min']} | {row['evidence']} | {escape(row['source'])} |"
                 for row in result["workload_rows"])
    for field in ("completed_workload", "remaining_required", "projected_required_baseline", "optional_or_conditional_segments",
                  "unresolved_segments", "nutrition", "comparable_weights", "open_items"):
        lines.append("## " + field.replace("_", " ").title())
        lines.append("```json\n" + json.dumps(result[field], indent=2, allow_nan=False) + "\n```")
    lines.extend("- " + line for line in result["limitations"])
    return "\n\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    input_arguments(parser)
    parser.add_argument("--week-start", type=date.fromisoformat, required=True,
                        help="First date of the user's chosen seven-day period; not limited to Monday")
    parser.add_argument("--as-of", type=date.fromisoformat, required=True, help="User's local date")
    args = parser.parse_args()
    try:
        result = audit(selected_sources(args.workspace, args.notebook), args.week_start, args.as_of)
    except (OSError, ValueError) as error:
        print(f"Weekly audit stopped: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, allow_nan=False) if args.format == "json" else markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
