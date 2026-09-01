#!/usr/bin/env python3
"""Prove the blueprint is not decorative.

Checks:
  catalog IDs have capability READMEs
  ENCODED ledger rows name existing check paths
  orient.py succeeds on this repo
  orient.py fails when START-HERE.md is missing (Law 2)
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


BLUEPRINT = Path(__file__).resolve().parent.parent
ROOT = BLUEPRINT.parents[1]
ORIENT = BLUEPRINT / "bin" / "orient.py"
CATALOG = BLUEPRINT / "CAPABILITY-CATALOG.md"
LEDGER = BLUEPRINT / "rules" / "LEDGER.md"


def run(args, cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, cwd=cwd)


def catalog_ids() -> list[str]:
    ids = []
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\|\s*(C\d+)\s*\|", line)
        if match:
            ids.append(match.group(1))
    return ids


def cap_dir(cid: str) -> Path:
    num = int(cid[1:])
    for path in (BLUEPRINT / "capabilities").iterdir():
        if path.is_dir() and path.name.startswith(f"{num:02d}-"):
            return path
    return BLUEPRINT / "capabilities" / f"{num:02d}"


def check_catalog() -> list[str]:
    errors = []
    ids = catalog_ids()
    if len(ids) < 10:
        errors.append(f"catalog too small ({len(ids)} rows)")
    for cid in ids:
        readme = cap_dir(cid) / "README.md"
        if not readme.exists():
            errors.append(f"{cid} missing {readme.relative_to(ROOT)}")
    return errors


def check_ledger() -> list[str]:
    errors = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| R"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        rid, _idea, enforcement, check, _sab = cells[:5]
        if enforcement != "ENCODED":
            continue
        for token in re.findall(r"`([^`]+)`", check):
            if " " in token or token.startswith("python"):
                continue
            path = ROOT / token
            if not path.exists():
                errors.append(f"{rid} ENCODED check missing: {token}")
    return errors


def check_orient_clean() -> list[str]:
    result = run([sys.executable, str(ORIENT), "--root", str(ROOT)])
    if result.returncode != 0:
        return [f"orient on clean repo failed: {result.stderr.strip()}"]
    if "NEXT:" not in result.stdout or "THE WHOLE JOB" not in result.stdout:
        return ["orient stdout missing NEXT: or THE WHOLE JOB"]
    return []


def check_orient_sabotage() -> list[str]:
    tmp = Path(tempfile.mkdtemp(prefix="orient-sabotage-"))
    try:
        (tmp / "README.md").write_text("not the front door\n", encoding="utf-8")
        result = run([sys.executable, str(ORIENT), "--root", str(tmp)])
        if result.returncode == 0:
            return ["orient stayed green with no START-HERE.md — guard is decorative"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    errors = []
    errors.extend(check_catalog())
    errors.extend(check_ledger())
    errors.extend(check_orient_clean())
    errors.extend(check_orient_sabotage())
    if errors:
        for item in errors:
            print("FAIL    " + item)
        print(f"\nBLUEPRINT SELFTEST FAILED ({len(errors)})")
        return 1
    print("PASS    catalog READMEs exist")
    print("PASS    ENCODED ledger paths exist")
    print("PASS    orient succeeds on this repo")
    print("PASS    orient fails without START-HERE.md")
    print("\nBLUEPRINT SELFTEST PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
