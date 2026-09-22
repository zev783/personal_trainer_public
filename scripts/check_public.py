"""Check public paths, common disclosure patterns, and exact generated artifacts."""

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

if __package__:
    from .build_starter import ROOT, build, safe_path
    from .public_manifest import PUBLIC_FILES, TRANSLATION_PAIRS
else:
    from build_starter import ROOT, build, safe_path
    from public_manifest import PUBLIC_FILES, TRANSLATION_PAIRS

# These are tripwires, not a general personal-data classifier.
PATTERNS = (
    ("absolute user directory", re.compile(r"(?:[A-Za-z]:[\\/]Users[\\/][\w.-]+|/(?:Users|home)/[\w.-]+)[\\/]")),
    ("email address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("credential-like token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{24,})\b")),
)


def visible_files(root):
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root, capture_output=True, check=True,
    )
    return sorted(set(result.stdout.decode("utf-8").split("\0")) - {""})


def check_files(root, names):
    problems = []
    for name in names:
        if name not in PUBLIC_FILES:
            problems.append(f"Unexpected public or tracked path: {name}")
            continue
        try:
            path = safe_path(root, name)
            if path.suffix == ".zip":
                continue  # Exact expected bytes, including every entry, are checked by build().
            content = path.read_text(encoding="utf-8")
        except (OSError, ValueError) as error:
            problems.append(f"Cannot validate {name}: {error}")
            continue
        for label, pattern in PATTERNS:
            if pattern.search(content):
                problems.append(f"Review {name}: possible {label} (value withheld)")
    return problems


def check_translation_review(root):
    """Detect edits after the last bilingual review; hashes do not prove translation quality."""
    review = json.loads(safe_path(root, "docs/translation-review.json").read_text(encoding="utf-8"))
    expected = {name for pair in TRANSLATION_PAIRS for name in pair}
    hashes = review.get("sha256", {})
    if set(hashes) != expected:
        return ["Translation review must cover every English/Russian source pair"]
    problems = []
    for name in sorted(expected):
        # Normalize line endings so Windows and Linux check the same reviewed text.
        content = safe_path(root, name).read_text(encoding="utf-8").encode("utf-8")
        if hashlib.sha256(content).hexdigest() != hashes[name]:
            problems.append(f"Bilingual review required after editing: {name}")
    return problems


def main():
    try:
        names = visible_files(ROOT)
        problems = check_files(ROOT, names)
        missing = PUBLIC_FILES - set(names)
        problems.extend(f"Expected public file is missing or ignored: {name}" for name in sorted(missing))
        problems.extend(check_translation_review(ROOT))
        build(check=True)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Public check failed: {error}", file=sys.stderr)
        return 1
    if problems:
        print("Public check failed:\n" + "\n".join(problems), file=sys.stderr)
        return 1
    print(f"Checked {len(names)} public files and exact generated downloads. Review content before publishing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
