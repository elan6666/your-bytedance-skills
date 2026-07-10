import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "byte-do" / "scripts" / "byte_state.py"
SPEC = importlib.util.spec_from_file_location("byte_state", SCRIPT)
byte_state = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(byte_state)


class ByteStateTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, relative, content, mtime=None):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        if mtime is not None:
            os.utime(path, (mtime, mtime))
        return path

    def add_specs(self):
        for name in ["PRODUCT_SPEC.md", "UX_SPEC.md", "TECH_SPEC.md"]:
            self.write(f".byte-os/{name}", "# Spec\n")

    def add_complete_plan(self, mtime=10):
        self.write(
            ".byte-os/plans/001-core.plan.md",
            "---\nid: 001\nstatus: complete\nwave: 1\n---\n# Plan\n",
            mtime,
        )

    def next(self):
        return byte_state.next_workflow(byte_state.scan(self.root))[0]

    def test_missing_state_starts_project(self):
        self.assertEqual(self.next(), "byte-start")

    def test_existing_codebase_requires_harness_before_shape(self):
        self.write(
            ".byte-os/STATUS.md",
            "---\nschema_version: 1\nproject_kind: existing_codebase\n---\n",
        )
        self.assertEqual(self.next(), "byte-codebase-harness")

    def test_complete_existing_codebase_harness_allows_shape(self):
        self.write(
            ".byte-os/STATUS.md",
            "---\nschema_version: 1\nproject_kind: existing_codebase\n---\n",
        )
        for name in ["CODEBASE_MAP.md", "HARNESS.md", "AGENTS_AUDIT.md"]:
            self.write(f".byte-os/{name}", "# Ready\n")
        self.assertEqual(self.next(), "byte-shape")

    def test_git_directory_alone_does_not_force_harness(self):
        (self.root / ".git").mkdir()
        self.write(".byte-os/STATUS.md", "Stage: started\n")
        self.assertEqual(self.next(), "byte-shape")

    def test_legacy_partial_harness_routes_to_harness(self):
        self.write(".byte-os/STATUS.md", "Stage: started\nHarness: partial\n")
        self.assertEqual(self.next(), "byte-codebase-harness")

    def test_stale_ready_harness_without_artifacts_routes_to_repair(self):
        self.write(".byte-os/STATUS.md", "Stage: started\nHarness: ready\n")
        self.assertEqual(self.next(), "byte-codebase-harness")

    def test_hard_blocker_reports_status_instead_of_retrying(self):
        self.write(
            ".byte-os/STATUS.md",
            "---\nschema_version: 1\nstage: blocked\nhard_blocked: true\n---\n",
        )
        self.assertEqual(self.next(), "byte-status")

    def test_incomplete_plan_routes_to_build(self):
        self.write(".byte-os/STATUS.md", "Stage: planned\n")
        self.add_specs()
        self.write(
            ".byte-os/plans/001-core.plan.md",
            "---\nid: 001\nstatus: pending\n---\n",
        )
        self.assertEqual(self.next(), "byte-build")

    def test_brainstorm_without_discussion_routes_to_discuss(self):
        self.write(".byte-os/STATUS.md", "Stage: started\n")
        self.write(".byte-os/BRAINSTORM.md", "# Directions\n")
        self.assertEqual(self.next(), "byte-discuss")

    def test_discussion_without_specs_routes_to_shape(self):
        self.write(".byte-os/STATUS.md", "Stage: discussing\n")
        self.write(".byte-os/DISCUSSION.md", "# Confirmed\n")
        self.assertEqual(self.next(), "byte-shape")

    def test_iteration_newer_than_blocking_review_routes_to_review(self):
        self.write(".byte-os/STATUS.md", "Stage: iterating\n")
        self.add_specs()
        self.add_complete_plan(mtime=10)
        self.write(
            ".byte-os/reviews/review-1.md",
            "# Verdict\nblock\n",
            mtime=20,
        )
        self.write(
            ".byte-os/iterations/iteration-1.md",
            "# Changes made\nFixed the blocker.\n",
            mtime=30,
        )
        self.assertEqual(self.next(), "byte-review")

    def test_current_blocking_review_routes_to_iteration(self):
        self.write(".byte-os/STATUS.md", "Stage: reviewed\n")
        self.add_specs()
        self.add_complete_plan(mtime=10)
        self.write(
            ".byte-os/reviews/review-1.md",
            "# Verdict\niterate\n",
            mtime=20,
        )
        self.assertEqual(self.next(), "byte-iterate")

    def test_completed_plan_newer_than_review_requires_fresh_review(self):
        self.write(".byte-os/STATUS.md", "Stage: building\n")
        self.add_specs()
        self.write(
            ".byte-os/reviews/review-1.md",
            "# Verdict\nship\n",
            mtime=20,
        )
        self.add_complete_plan(mtime=30)
        self.assertEqual(self.next(), "byte-review")

    def test_ship_review_routes_to_delivery_then_status(self):
        self.write(".byte-os/STATUS.md", "Stage: reviewed\n")
        self.add_specs()
        self.add_complete_plan(mtime=10)
        self.write(
            ".byte-os/reviews/review-1.md",
            "# Verdict\nship\n",
            mtime=20,
        )
        self.assertEqual(self.next(), "byte-deliver")
        self.write(".byte-os/DELIVERY.md", "# Delivery\n")
        self.assertEqual(self.next(), "byte-status")

    def test_update_adds_schema_without_losing_body(self):
        self.write(".byte-os/STATUS.md", "# Status\n\nStage: started\n")
        byte_state.update(self.root, ["stage=shaped", "next_workflow=byte-plan"])
        text = (self.root / ".byte-os/STATUS.md").read_text(encoding="utf-8")
        self.assertIn("schema_version: 1", text)
        self.assertIn("stage: shaped", text)
        self.assertIn("# Status", text)

    def test_validate_rejects_unknown_plan_status(self):
        self.write(".byte-os/STATUS.md", "---\nschema_version: 1\n---\n")
        self.write(
            ".byte-os/plans/001-core.plan.md",
            "---\nid: 001\nstatus: done\n---\n",
        )
        result = byte_state.validate(byte_state.scan(self.root))
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("Invalid plan status", result["errors"][0])

    def test_validate_rejects_invalid_status_enum(self):
        self.write(
            ".byte-os/STATUS.md",
            "---\nschema_version: 1\nproject_kind: legacy\n---\n",
        )
        result = byte_state.validate(byte_state.scan(self.root))
        self.assertIn("Invalid project_kind value: 'legacy'", result["errors"])


if __name__ == "__main__":
    unittest.main()
