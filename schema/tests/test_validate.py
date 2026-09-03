"""Smoke test for the evidence_kernel package (stdlib unittest, no third-party dependency).

Run from the repository root:  python -m unittest discover -s schema/tests
"""
import json
import sys
import unittest
from pathlib import Path

SCHEMA_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCHEMA_DIR))

import evidence_kernel  # noqa: E402
from evidence_kernel import BUNDLED_SCHEMA_DIR, SCHEMA_FILES, validate  # noqa: E402

GOOD_RECEIPT = """\
STATE: DONE
OBJECT: schema/evidence_kernel package
EXACT_REF: 9e34cbfb1673965ed26f407cce2e6663190f4a9e
EVIDENCE: schema/tests/test_validate.py
PROGRESS: INFRASTRUCTURE
EFFECT: the validator is pip-installable
NEXT_OWNER: principal
SESSION_ID: test
"""

BAD_RECEIPT = """\
STATE: FINISHED
OBJECT: <fill me in>
EXACT_REF: 9e34cbfb1673965ed26f407cce2e6663190f4a9e
PROGRESS: INFRASTRUCTURE
EFFECT: none
NEXT_OWNER: principal
"""


class ValidateTest(unittest.TestCase):
    def test_good_receipt_has_no_errors(self):
        self.assertEqual(validate("receipt", GOOD_RECEIPT), [])

    def test_bad_receipt_is_rejected(self):
        errors = validate("receipt", BAD_RECEIPT)
        joined = "\n".join(errors)
        self.assertIn("missing required field EVIDENCE", joined)
        self.assertIn("'FINISHED' not in", joined)
        self.assertIn("<fill me in>", joined)

    def test_unknown_record_type_raises(self):
        with self.assertRaises(ValueError):
            validate("invoice", GOOD_RECEIPT)

    def test_bundled_schemas_match_repo_copies(self):
        """The package bundles copies of schema/*.schema.json; they must not drift."""
        for name in SCHEMA_FILES:
            repo = json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))
            bundled = json.loads((BUNDLED_SCHEMA_DIR / name).read_text(encoding="utf-8"))
            self.assertEqual(repo, bundled, f"{name}: bundled copy differs from schema/{name}")

    def test_version_matches_kernel(self):
        kernel = json.loads((SCHEMA_DIR / "evidence-kernel.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(evidence_kernel.__version__, kernel["version"])


if __name__ == "__main__":
    unittest.main()
