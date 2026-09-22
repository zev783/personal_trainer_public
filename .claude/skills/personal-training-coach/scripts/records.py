"""Read only the selected trainer records; shared by the portable analysis tools."""

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import math
import re


@dataclass(frozen=True)
class Source:
    name: str
    text: str
    day: date | None = None
    domain: str = "notebook"


def selected_sources(workspace=None, notebook=None):
    if (workspace is None) == (notebook is None):
        raise ValueError("Choose exactly one --workspace or --notebook")
    if notebook is not None:
        path = Path(notebook)
        if path.is_symlink():
            raise ValueError("Use the actual notebook file, not a symbolic link")
        return [Source(path.name, path.read_text(encoding="utf-8-sig"))]
    root = Path(workspace).resolve()
    if not (root / "logs").is_dir():
        raise ValueError("The selected workspace must contain a logs directory")
    result = []
    for domain in ("workouts", "nutrition", "health", "check-ins", "measurements"):
        directory = root / "logs" / domain
        if not directory.exists():
            continue
        if directory.is_symlink() or not directory.resolve().is_relative_to(root):
            raise ValueError("Linked log directories are not supported")
        for path in sorted(directory.glob("*.md")):
            if not re.match(r"^\d{4}-\d{2}-\d{2}(?:-|\.md$)", path.name):
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                raise ValueError("Linked log files are not supported")
            result.append(Source(path.relative_to(root).as_posix(),
                                 path.read_text(encoding="utf-8-sig"),
                                 date.fromisoformat(path.name[:10]), domain))
    return result


def key(value):
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def tables(source):
    """Yield named rows of Markdown tables, retaining line-level provenance."""
    lines = source.text.splitlines()
    heading = ""
    i = 0
    while i < len(lines):
        if lines[i].startswith("#"):
            heading = lines[i].lstrip("# ").strip()
        if i + 1 < len(lines) and lines[i].strip().startswith("|"):
            separator = cells(lines[i + 1])
            if separator and all(re.fullmatch(r":?-{3,}:?", item) for item in separator):
                headers = [key(item) for item in cells(lines[i])]
                if len(headers) != len(set(headers)) or len(headers) != len(separator):
                    raise ValueError(f"Ambiguous table headers at {source.name}:{i + 1}")
                i += 2
                while i < len(lines) and lines[i].strip().startswith("|"):
                    values = cells(lines[i])
                    if len(values) != len(headers):
                        raise ValueError(f"Malformed table row at {source.name}:{i + 1}")
                    if any(value.strip() for value in values):
                        row = dict(zip(headers, values))
                        row["_source"] = f"{source.name}:{i + 1}"
                        row["_heading"] = heading
                        row["_file_date"] = source.day.isoformat() if source.day else ""
                        yield row
                    i += 1
                continue
        i += 1


def cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def number(value, field="value", nonnegative=True):
    value = str(value).strip()
    if value.lower() in ("", "unknown", "not reported", "not provided", "none", "-", "n/a"):
        return None
    if not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)", value):
        raise ValueError(f"{field} needs a plain number or unknown, not {value!r}")
    result = float(value)
    if not math.isfinite(result) or (nonnegative and result < 0):
        raise ValueError(f"Invalid {field}")
    return result


def row_date(row):
    value = row.get("date") or row.get("_file_date")
    if not value:
        raise ValueError(f"Missing date at {row['_source']}")
    return date.fromisoformat(value)


def frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    block = text.split("---", 2)[1]
    return {key(k): v.strip().strip('\"\'') for line in block.splitlines()
            if ":" in line for k, v in [line.split(":", 1)]}


def input_arguments(parser):
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--workspace", type=Path, help="Private folder containing logs/")
    group.add_argument("--notebook", type=Path, help="Private MY-TRAINER.md with structured tables")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")


def escape(value):
    return str(value).replace("|", "/").replace("\n", " ")
