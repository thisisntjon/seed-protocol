#!/usr/bin/env python3
"""Validate every banked evidence record against schema/*.schema.json.

schema/evidence-kernel.schema.json maps each record directory to its schema. Every *.md file
directly under workflow/receipts, workflow/dispatches, workflow/experiments, and
workflow/handoffs is parsed exactly as scripts/onboard_check.py parses it (FIELD: value lines
for records; first line + '## ' headings for handoffs) and validated against the schema.

The parser and validator live in the installable package schema/evidence_kernel (one
implementation; `pip install ./schema` gives the same code as the `evidence-kernel` console
script). This script is the repo-specific driver: it points the validator at this tree's
schema/ directory, refuses to run if the kernel's closed vocabularies drift from the checker's
constants, and refuses if the package's bundled schema copies drift from schema/.
Exit 0 means every record satisfies the machine form of its template. ASCII output only.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "schema"))
from evidence_kernel import (  # noqa: E402
    BUNDLED_SCHEMA_DIR, HANDOFF_HEADINGS, KERNEL_NAME, SCHEMA_FILES, SUPPORTED_KEYWORDS,
    Validator, check_tree, normalize_record, parse_fields, parse_handoff,
)

__all__ = [
    "HANDOFF_HEADINGS", "SUPPORTED_KEYWORDS", "Validator",
    "normalize_record", "parse_fields", "parse_handoff", "main",
]


# --- driver --------------------------------------------------------------------------------

def check_vocabularies(root, kernel, msgs):
    sys.path.insert(0, str(root / "scripts"))
    try:
        import onboard_check  # noqa: E402
    except Exception as exc:  # pragma: no cover
        msgs.append(f"ERROR   cannot import scripts/onboard_check.py: {exc}")
        return
    expected = {
        "STATE": onboard_check.RECEIPT_STATES,
        "PROGRESS": onboard_check.PROGRESS_KINDS,
        "OUTCOME": onboard_check.EXPERIMENT_OUTCOMES,
    }
    vocab = kernel.get("properties", {}).get("vocabularies", {}).get("properties", {})
    for name, tokens in expected.items():
        declared = set(vocab.get(name, {}).get("const", []))
        if declared != set(tokens):
            msgs.append(
                f"ERROR   kernel vocabulary {name} {sorted(declared)} != checker {sorted(tokens)}"
            )


def _load(path):
    """Parsed comparison: line endings differ across autocrlf checkouts, content must not."""
    return json.loads(path.read_text(encoding="utf-8"))


def check_bundled_copies(schema_dir, msgs):
    """The package ships copies of schema/*.schema.json; a silent fork would be two contracts."""
    for name in SCHEMA_FILES:
        bundled = BUNDLED_SCHEMA_DIR / name
        source = schema_dir / name
        if not bundled.exists():
            msgs.append(f"ERROR   schema/evidence_kernel/schemas/{name} missing -- package copy of the schema")
        elif source.exists() and _load(bundled) != _load(source):
            msgs.append(f"ERROR   schema/evidence_kernel/schemas/{name} differs from schema/{name} -- copy it again")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None, help="repo root (default: parent of this script)")
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    schema_dir = root / "schema"
    msgs = []
    kernel_path = schema_dir / KERNEL_NAME
    if not kernel_path.exists():
        print("ERROR   schema/evidence-kernel.schema.json missing")
        print("\nSCHEMA CHECK FAILED")
        return 1
    validator = Validator(schema_dir)
    kernel = validator.load(KERNEL_NAME)
    check_vocabularies(root, kernel, msgs)
    check_bundled_copies(schema_dir, msgs)

    record_msgs, counted, records = check_tree(root, schema_dir)
    msgs += record_msgs

    for msg in msgs:
        print(msg)
    errors = [m for m in msgs if m.startswith("ERROR")]
    verdict = "SCHEMA CHECK PASSED" if not errors else "SCHEMA CHECK FAILED -- a record does not match its schema"
    print(f"\n{counted} record(s) validated against {len(records)} schema(s); {len(errors)} error(s). {verdict}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
