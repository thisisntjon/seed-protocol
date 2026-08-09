#!/usr/bin/env python3
"""Install SEED's portable core into an existing local git repository.

Project identity files (README, START-HERE, AGENTS, PLAN, GATES, CLAIMS, retractions) are
deliberately not copied: they must tell the truth about the target. This tool copies only the
invariant protocol implementation and templates, refuses every differing destination before it
writes, and records source identity plus per-file hashes in workflow/SEED-TRANSPLANT.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PORTABLE_FILES = (
    "LAWS.md",
    "scripts/onboard_check.py",
    "scripts/sabotage_test.py",
    "scripts/status.py",
    "scripts/checkpoint.py",
    "scripts/transplant.py",
    "workflow/templates/DISPATCH.md",
    "workflow/templates/RECEIPT.md",
    "workflow/templates/HANDOFF.md",
    "workflow/templates/EXPERIMENT.md",
)
PROVENANCE_PATH = Path("workflow/SEED-TRANSPLANT.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_commit() -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("SEED source has no git identity")
    return result.stdout.strip()


def target_is_clean_git(target: Path) -> tuple[bool, str]:
    if not (target / ".git").exists():
        return False, "target must be an existing standalone git repository"
    result = subprocess.run(
        ["git", "-C", str(target), "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False, "target git status failed"
    if result.stdout.strip():
        return False, "target working tree must be clean before transplant"
    return True, ""


def plan(target: Path) -> dict[str, object]:
    copied = []
    identical = []
    conflicts = []
    files = []
    for relative in PORTABLE_FILES:
        source = ROOT / relative
        destination = target / relative
        if not source.exists():
            raise RuntimeError(f"portable source missing: {relative}")
        digest = sha256(source)
        files.append({"path": relative, "sha256": digest})
        if not destination.exists():
            copied.append(relative)
        elif destination.is_file() and sha256(destination) == digest:
            identical.append(relative)
        else:
            conflicts.append(relative)
    identity_payload = "\n".join(
        f"{item['path']}:{item['sha256']}" for item in sorted(files, key=lambda item: item["path"])
    )
    portable_identity = hashlib.sha256(identity_payload.encode("utf-8")).hexdigest()
    return {
        "source_commit": source_commit(),
        "portable_identity_sha256": portable_identity,
        "target": str(target),
        "would_copy": copied,
        "identical": identical,
        "conflicts": conflicts,
        "files": files,
    }


def apply_transplant(target: Path, transplant_plan: dict[str, object]) -> None:
    conflicts = list(transplant_plan["conflicts"])
    if conflicts:
        raise RuntimeError("refusing to overwrite differing target file(s): " + ", ".join(conflicts))
    for relative in transplant_plan["would_copy"]:
        source = ROOT / str(relative)
        destination = target / str(relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    provenance = {
        "schema_version": 1,
        "source_project": "Bonkers / SEED",
        "source_commit": transplant_plan["source_commit"],
        "portable_identity_sha256": transplant_plan["portable_identity_sha256"],
        "installed_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "portable_files": transplant_plan["files"],
        "project_specific_files_required": [
            "START-HERE.md",
            "AGENTS.md",
            "GATES.md",
            "CLAIMS.md",
            "workflow/PLAN.md",
            "workflow/canon/RETRACTIONS.md",
        ],
    }
    destination = target / PROVENANCE_PATH
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--apply", action="store_true", help="write after a conflict-free preflight")
    args = parser.parse_args(argv)
    target = args.target.resolve()
    valid, reason = target_is_clean_git(target)
    if not valid:
        print(f"REFUSED: {reason}", file=sys.stderr)
        return 2
    try:
        transplant_plan = plan(target)
        if args.apply:
            apply_transplant(target, transplant_plan)
            transplant_plan["applied"] = True
        else:
            transplant_plan["applied"] = False
        print(json.dumps(transplant_plan, indent=2))
        return 0
    except (OSError, RuntimeError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
