"""Console script: ``evidence-kernel check <path...>``.

A path may be a record file or a directory of records. The record type is inferred from the
directory name (receipts, dispatches, experiments, handoffs) unless ``--type`` is given.
Exit 0 means every record matched its schema. ASCII output only.
"""
import argparse
import sys
from pathlib import Path

from . import RECORD_TYPES, Validator, __version__

DIRECTORY_TYPES = {
    "receipts": "receipt",
    "dispatches": "dispatch",
    "experiments": "experiment",
    "handoffs": "handoff",
}


def infer_type(path):
    for candidate in (path, path.parent):
        record_type = DIRECTORY_TYPES.get(candidate.name)
        if record_type:
            return record_type
    return None


def collect(paths):
    """Yield (path, record_type_or_None) for every record file named by ``paths``."""
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for child in sorted(path.glob("*.md")):
                yield child, infer_type(child)
        else:
            yield path, infer_type(path)


def run_check(paths, record_type=None, schema_dir=None):
    validator = Validator(schema_dir)
    msgs = []
    counted = 0
    for path, inferred in collect(paths):
        kind = record_type or inferred
        if not path.exists():
            msgs.append(f"ERROR   {path}: no such file")
            continue
        if kind is None:
            msgs.append(f"ERROR   {path}: cannot infer record type from its directory; pass --type")
            continue
        body = path.read_text(encoding="utf-8", errors="replace")
        counted += 1
        for err in validator.validate_text(f"{kind}.schema.json", body):
            msgs.append(f"ERROR   {path} [{kind}.schema.json] {err}")
    return msgs, counted


def main(argv=None):
    parser = argparse.ArgumentParser(prog="evidence-kernel")
    parser.add_argument("--version", action="version", version=f"evidence-kernel {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="validate record files or directories of records")
    check.add_argument("paths", nargs="+")
    check.add_argument("--type", choices=RECORD_TYPES, default=None,
                       help="record type for every path (default: infer from directory name)")
    check.add_argument("--schema-dir", default=None,
                       help="directory holding the *.schema.json files (default: bundled copies)")
    args = parser.parse_args(argv)

    msgs, counted = run_check(args.paths, args.type, args.schema_dir)
    for msg in msgs:
        print(msg)
    errors = [m for m in msgs if m.startswith("ERROR")]
    verdict = "SCHEMA CHECK PASSED" if not errors else "SCHEMA CHECK FAILED -- a record does not match its schema"
    print(f"\n{counted} record(s) validated; {len(errors)} error(s). {verdict}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
