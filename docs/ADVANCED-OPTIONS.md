# Optional tools after setup

Start with [the beginner guide](../START-HERE.md). Ordinary coaching needs project instructions, one coaching handbook, and one private notebook. [По-русски](ADVANCED-OPTIONS.ru.md).

## JSONL knowledge bundle

[agent.jsonl](../starter/agent.jsonl) contains the same public workflows, references, and research as the handbook. It is a custom upload format, not an automatically discovered ChatGPT setting. Use it instead of the handbook if your app accepts it, and still paste the project instructions. There is no need to upload both.

## Research and calculated analysis

Ask “Research whether this change would help my goal; show sources and uncertainty.” The coach needs browsing to verify current sources. The stored research library has checked dates and is not a continuously updated literature review. Findings remain suggestions until you agree to change your plan.

For calculated weekly audits and statistical weight trends, attach [trainer-tools.zip](../starter/trainer-tools.zip) in a session with Python execution and ask the assistant to use it with your current notebook. An uploaded ZIP does not grant execution. If execution is unavailable, use the descriptive coaching workflows. See [analytics](ANALYTICS.md).

## Claude custom skill or Claude Code

If your Claude account supports custom skills, upload [personal-training-coach.zip](../starter/personal-training-coach.zip) through its skill upload controls and enable it for training conversations. It includes the public handbook and analysis tools. Keep your private notebook separate. See [Claude's skill guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

Claude Code users can open the repository: the root `CLAUDE.md` points to `.claude/skills/personal-training-coach/`. Codex uses `AGENTS.md`. These repository entrypoints are distinct from the self-contained file uploaded in a Claude Project.

## Private local folders

For an assistant that can actually edit local files, use [folder mode](FOLDER-MODE.md). Choose one authoritative private workspace or notebook and reconcile it before switching modes. Do not fill the public templates with personal data.

## Russian coaching

[The Russian guide](../START-HERE.ru.md) uses translated instructions and a translated blank notebook from `starter/ru`. Its generated bundles contain the identical English workflow and research sources, plus Russian language instructions. The conversation and notebook notes are in Russian. Technical table headings and values stay compatible with the shared analysis tools; the coach explains them instead of asking the user to translate them.
