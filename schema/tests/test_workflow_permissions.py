"""The verify workflow must not inherit a write-capable GITHUB_TOKEN."""
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "verify.yml"


class WorkflowPermissionsTest(unittest.TestCase):
    def test_verify_workflow_contents_are_read_only(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read\n", text)
        self.assertNotIn("contents: write", text)


if __name__ == "__main__":
    unittest.main()
