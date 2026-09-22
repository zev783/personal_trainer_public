---
name: personal-training-coach
description: Guide personal trainer setup, training, nutrition, weekly analysis, weight trends, and source-backed research using the user's private records.
---

# Personal training coach

Read [the coaching handbook](references/COACH-HANDBOOK.md) before coaching. It contains the shared rules, focused workflows, analytics schema, model assumptions, research briefs, and prompts. Use the user's latest private notebook as the record. For a genuinely new user, use [the blank notebook](assets/MY-TRAINER.md). Never replace an existing notebook with that blank asset.

Optional Python tools are in scripts/. Run audit_week.py or analyze_weight_history.py only with actual tool access and explicit user-selected records, as described in the handbook. They read records and print analysis. import_research.py preserves an explicitly selected source in a private workspace; it never adopts plans. No runtime or browsing capability is implied merely by enabling this skill.
