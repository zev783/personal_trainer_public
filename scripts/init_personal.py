"""Initialize the ignored personal folder from blank templates, without overwrites."""

from pathlib import Path
import sys

if __package__:
    from .build_starter import ROOT, read_public, safe_path
    from .public_manifest import TEMPLATE_FILES
else:
    from build_starter import ROOT, read_public, safe_path
    from public_manifest import TEMPLATE_FILES


def initialize(root=ROOT):
    root = Path(root)
    pending = []
    existing = 0
    for source in TEMPLATE_FILES:
        if not source.startswith("templates/workspace/"):
            continue
        relative = source.removeprefix("templates/workspace/")
        target = safe_path(root, "personal/" + relative)
        if target.exists():
            if not target.is_file():
                raise ValueError(f"Expected a file at personal/{relative}")
            existing += 1
            continue
        # Read and validate everything before writing the first file.
        pending.append((target, read_public(root, source)))
    for target, content in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8", newline="\n") as output:
            output.write(content)
    return len(pending), existing


def main():
    try:
        created, preserved = initialize()
    except (OSError, ValueError) as error:
        print(f"Initialization stopped: {error}", file=sys.stderr)
        return 1
    print(f"Private folder ready: {created} blank files created, {preserved} existing files preserved.")
    print("Your records belong in personal/. Back them up privately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
