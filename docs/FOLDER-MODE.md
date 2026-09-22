# Optional: use a local folder

The [normal app setup](../START-HERE.md) needs no installation. This option is for an assistant session that can actually read and write a selected local folder, such as a coding agent or a desktop mode with folder access.

1. Download or clone this repository into a folder of your choice.
2. Open that folder in your assistant. Tell it: **“Read AGENTS.md and help me set up my own personal trainer. Store all my records in personal/.”**
3. The assistant can run `python scripts/init_personal.py` to create your private folder from blank templates. If Python is unavailable, it can copy only `templates/workspace/` into a new `personal/` directory, without replacing anything already there.
4. Complete the setup conversation and agree to your first plan.
5. Ask the assistant where it saved the records. Back up `personal/` privately yourself.

You can run the helper yourself with Python 3.10 or newer, from the repository folder:

```text
python scripts/init_personal.py
```

On Windows, `py` may be the command available instead of `python`. No third-party Python packages are needed. Running initialization again preserves existing files and adds only missing blank templates.

## Folder map

```text
personal/                 Your private working records; ignored by Git
  profile/                Goals, constraints, availability, equipment, preferences
  goals/                  Optional event and bodyweight goals
  schedule/               Current training and nutrition plan pointers
    weeks/                Dated draft and adopted weekly plans
  templates/              Your own reusable workout and nutrition plans
  logs/
    workouts/             Actual reported exercise
    nutrition/            Actual reported food and drink
    check-ins/            Recovery and practical constraints
    measurements/         Optional periodic measurements
    health/               Optional health observations and weigh-in conditions
    weekly-reviews/       Source-linked reviews and proposals
  coaching/               Observations and tested helpful cues
  food/products/          Serving-specific product facts
  food/recipes/           Recipe facts and yield
  health/                 Optional relevant source context
  supplements/            Optional reported use; no default regimen
  benchmarks/             Traceable measured or estimated performance summaries
  research/               Findings that have not automatically become a plan
  prompts/                Reusable research questions
  automation/             Notes for future, explicitly added automation
```

The tracked `templates/workspace/` mirrors this structure with blank files. The initializer reads only those templates. It never migrates an existing person's workspace.

## Skills and discovery

`AGENTS.md` and `CLAUDE.md` route local assistants to `skills/personal-training-coach/SKILL.md`. Other workflows live alongside it. This is explicit instruction routing; it does not assume every app automatically discovers a root `skills/` folder. If your assistant ignores root guidance, ask it to read `AGENTS.md` explicitly.

For native Claude skill upload, use the generated ZIP described in [Start here](../START-HERE.md). It is self-contained. Do not install loose workflow folders without their shared core, because they refer to each other. Ordinary ChatGPT project use does not depend on any of this.

## Move between folder and chat

Ask the local assistant to export the complete current profile, approved plans, and records into a private notebook, preserving history and sources. This is an assistant task, not an included automatic sync command. Review it before uploading it to a private project. When coming back, identify which version is authoritative and reconcile changes before importing. Keep historical backups out of project knowledge to avoid competing active versions.
