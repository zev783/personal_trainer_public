"""Behavior checks for the privacy boundary and portable starter packaging."""

import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
import zipfile

from scripts.build_starter import ROOT, build, render_outputs, document_anchor
from scripts.check_public import check_files, visible_files, check_translation_review
from scripts.init_personal import initialize
from scripts.public_manifest import (GENERATED_FILES, PUBLIC_FILES, SKILLS, TEMPLATE_FILES,
                                    REFERENCE_FILES, RESEARCH_FILES, PROMPT_FILES, ANALYSIS_TOOLS,
                                    LOCALIZED_INPUTS, TRANSLATION_PAIRS)


class StarterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        sources = list(TEMPLATE_FILES) + [f"skills/{name}/SKILL.md" for name in SKILLS]
        sources += list(REFERENCE_FILES + RESEARCH_FILES + PROMPT_FILES + ANALYSIS_TOOLS)
        sources += ["docs/PROJECT-INSTRUCTIONS.txt", ".gitignore", "LICENSE"]
        sources += list(LOCALIZED_INPUTS)
        for name in sources:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)

    def test_initialization_preserves_records_and_adds_missing_templates(self):
        created, preserved = initialize(self.root)
        self.assertEqual(created, len(TEMPLATE_FILES) - 1)
        self.assertEqual(preserved, 0)
        profile = self.root / "personal/profile/about-me.md"
        profile.write_text("Synthetic private profile", encoding="utf-8")
        missing = self.root / "personal/schedule/current.md"
        missing.unlink()
        created, preserved = initialize(self.root)
        self.assertEqual(created, 1)
        self.assertEqual(preserved, len(TEMPLATE_FILES) - 2)
        self.assertEqual(profile.read_text(encoding="utf-8"), "Synthetic private profile")
        self.assertEqual(missing.read_bytes(), (self.root / "templates/workspace/schedule/current.md").read_bytes())

    def test_build_is_reproducible_and_never_packages_private_records(self):
        baseline = render_outputs(self.root)
        initialize(self.root)
        canary = b"PRIVATE_CANARY_f83e47_do_not_export"
        (self.root / "personal/profile/about-me.md").write_bytes(canary)
        (self.root / "chat-export.txt").write_bytes(canary)
        self.assertEqual(baseline, render_outputs(self.root))
        build(self.root)
        build(self.root, check=True)
        for name in GENERATED_FILES:
            self.assertNotIn(canary, (self.root / name).read_bytes())
        build(self.root)
        self.assertEqual(baseline, {name: (self.root / name).read_bytes() for name in GENERATED_FILES})

    def test_stale_or_contaminated_download_fails_without_rewriting(self):
        build(self.root)
        target = self.root / "starter/MY-TRAINER.md"
        target.write_text("Synthetic personal notebook accidentally saved publicly", encoding="utf-8")
        before = target.read_bytes()
        with self.assertRaisesRegex(ValueError, "stale"):
            build(self.root, check=True)
        self.assertEqual(before, target.read_bytes())

    def test_claude_zip_is_self_contained_and_uses_one_root_folder(self):
        outputs = render_outputs(self.root)
        with zipfile.ZipFile(io.BytesIO(outputs["starter/personal-training-coach.zip"])) as package:
            self.assertEqual(set(package.namelist()), {
                "personal-training-coach/SKILL.md",
                "personal-training-coach/references/COACH-HANDBOOK.md",
                "personal-training-coach/references/RESEARCH-LIBRARY.md",
                "personal-training-coach/assets/MY-TRAINER.md",
                "personal-training-coach/LICENSE",
            } | {"personal-training-coach/" + name for name in ANALYSIS_TOOLS})
            self.assertEqual(package.read("personal-training-coach/references/COACH-HANDBOOK.md"),
                             outputs["starter/COACH-HANDBOOK.md"])
            self.assertEqual(package.read("personal-training-coach/assets/MY-TRAINER.md"),
                             outputs["starter/MY-TRAINER.md"])
            entry = package.read("personal-training-coach/SKILL.md").decode("utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", entry):
                self.assertIn("personal-training-coach/" + target, package.namelist())

    def test_claude_code_tree_matches_the_portable_skill(self):
        outputs = render_outputs(self.root)
        with zipfile.ZipFile(io.BytesIO(outputs["starter/personal-training-coach.zip"])) as package:
            for name in package.namelist():
                self.assertEqual(outputs[".claude/skills/" + name], package.read(name))
        project_file = outputs["starter/CLAUDE.md"]
        self.assertIn(outputs["starter/PROJECT-INSTRUCTIONS.txt"].rstrip(), project_file)
        self.assertIn(outputs["starter/COACH-HANDBOOK.md"], project_file)

    def test_agent_jsonl_is_complete_valid_and_explicit_about_usage(self):
        outputs = render_outputs(self.root)
        self.assertEqual(outputs["agent.jsonl"], outputs["starter/agent.jsonl"])
        records = [json.loads(line) for line in outputs["agent.jsonl"].decode("utf-8").splitlines()]
        self.assertEqual(records[0]["schema"], "personal-trainer-agent-bundle/v1")
        self.assertEqual(records[0]["type"], "bundle")
        self.assertIn("not an automatically discovered", records[0]["usage"])
        self.assertEqual(records[1]["type"], "project_instructions")
        self.assertEqual(records[1]["content"],
                         outputs["starter/PROJECT-INSTRUCTIONS.txt"].decode("utf-8").strip())
        documents = [record for record in records if record["type"] == "document"]
        expected = tuple(f"skills/{name}/SKILL.md" for name in SKILLS)
        expected += REFERENCE_FILES + RESEARCH_FILES + PROMPT_FILES
        self.assertEqual(tuple(record["source_path"] for record in documents), expected)
        self.assertEqual(records[0]["document_count"], len(documents))

    def test_handbook_links_do_not_require_repository_files(self):
        handbook = render_outputs(self.root)["starter/COACH-HANDBOOK.md"].decode("utf-8")
        anchors = set(re.findall(r'<a id="([^"]+)">', handbook))
        expected = set(SKILLS) | {document_anchor(name) for name in REFERENCE_FILES + RESEARCH_FILES + PROMPT_FILES}
        self.assertEqual(anchors, expected)
        for target in re.findall(r"\]\(([^)]+)\)", handbook):
            if target.startswith(("https://", "http://")):
                continue
            self.assertTrue(target.startswith("#"), target)
            self.assertIn(target[1:], anchors)

    def test_russian_bundles_preserve_every_shared_workflow_and_research_source(self):
        outputs = render_outputs(self.root)
        def schema_lines(name):
            return [line for line in outputs[name].decode().splitlines()
                    if line.startswith(("## ", "### ", "|"))]
        self.assertEqual(schema_lines("starter/MY-TRAINER.md"), schema_lines("starter/ru/MY-TRAINER.md"))
        self.assertTrue(outputs["starter/ru/COACH-HANDBOOK.md"].endswith(outputs["starter/COACH-HANDBOOK.md"]))
        for folder in ("starter", "starter/ru"):
            self.assertEqual(outputs[f"{folder}/COACH-HANDBOOK.md"], outputs[f"{folder}/COACH-HANDBOOK.txt"])
        self.assertEqual(outputs["starter/RESEARCH-LIBRARY.md"], outputs["starter/ru/RESEARCH-LIBRARY.md"])
        english = [json.loads(line) for line in outputs["starter/agent.jsonl"].decode().splitlines()]
        russian = [json.loads(line) for line in outputs["starter/ru/agent.jsonl"].decode().splitlines()]
        self.assertEqual(russian[0]["language"], "ru")
        self.assertEqual(english[2:], russian[2:])
        self.assertEqual(russian[1]["content"], outputs["starter/ru/PROJECT-INSTRUCTIONS.txt"].decode().strip())
        self.assertIn(outputs["starter/ru/PROJECT-INSTRUCTIONS.txt"].rstrip(), outputs["starter/ru/CLAUDE.md"])
        self.assertIn(outputs["starter/ru/COACH-HANDBOOK.md"], outputs["starter/ru/CLAUDE.md"])

    def test_translation_review_detects_edits_on_either_side(self):
        names = [name for pair in TRANSLATION_PAIRS for name in pair] + ["docs/translation-review.json"]
        for name in names:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        self.assertEqual(check_translation_review(self.root), [])
        for name in TRANSLATION_PAIRS[0]:
            target = self.root / name
            original = target.read_bytes()
            target.write_bytes(original + b"\nChanged instruction requiring review.\n")
            self.assertTrue(any(name in issue for issue in check_translation_review(self.root)))
            target.write_bytes(original)

    def test_research_download_links_resolve_to_itself_or_handbook(self):
        outputs = render_outputs(self.root)
        library = outputs["starter/RESEARCH-LIBRARY.md"].decode("utf-8")
        handbook = outputs["starter/COACH-HANDBOOK.md"].decode("utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", library):
            if target.startswith(("http://", "https://")):
                continue
            document, anchor = target.split("#", 1)
            self.assertIn(document, ("", "COACH-HANDBOOK.md"))
            self.assertIn(f'id="{anchor}"', handbook if document else library)

    def test_git_ignores_private_records_and_checker_catches_force_added_record(self):
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True, capture_output=True)
        initialize(self.root)
        private_name = "personal/profile/about-me.md"
        self.assertNotIn(private_name, visible_files(self.root))
        subprocess.run(["git", "add", "--force", private_name], cwd=self.root, check=True, capture_output=True)
        names = visible_files(self.root)
        self.assertIn(private_name, names)
        self.assertTrue(any(private_name in error for error in check_files(self.root, names)))

    def test_checker_reports_patterns_without_echoing_sensitive_values(self):
        target = self.root / "README.md"
        synthetic = "person" + "@" + "example.invalid"
        target.write_text(synthetic, encoding="utf-8")
        issues = check_files(self.root, ["README.md"])
        self.assertTrue(any("email address" in issue for issue in issues))
        self.assertNotIn(synthetic, "\n".join(issues))

    def test_linked_source_is_rejected(self):
        source = self.root / "templates/MY-TRAINER.md"
        secret = self.root / "private-source.txt"
        secret.write_text("PRIVATE CANARY", encoding="utf-8")
        source.unlink()
        try:
            source.symlink_to(secret)
        except OSError:
            self.skipTest("Creating symlinks is not available for this account")
        with self.assertRaisesRegex(ValueError, "Linked paths"):
            render_outputs(self.root)

    def test_linked_private_destination_is_rejected(self):
        actual = self.root / "elsewhere"
        actual.mkdir()
        try:
            (self.root / "personal").symlink_to(actual, target_is_directory=True)
        except OSError:
            self.skipTest("Creating symlinks is not available for this account")
        with self.assertRaisesRegex(ValueError, "Linked paths"):
            initialize(self.root)
        self.assertEqual(list(actual.iterdir()), [])

    def test_public_markdown_links_resolve(self):
        for name in PUBLIC_FILES:
            if not name.endswith(".md"):
                continue
            path = ROOT / name
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if target.startswith(("https://", "http://", "#")):
                    continue
                self.assertTrue((path.parent / target.split("#")[0]).is_file(), (name, target))


if __name__ == "__main__":
    unittest.main()
