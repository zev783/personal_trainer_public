"""Preserve a user-selected source and import note in a private workspace; never adopt it."""

import argparse
from datetime import date
import hashlib
from pathlib import Path
import re
import sys


def preserve_source(workspace, source, topic, imported_on, title, source_type, url=""):
    root = Path(workspace).resolve()
    original = Path(source)
    project = Path(__file__).resolve().parents[1]
    if (not (root / "logs").is_dir() or root == project
            or root.is_relative_to(project / "templates") or root.is_relative_to(project / "starter")):
        raise ValueError("Choose a private workspace containing logs/, not the public repository")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", topic):
        raise ValueError("Topic must use lowercase letters, digits, and hyphens")
    if original.suffix.lower() not in {".md", ".txt", ".pdf"} or not original.is_file():
        raise ValueError("Select an existing Markdown, text, or PDF source")
    for label, value in (("title", title), ("source type", source_type), ("URL", url)):
        if "\n" in value or "\r" in value:
            raise ValueError(f"Use one line for {label}")
    if url and not url.startswith(("https://", "http://")):
        raise ValueError("Source URL must be HTTP(S), or omitted")
    data = original.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    research = root / "research"
    source_dir = research / "sources"
    for path in (research, source_dir):
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError("Linked research directories are not supported")
    prefix = f"{imported_on.isoformat()}-{topic}"
    destination = source_dir / f"{prefix}-{digest[:12]}{original.suffix.lower()}"
    note = research / f"{prefix}-import.md"
    if destination.exists() or note.exists():
        raise ValueError("Import already exists; choose a new topic/version rather than overwrite history")
    note_text = (f"# {title}\n\n- Imported: {imported_on.isoformat()}\n- Source type: {source_type}\n"
        f"- Source URL: {url or 'not supplied'}\n- Preserved source: sources/{destination.name}\n"
        f"- SHA-256: {digest}\n- Verification: unverified import\n- Adoption: research only\n\n"
        "## Claims and limitations\n\nNot yet reviewed. Import preserves supplied bytes; it does not validate claims, "
        "citations, authorship, or applicability. Read and verify before summarizing findings.\n\n"
        "## Proposed changes\n\nNone adopted. No training, nutrition, supplement, or actual-log records changed.\n")
    source_dir.mkdir(parents=True, exist_ok=True)
    with destination.open("xb") as output:
        output.write(data)
    with note.open("x", encoding="utf-8", newline="\n") as output:
        output.write(note_text)
    return {"source": destination.relative_to(root).as_posix(),
            "note": note.relative_to(root).as_posix(), "sha256": digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--date", type=date.fromisoformat, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source-type", choices=("user-supplied", "ai-synthesis", "article", "official-guidance"), required=True)
    parser.add_argument("--url", default="")
    args = parser.parse_args()
    try:
        result = preserve_source(args.workspace, args.source, args.topic, args.date, args.title, args.source_type, args.url)
    except (OSError, ValueError) as error:
        print(f"Research import stopped: {error}", file=sys.stderr)
        return 2
    print(f"Saved {result['source']} and {result['note']}; SHA-256 {result['sha256']}. Research only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
