---
name: research-personal-training
description: Research or refresh training, nutrition, recovery, event, or supplement questions; preserve supplied sources, verify claims, assess applicability, and keep proposed changes separate from adopted plans.
---

# Research personal training

Follow [Personal training coach](../personal-training-coach/SKILL.md). Use this when the user asks for evidence, a research refresh, comparison of methods, evaluation of a supplied paper or AI report, or a source-backed proposed plan change. Ordinary workout delivery does not require repeating a literature review.

## Establish the question and evidence boundary

Read only the relevant goals, constraints, equipment, schedule, dated response logs, and prior research. Confirm the decision: improve a program, evaluate a claim, check event rules, investigate fueling, or assess evidence/safety for a supplement. Use generic non-identifying search terms. Do not upload a private notebook to search, copy other people's records, or assume that a plan or product order proves actual use.

Consult the [research library](../../research/README.md) for seed evidence and topic questions, then verify time-sensitive claims with current sources. The library is an explicitly limited starting set, not an exhaustive or continuously updated review. Choose a reusable prompt under `prompts/research/` in the private folder, or the corresponding prompt section in the handbook.

## Import without endorsing

When the user provides a report, preserve the original before deriving a summary. Keep source type, title, supplied author/model if known, import date, URL if available, and verification state. AI-generated text with citations is still a synthesis until the citations and associated claims are checked.

With local file tools, `python scripts/import_research.py --workspace personal --source SOURCE.txt --topic TOPIC --date YYYY-MM-DD --title TITLE --source-type ai-synthesis` saves exact source bytes and a SHA-256 import note in the private workspace. Paths/dates/titles must be actual user-selected values, not these placeholders. In chat, give the user the original source and separate import note to save; compute a hash only with an actual tool. Never fabricate a hash or claim the provider's stored attachment was modified.

## Research method

1. Record the research date, evidence cutoff, question, and relevant record versions. Record model name only if known. Read the actual source, not just a title or another AI's citation.
2. For rules, use the event organizer or governing body and the correct event/category/season. For empirical findings, inspect original studies; use systematic reviews, meta-analyses, consensus statements, and official guidance as labeled syntheses. Distinguish all of these from expert opinion, mechanistic reasoning, and marketing.
3. For material claims record population, design, intervention/comparator, outcome, duration, effect and uncertainty if available, applicability, limitations, and direct source URL/identifier. Do not invent numbers missing from an abstract. State whether only the abstract or full text was checked, and inspect corrections/retractions when indicated.
4. Examine contrary evidence and alternative explanations. A biomarker, lactate concentration, or attractive mechanism does not by itself demonstrate better performance. A study in trained cyclists does not establish an optimal running or mixed-sport dose.
5. Match evidence to the user's goal, baseline, available time, equipment, recovery, and relevant disclosed restrictions. Keep uncertainty when records are incomplete. Health-sensitive and supplement recommendations require appropriate professional review; no unsupervised medication or hormone protocols.
6. If browsing is unavailable, label the result `source review only` or `unverified draft`, list claims needing verification, and avoid claiming a current literature search.

## Output and adoption

Use the [research note format](../../templates/workspace/research/_note-template.md): scope, concise conclusion, evidence table, what remains supported, what changed, applicability, uncertainty/safety, exact proposed changes, and sources. Keep separate claim verification and adoption statuses: `verified source` does not mean `adopted plan`.

Save each refresh as a new dated private note, link the previous note, and update the private research index. Never silently overwrite a supplied original or prior conclusion. In notebook mode, append the note/source index and preserve or explicitly archive detailed notes.

When proposing an experiment, specify the question, one changed variable when practical, baseline/comparator, controlled conditions, outcome measures, review date, and safety/stop conditions. A proposal does not establish that the experiment occurred. If the user already explicitly authorized a specific plan edit, implement only that scope after resolving material safety/evidence gaps; otherwise keep the proposal inactive until adoption. Record the research basis, effective date, and affected plan version upon adoption. Past actual logs remain unchanged.
