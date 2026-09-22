---
name: infer-body-weight-trend
description: Log real weigh-ins and conditions, run the portable condition-aware weight model, and separate raw measurements, reference estimates, scale trends, and explicitly justified prior-informed results.
---

# Infer body weight trend

Follow [Personal training coach](../personal-training-coach/SKILL.md). Weight tracking is optional. Read the chosen goal, relevant observations, adopted nutrition expectations only when applicable, and the [model guide](references/model.md) before calculating or interpreting model output.

## Log the observation

Preserve every genuine reading with its date, exact weight/unit, time or relation to waking, clothing, intake, bathroom, and reported hydration/heat context. Unknown conditions remain unknown. Never require ideal measurements or subtract food, fluid, clothing, or bathroom mass as an exact correction. Correct a transcription mistake in place; retain separate actual readings.

Use the structured Bodyweight table in the notebook or dated `logs/health/` file, following the [analytics guide](../../docs/ANALYTICS.md). Narrow condition labels must be supported by the user's words. Do not translate “probably” or “not dehydrated” into confirmed dehydration. Ask a short follow-up only when it materially improves interpretation; do not block logging an imperfect observation.

## Run the model when available

With file and Python access, run `python scripts/analyze_weight_history.py --workspace personal --unit kg --window-days 21 --format json`, substituting the user's chosen unit. In notebook mode use `--notebook MY-TRAINER.md`. The packaged tools can run in a supported app sandbox; the user need not install Python on their own device for such a session. Do not claim execution without a real successful tool result.

Inspect the extracted rows, raw units, conditions, date window, and model settings before trusting output. Report parsing gaps or conflicting units instead of discarding them silently. Multiple observations are aggregated by date in each model draw; one busy measurement day is not several independent days. The model retains nonstandard observations with uncertain condition offsets rather than deleting them.

An optional prior-informed run requires both `--expected-weekly-change` and `--expected-weekly-sd` in the selected output unit plus `--prior-basis`. Use only an adopted expectation supported by actual adherence; neither a calorie target nor an unlogged evening proves adherence. Retain scale-only results beside the optional prior-informed result. No automatic calorie-deficit-to-tissue conversion is supplied.

## Report four distinct quantities

1. Literal latest measured readings and conditions.
2. Latest reference-condition estimate and its uncertainty.
3. Scale-only current level with 68%, 90%, and 95% model intervals.
4. Weekly change and model probability of decrease, with date coverage and uncertainty.

Show a prior-informed result only if actually run with justified inputs. Label intervals as model-based uncertainty, not validated clinical confidence. Explain the main assumptions and actual unknown conditions driving uncertainty. No result isolates fat, lean tissue, or hydration. Sparse data, unusual conditions, and a poor linear fit can limit interpretation.

If execution is unavailable, keep the raw observations and optionally provide a transparent descriptive average over comparable days. Name the dates, units, selection rule, and distinct-day count. Preserve noncomparable observations as context. Do not invent model intervals or a probability, and do not present this fallback as equivalent to the full analysis.

Save raw records and source-linked derived findings in their separate sections. Never change targets or training merely because the scale moved; follow the user's chosen adjustment rules and core safety boundary.
