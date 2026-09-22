"""Build portable downloads from named public inputs only (Python standard library)."""

import argparse
import io
import json
from pathlib import Path
import re
import posixpath
import sys
import zipfile

if __package__:
    from .public_manifest import GENERATED_FILES, SKILLS, REFERENCE_FILES, RESEARCH_FILES, PROMPT_FILES, ANALYSIS_TOOLS
else:
    from public_manifest import GENERATED_FILES, SKILLS, REFERENCE_FILES, RESEARCH_FILES, PROMPT_FILES, ANALYSIS_TOOLS

ROOT = Path(__file__).resolve().parents[1]


def safe_path(root, relative):
    """Refuse traversal and linked files/directories before reading or writing."""
    root = Path(root).resolve()
    relative = Path(relative)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Expected a path within the selected public source root")
    path = root
    for part in relative.parts:
        path = path / part
        # is_junction exists on Python 3.12+; resolve containment also protects older versions.
        if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
            raise ValueError(f"Linked paths are not public build inputs or outputs: {relative}")
    if not path.resolve().is_relative_to(root):
        raise ValueError(f"Path escaped public source root: {relative}")
    return path


def read_public(root, relative):
    return safe_path(root, relative).read_text(encoding="utf-8")


def skill_body(text):
    match = re.match(r"\A---\n.*?\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError("A skill source is missing frontmatter")
    return text[match.end():].strip()


def document_anchor(name):
    if name.startswith("skills/") and name.endswith("/SKILL.md"):
        return name.split("/")[1]
    return "ref-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def render_document(root, paths, title, all_paths):
    anchors = {name: document_anchor(name) for name in all_paths}
    included = set(paths)
    parts = [f"# {title}\n\nGenerated only from public instructions and sources. No personal records.\n\n"
             + "## Contents\n\n" + "\n".join(
                 f"- [{Path(name).stem if not name.endswith('/SKILL.md') else name.split('/')[1]}](#{anchors[name]})"
                 for name in paths)]
    for name in paths:
        content = read_public(root, name)
        body = skill_body(content) if name.endswith("/SKILL.md") else content.strip()
        def rewrite(match):
            target = match.group(1)
            if target.startswith(("https://", "http://", "#")):
                return match.group(0)
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), target.split("#")[0]))
            if resolved not in anchors:
                raise ValueError(f"Unpackaged reference from {name}: {target}")
            prefix = "" if resolved in included else "COACH-HANDBOOK.md"
            return f"]({prefix}#{anchors[resolved]})"
        body = re.sub(r"\]\(([^)]+)\)", rewrite, body)
        parts.append(f'<a id="{anchors[name]}"></a>\n\n{body}')
    return ("\n\n---\n\n".join(parts) + "\n").encode("utf-8")


def zip_bytes(entries):
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as package:
        for name, content in entries:
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            package.writestr(entry, content)
    return archive.getvalue()


def source_category(name):
    if name.startswith("skills/"):
        return "workflow"
    if name in RESEARCH_FILES:
        return "research"
    if name in PROMPT_FILES:
        return "research_prompt"
    return "reference"


def render_agent_jsonl(root, paths, instructions, language="en"):
    """Render a portable knowledge bundle; this is not a platform config schema."""
    schema = "personal-trainer-agent-bundle/v1"
    records = [{
        "schema": schema,
        "type": "bundle",
        "id": "personal-training-coach",
        "language": language,
        "title": "Personal trainer coaching knowledge bundle",
        "usage": (
            "Upload this file as project knowledge and paste the project_instructions record "
            "into the app's project instructions. This custom JSONL format is a portable source "
            "bundle, not an automatically discovered ChatGPT configuration file."
        ),
        "privacy": (
            "Contains public generic instructions only. Keep the user's latest MY-TRAINER.md "
            "as a separate private project source and treat it as the record of plans and history."
        ),
        "document_count": len(paths),
    }, {
        "schema": schema,
        "type": "project_instructions",
        "id": "project-instructions",
        "content": instructions.decode("utf-8").strip(),
    }]
    for ordinal, name in enumerate(paths, start=1):
        content = read_public(root, name)
        body = skill_body(content) if name.endswith("/SKILL.md") else content.strip()
        records.append({
            "schema": schema,
            "type": "document",
            "id": document_anchor(name),
            "ordinal": ordinal,
            "category": source_category(name),
            "source_path": name,
            "content": body,
        })
    return ("\n".join(json.dumps(record, ensure_ascii=False, separators=(",", ":"))
                      for record in records) + "\n").encode("utf-8")


