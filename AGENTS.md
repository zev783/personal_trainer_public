# Shared agent entrypoint

Read [the personal-training-coach skill](skills/personal-training-coach/SKILL.md) before coaching or editing coaching behavior. It routes to the other skills and defines record authority.

For repository maintenance, read [docs/MAINTAINING.md](docs/MAINTAINING.md). Public sources are generic instructions and blank templates. Personal records belong only in the ignored `personal/` directory or outside this repository. Never read or import a neighboring personal workspace unless the user explicitly requests it. Never publish personal records.

Generated files in `starter/`, the root `agent.jsonl`, and the Claude Code package under `.claude/skills/` come from `python scripts/build_starter.py`; edit their canonical sources instead. `agent.jsonl` is an uploadable custom knowledge bundle, not an automatically discovered Codex instruction file. Validate with `python scripts/check_public.py`, `python scripts/build_starter.py --check`, and `python -m unittest discover -s tests`.
