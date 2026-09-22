"""Explicit public inputs. Never discover build inputs from private working folders."""

SKILLS = (
    "personal-training-coach",
    "onboard-personal-training",
    "manage-personal-training-day",
    "manage-personal-training-nutrition",
    "review-personal-training-week",
    "infer-body-weight-trend",
    "research-personal-training",
)

TEMPLATE_FILES = (
    "templates/MY-TRAINER.md",
    "templates/workspace/README.md",
    "templates/workspace/profile/about-me.md",
    "templates/workspace/profile/goals.md",
    "templates/workspace/profile/constraints.md",
    "templates/workspace/profile/availability.md",
    "templates/workspace/profile/training-preferences.md",
    "templates/workspace/profile/gym-equipment.md",
    "templates/workspace/profile/gym-layout.md",
    "templates/workspace/goals/body-weight.md",
    "templates/workspace/goals/events/README.md",
    "templates/workspace/schedule/current.md",
    "templates/workspace/schedule/current-eating.md",
    "templates/workspace/schedule/weeks/README.md",
    "templates/workspace/templates/workouts/daily/_template.md",
    "templates/workspace/templates/workouts/weekly/_template.md",
    "templates/workspace/templates/workouts/blocks/_template.md",
    "templates/workspace/templates/nutrition/daily-targets.md",
    "templates/workspace/templates/nutrition/day-template.md",
    "templates/workspace/food/README.md",
    "templates/workspace/food/products/_template.md",
    "templates/workspace/food/recipes/_template.md",
    "templates/workspace/coaching/README.md",
    "templates/workspace/health/README.md",
    "templates/workspace/health/medical/README.md",
    "templates/workspace/health/labs/README.md",
    "templates/workspace/health/wearables/README.md",
    "templates/workspace/supplements/current-stack.md",
    "templates/workspace/benchmarks/current.md",
    "templates/workspace/research/README.md",
    "templates/workspace/prompts/research/README.md",
    "templates/workspace/automation/README.md",
    "templates/workspace/logs/workouts/README.md",
    "templates/workspace/logs/nutrition/README.md",
    "templates/workspace/logs/check-ins/README.md",
    "templates/workspace/logs/measurements/README.md",
    "templates/workspace/logs/health/README.md",
    "templates/workspace/logs/weekly-reviews/README.md",
    "templates/workspace/research/_note-template.md",
    "templates/workspace/research/index.md",
    "templates/workspace/research/sources/README.md",
    "templates/workspace/research/training/README.md",
    "templates/workspace/research/nutrition/README.md",
    "templates/workspace/research/recovery/README.md",
    "templates/workspace/research/supplements/README.md",
    "templates/workspace/logs/health/_template.md",
    "templates/workspace/logs/workouts/_template.md",
    "templates/workspace/logs/nutrition/_template.md",
    "templates/workspace/profile/analysis-preferences.md",
    "templates/workspace/templates/nutrition/shopping-list-template.md",
    "templates/workspace/prompts/research/_refresh-template.md",
    "templates/workspace/prompts/research/training-plan-refresh.md",
    "templates/workspace/prompts/research/nutrition-fueling-refresh.md",
    "templates/workspace/prompts/research/recovery-refresh.md",
    "templates/workspace/prompts/research/supplement-refresh.md",
    "templates/workspace/prompts/research/event-preparation-refresh.md",
    "templates/workspace/prompts/research/durability-experiment.md",
)

REFERENCE_FILES = (
    "docs/ANALYTICS.md",
    "skills/personal-training-coach/references/workload-and-loads.md",
    "skills/personal-training-coach/references/nutrition-control.md",
    "skills/review-personal-training-week/references/report-format.md",
    "skills/infer-body-weight-trend/references/model.md",
    "templates/workspace/research/_note-template.md",
)

RESEARCH_FILES = (
    "research/README.md",
    "research/training/concurrent-training.md",
    "research/training/durability-and-transitions.md",
    "research/nutrition/fueling-and-energy.md",
    "research/recovery/sleep-and-monitoring.md",
    "research/supplements/evidence-and-risk.md",
    "research/measurement/weight-variability.md",
)

