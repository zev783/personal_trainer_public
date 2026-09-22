# Run the trainer's analysis tools

For everyday use, ask **“Review my week”**, **“Show my workload totals”**, or **“Analyze my weight trend and explain the uncertainty.”** The assistant should use the tools when it has a Python runtime and access to your files. If it cannot run them, it must say so and limit itself to transparent descriptive arithmetic; it cannot invent model output.

The standard-library Python tools work from either a private folder or a saved notebook. They read the selected input, print results, and never change plans or logs. The separate research importer writes only an explicitly selected private workspace. No tool makes network requests or uploads data.

## Access and commands

In a local copy of this repository, use the commands below. In a chat session with Python/file support, supply `starter/trainer-tools.zip` and your latest notebook, and ask the assistant to extract the tools privately and use the same commands with actual sandbox paths. A native Claude skill ZIP includes those tools as well. Code execution depends on the account/session's capabilities; uploading a ZIP does not by itself prove execution.

```text
python scripts/audit_week.py --workspace personal --week-start YYYY-MM-DD --as-of YYYY-MM-DD
python scripts/audit_week.py --notebook MY-TRAINER.md --week-start YYYY-MM-DD --as-of YYYY-MM-DD --format json
python scripts/analyze_weight_history.py --notebook MY-TRAINER.md --unit kg --window-days 21 --format json
python scripts/analyze_weight_history.py --workspace personal --unit lb --as-of YYYY-MM-DD
```

Replace dates with the user's actual local dates. Choose any desired first day for the seven-day audit. `--as-of` is mandatory for the audit to avoid silently using the computer's timezone. Weight analysis defaults to the latest observed date and shows its actual data range. `--as-of` can limit that range explicitly.

For an explicitly justified prior-informed weight analysis, also provide `--expected-weekly-change`, `--expected-weekly-sd`, and `--prior-basis`. Both numeric values use the selected kg/lb unit; uncertainty must be positive. They are not derived automatically from a diet plan. Read the [model guide](../skills/infer-body-weight-trend/references/model.md) first.

## Structured records

The tools accept Markdown tables so records remain readable in an ordinary chat. The assistant maintains these tables from reported facts; the user does not need to type them. Blank templates are in `templates/workspace/logs/`. Notebook sections include the same tables. Preserve detailed source reports and label derived summaries. Avoid literal pipe characters inside table cells.

An empty cell, `unknown`, or `not reported` means missing, not zero. Numeric fields need plain decimal numbers in the column's units, with no commas, ranges, or prose. Put ranges in their own low/high columns and explanations in Assumptions. Malformed rows stop analysis instead of guessing.

### Weigh-ins

Required columns: `Date`, `Weight`, `Unit`, `Time/context`, `Clothing`, `Intake`, `Bathroom`, `Notes`. The tool also accepts a weight with its explicit unit in the Weight cell. Dated health files may omit Date in favor of their filename. No unit is guessed. Preserve separate genuine readings and correct a typo in place.

Narrow recognized condition labels include `nude`, `underwear only`, `pre-intake`, and `after urination`, used only when reported. A water-only amount can be `250 ml water`, `0.25 l water`, or `8 US fl oz water`. Other intake text gets broad uncertainty rather than a guessed exact correction. Unknowns and original wording remain visible in JSON results.

### Workload

Each non-overlapping segment has `Date`, stable `ID`, `Status`, `Required`, `Category`, `Modality`, `Active min`, optional `Min low` and `Min high`, `Distance km`, `Z1` through `Z5`, `Unclassified min`, `Race-specific min`, optional segment `Elapsed min`, `Evidence`, `Assumptions`, `Plan status`, and `Plan version`.

- Status: `completed`, `partial`, `planned`, `skipped`, or `unknown`.
- Required: `yes`, `no` (optional), `conditional`, or `unknown`.
- Category: `conditioning`, `strength`, `other`, or `unknown`; use the user's classification rules.
- Evidence: `measured`, `reported`, `inferred`, `projected`, or `unknown`. Inferences require assumptions; projected work cannot be recorded as completed.
- Planned rows enter projections only with `Plan status` set to `adopted` and a named `Plan version`. Draft, superseded, or unversioned planned work remains unresolved. The assistant must verify these labels against the actual active plan; the script cannot prove a user's approval from a table alone.
- Partial rows contain only completed work. Remaining work gets a distinct planned segment. When a whole planned segment becomes completed, update its row rather than adding another with the same ID.
- Zone values plus unclassified time equal known conditioning active time. If zones do not cover known activity, the tool labels the remainder unclassified. It never estimates zone splits from a sport name. Unknown-duration rows stay missing even if other totals can be calculated.
- Event-specific minutes overlap active minutes and are never added again. Whole-session elapsed time belongs in the log's metadata, not in every segment.

The audit rejects duplicate IDs, inconsistent ranges, zone totals above active time, and future completed entries. Optional/conditional segments remain separate alternatives. The projected baseline includes actuals and remaining required segments on or after the as-of date; old unreported planned work is unresolved. Known totals carry coverage counts so incomplete data cannot be presented as complete.

### Nutrition days

Use one summary row per date: `Date`, `Status`, `Calories`, `Protein g`, `Carbohydrate g`, `Fat g`, `Target calories`, `Target version`, `Basis`. Only user-confirmed `complete`, `completed`, `closed`, or `final` days enter full-day averages. Each nutrient has its own denominator. Do not put a known subtotal in the daily-total field when coverage is incomplete; keep it in itemized records and mark that summary field unknown. Basis distinguishes label-derived/reported values from estimates. Duplicate daily summaries stop analysis.

## Existing narrative records and the weekly report

Folder mode recognizes dated files in workouts, nutrition, health, check-ins, and measurements. Narrative-only records appear in coverage; they are not silently parsed into exact totals. The assistant can produce traceable structured summaries after reading them. Weight tables in the original time/context format remain supported when they include explicit units.

Use the audit as an arithmetic and navigation aid, then inspect original sources and produce the [weekly report](../skills/review-personal-training-week/references/report-format.md). The tool does not infer full-session adherence, diagnose recovery problems, adopt plans, or automatically publish benchmarks.