def render_outputs(root=ROOT):
    skill_paths = tuple(f"skills/{name}/SKILL.md" for name in SKILLS)
    handbook_paths = skill_paths + REFERENCE_FILES + RESEARCH_FILES + PROMPT_FILES
    handbook = render_document(root, handbook_paths, "Personal trainer coaching handbook", handbook_paths)
    library = render_document(root, RESEARCH_FILES, "Personal trainer research library", handbook_paths)
    instructions = read_public(root, "docs/PROJECT-INSTRUCTIONS.txt").encode("utf-8")
    russian_instructions = read_public(root, "docs/PROJECT-INSTRUCTIONS.ru.txt").encode("utf-8")
    russian_notebook = read_public(root, "templates/MY-TRAINER.ru.md").encode("utf-8")
    russian_intro = (
        "# Справочник персонального тренера\n\n"
        "Отвечай пользователю по-русски, если он не попросит другой язык. "
        "Пользователь не обязан читать внутренние материалы: объясняй нужное простыми словами. "
        "Ниже — те же полные английские методики, исследования и запросы, что и в основной версии. "
        "Личные записи находятся в отдельном актуальном MY-TRAINER.md. "
        "Сохраняй служебные заголовки и значения таблиц для совместимости с анализом.\n\n---\n\n"
    ).encode("utf-8")
    russian_handbook = russian_intro + handbook
    agent_jsonl = render_agent_jsonl(root, handbook_paths, instructions)
    notebook = read_public(root, "templates/MY-TRAINER.md").encode("utf-8")
    scripts = [(name, read_public(root, name).encode("utf-8")) for name in ANALYSIS_TOOLS]
    license_text = read_public(root, "LICENSE").encode("utf-8")
    skill = (
        "---\nname: personal-training-coach\n"
        "description: Guide personal trainer setup, training, nutrition, weekly analysis, weight "
        "trends, and source-backed research using the user's private records.\n"
        "---\n\n# Personal training coach\n\n"
        "Read [the coaching handbook](references/COACH-HANDBOOK.md) before coaching. "
        "It contains the shared rules, focused workflows, analytics schema, model assumptions, "
        "research briefs, and prompts. Use the user's latest private notebook as the record. "
        "For a genuinely new user, use [the blank notebook](assets/MY-TRAINER.md). Never replace "
        "an existing notebook with that blank asset.\n\n"
        "Optional Python tools are in scripts/. Run audit_week.py or analyze_weight_history.py "
        "only with actual tool access and explicit user-selected records, as described in the handbook. "
        "They read records and print analysis. import_research.py preserves an explicitly selected "
        "source in a private workspace; it never adopts plans. No runtime or browsing capability "
        "is implied merely by enabling this skill.\n"
    ).encode("utf-8")
    claude_entries = [
        ("personal-training-coach/SKILL.md", skill),
        ("personal-training-coach/references/COACH-HANDBOOK.md", handbook),
        ("personal-training-coach/references/RESEARCH-LIBRARY.md", library),
        ("personal-training-coach/assets/MY-TRAINER.md", notebook),
        ("personal-training-coach/LICENSE", license_text),
    ] + [("personal-training-coach/" + name, content) for name, content in scripts]
    tools_readme = (
        "# Private trainer analysis tools\n\n"
        "Read COACH-HANDBOOK.md for schemas, model assumptions, research workflow, and examples.\n"
        "Python 3.10+; standard library only. Run from this extracted folder.\n\n"
        "python scripts/audit_week.py --help\n"
        "python scripts/analyze_weight_history.py --help\n"
        "python scripts/import_research.py --help\n\n"
        "Choose your private notebook or workspace explicitly. Audit and weight analysis are "
        "read-only; research import writes preserved source bytes and a note only to the "
        "chosen private workspace. No networking, automatic plan changes, or background tasks.\n"
    ).encode("utf-8")
    claude_project = (
        "# Personal trainer knowledge for Claude Projects\n\n"
        "This self-contained file contains public coaching instructions and reference material. "
        "Add it to a private Claude Project together with the user's latest MY-TRAINER.md, then "
        "paste the project instructions below into the project's instructions field. The notebook "
        "is the authority for personal plans and history.\n\n"
        "## Project instructions\n\n"
    ).encode("utf-8") + instructions.rstrip() + b"\n\n---\n\n## Coaching handbook\n\n" + handbook
    outputs = {
        "agent.jsonl": agent_jsonl,
        "starter/PROJECT-INSTRUCTIONS.txt": instructions,
        "starter/agent.jsonl": agent_jsonl,
        "starter/CLAUDE.md": claude_project,
        "starter/COACH-HANDBOOK.md": handbook,
        "starter/COACH-HANDBOOK.txt": handbook,
        "starter/MY-TRAINER.md": notebook,
        "starter/personal-training-coach.zip": zip_bytes(claude_entries),
        "starter/trainer-tools.zip": zip_bytes(scripts + [
            ("README.md", tools_readme), ("COACH-HANDBOOK.md", handbook),
            ("MY-TRAINER.md", notebook), ("LICENSE", license_text)]),
        "starter/RESEARCH-LIBRARY.md": library,
        "starter/ru/PROJECT-INSTRUCTIONS.txt": russian_instructions,
        "starter/ru/MY-TRAINER.md": russian_notebook,
        "starter/ru/COACH-HANDBOOK.md": russian_handbook,
        "starter/ru/COACH-HANDBOOK.txt": russian_handbook,
        "starter/ru/CLAUDE.md": (
            "# Персональный тренер для проекта Claude\n\n"
            "Загрузите этот файл и актуальный MY-TRAINER.md в личный проект. "
            "Вставьте инструкции ниже в поле инструкций проекта. "
            "Личные планы и история берутся из дневника.\n\n## Инструкции проекта\n\n"
        ).encode("utf-8") + russian_instructions.rstrip() + b"\n\n---\n\n" + russian_handbook,
        "starter/ru/agent.jsonl": render_agent_jsonl(root, handbook_paths, russian_instructions, "ru"),
        "starter/ru/RESEARCH-LIBRARY.md": library,
    }
    for name, content in claude_entries:
        outputs[".claude/skills/" + name] = content
    return outputs


def build(root=ROOT, check=False):
    outputs = render_outputs(root)
    # Preflight every output before making any changes.
    paths = {name: safe_path(root, name) for name in outputs}
    if check:
        stale = [name for name, data in outputs.items()
                 if not paths[name].is_file() or paths[name].read_bytes() != data]
        if stale:
            raise ValueError("Missing or stale downloads: " + ", ".join(stale))
        return
    for name, data in outputs.items():
        paths[name].parent.mkdir(parents=True, exist_ok=True)
        paths[name].write_bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check without changing files")
    args = parser.parse_args()
    try:
        build(check=args.check)
    except (OSError, ValueError) as error:
        print(f"Starter build failed: {error}", file=sys.stderr)
        return 1
    print("Starter downloads are current." if args.check else "Built public handbooks, notebooks, and portable tool packages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