PROMPT_FILES = (
    "templates/workspace/prompts/research/_refresh-template.md",
    "templates/workspace/prompts/research/training-plan-refresh.md",
    "templates/workspace/prompts/research/nutrition-fueling-refresh.md",
    "templates/workspace/prompts/research/recovery-refresh.md",
    "templates/workspace/prompts/research/supplement-refresh.md",
    "templates/workspace/prompts/research/event-preparation-refresh.md",
    "templates/workspace/prompts/research/durability-experiment.md",
)

ANALYSIS_TOOLS = (
    "scripts/records.py",
    "scripts/audit_week.py",
    "scripts/analyze_weight_history.py",
    "scripts/import_research.py",
)

LOCALIZED_INPUTS = (
    "docs/PROJECT-INSTRUCTIONS.ru.txt",
    "templates/MY-TRAINER.ru.md",
)

# Reviewed pairs: the public checker flags edits until both are reviewed again.
TRANSLATION_PAIRS = (
    ("README.md", "README.ru.md"),
    ("START-HERE.md", "START-HERE.ru.md"),
    ("docs/PROJECT-INSTRUCTIONS.txt", "docs/PROJECT-INSTRUCTIONS.ru.txt"),
    ("templates/MY-TRAINER.md", "templates/MY-TRAINER.ru.md"),
    ("docs/FAQ.md", "docs/FAQ.ru.md"),
    ("docs/SAVING-YOUR-PROGRESS.md", "docs/SAVING-YOUR-PROGRESS.ru.md"),
    ("docs/PRIVACY.md", "docs/PRIVACY.ru.md"),
    ("docs/ADVANCED-OPTIONS.md", "docs/ADVANCED-OPTIONS.ru.md"),
)

CLAUDE_CODE_FILES = (
    ".claude/skills/personal-training-coach/SKILL.md",
    ".claude/skills/personal-training-coach/references/COACH-HANDBOOK.md",
    ".claude/skills/personal-training-coach/references/RESEARCH-LIBRARY.md",
    ".claude/skills/personal-training-coach/assets/MY-TRAINER.md",
    ".claude/skills/personal-training-coach/LICENSE",
) + tuple(
    ".claude/skills/personal-training-coach/" + name for name in ANALYSIS_TOOLS
)

GENERATED_FILES = (
    "agent.jsonl",
    "starter/PROJECT-INSTRUCTIONS.txt",
    "starter/agent.jsonl",
    "starter/CLAUDE.md",
    "starter/COACH-HANDBOOK.md",
    "starter/COACH-HANDBOOK.txt",
    "starter/MY-TRAINER.md",
    "starter/personal-training-coach.zip",
    "starter/trainer-tools.zip",
    "starter/RESEARCH-LIBRARY.md",
    "starter/ru/PROJECT-INSTRUCTIONS.txt",
    "starter/ru/MY-TRAINER.md",
    "starter/ru/COACH-HANDBOOK.md",
    "starter/ru/COACH-HANDBOOK.txt",
    "starter/ru/CLAUDE.md",
    "starter/ru/agent.jsonl",
    "starter/ru/RESEARCH-LIBRARY.md",
) + CLAUDE_CODE_FILES

PUBLIC_FILES = frozenset((
    "README.md",
    "START-HERE.md",
    "AGENTS.md",
    "CLAUDE.md",
    "LICENSE",
    ".gitignore",
    ".gitattributes",
    ".github/workflows/check.yml",
    "docs/PROJECT-INSTRUCTIONS.txt",
    "docs/SAVING-YOUR-PROGRESS.md",
    "docs/PRIVACY.md",
    "docs/FAQ.md",
    "docs/FOLDER-MODE.md",
    "docs/MAINTAINING.md",
    "docs/COACHING-SCENARIOS.md",
    "scripts/public_manifest.py",
    "scripts/build_starter.py",
    "scripts/init_personal.py",
    "scripts/check_public.py",
    "tests/test_starter.py",
    "tests/test_analytics.py",
    "docs/PORT-COVERAGE.md",
    "docs/translation-review.json",
) + TEMPLATE_FILES + GENERATED_FILES + REFERENCE_FILES + RESEARCH_FILES + ANALYSIS_TOOLS
  + LOCALIZED_INPUTS + tuple(name for pair in TRANSLATION_PAIRS for name in pair) + tuple(
    f"skills/{name}/SKILL.md" for name in SKILLS
))
