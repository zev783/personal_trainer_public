---
name: review-personal-training-week
description: Review a dated week of actual training, optional nutrition, and recovery, identify evidence gaps, and prepare next-week proposals without silently changing an adopted plan.
---

# Review personal training week

Follow [Personal training coach](../personal-training-coach/SKILL.md). Resolve the requested date range in the user's timezone and preferred week convention. With no dates supplied, use the latest completed week. Label a current week `in-progress`.

Read the applicable adopted plan versions and dated logs, relevant profile constraints, food facts for nutrient calculations, available comparable weight observations, and open recovery issues. If a notebook archive is not attached, explicitly exclude it from the review. Do not imply coverage of unseen records.

## Reconcile before interpreting

With a Python runtime and accessible records, run `python scripts/audit_week.py --workspace personal --week-start YYYY-MM-DD --as-of YYYY-MM-DD --format json`, substituting the actual chosen dates. In notebook mode use `--notebook MY-TRAINER.md` instead of `--workspace`. The [analytics guide](../../docs/ANALYTICS.md) covers the portable tools, supported tables, and coverage limits. Inspect every source behind the totals. The audit is read-only and does not replace source interpretation. If it cannot run, disclose that and do transparent arithmetic only; do not claim an automated audit occurred.

- **Coverage:** show which dates have usable records, partial entries, or no reports. Missing evidence is not a failed workout or zero food intake.
- **Plan versus actual:** distinguish required, optional, completed, partial, explicitly skipped, substituted, and unreported work. Never silently activate optional sessions. If giving an adherence percentage, name the denominator and treatment of unknown sessions.
- **Workload:** separate measured, reported, inferred, and projected totals. Use only confirmed completion as the basis for estimates; show assumptions and avoid overlapping device/session totals. Do not merge active exercise and elapsed gym time.
- **Nutrition:** include only user-confirmed complete days in full-day averages, naming the count. Describe partial days separately. Compare against the target version effective on each date, not the newest target retroactively.
- **Weight:** use [Infer body weight trend](../infer-body-weight-trend/SKILL.md). Bodyweight is optional and should not dominate a performance goal.
- **Recovery:** describe reported sleep, energy, soreness, pain, and direction of change without diagnosing causes. Flag unresolved safety concerns.
- **Benchmarks:** require a dated source and comparable movement/equipment/conditions. Mark inferred benchmarks as estimates. Do not rewrite original logs to fit a derived summary.

## Deliver a useful review

Follow the [detailed report format](references/report-format.md), including modality totals, zones plus unclassified minutes, required-work baseline, optional scenarios, nutrient denominators, comparable weight observations, and evidence gaps. Apply the user's current analysis preferences, never a fixed station exclusion or default zone split. Detailed load, workload, and benchmark rules are in [Workload and loads](../personal-training-coach/references/workload-and-loads.md).

Lead with the period and whether evidence is complete, partial, or in progress. Give a few concrete observations, followed by **Keep**, **Watch**, and **Proposed changes**. Name the evidence and uncertainty behind material recommendations. A lighter next week may be appropriate; progress does not always mean adding volume.

When asked to prepare next week, produce a dated draft that fits the user's availability and constraints. Explain changes relative to the adopted plan. Preserve the current plan until the user agrees to use the draft or has already explicitly authorized those changes. A completed review alone is not plan adoption.

Save a requested or closed review to `logs/weekly-reviews/` in folder mode, or to the notebook's weekly reviews section in chat mode. Use the period end date and record the full range. Save proposals separately from adopted changes and carry forward open questions.
