#!/usr/bin/env python3
"""Install the factory into a clean git repo, or verify this repo.

--dest PATH   assemble CORE + identity templates, then copy this blueprint tree
              (catalog, capabilities, templates, bins, rules).
no args       verify this repo contains the catalog + bins.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


BLUEPRINT = Path(__file__).resolve().parent.parent
ROOT = BLUEPRINT.parents[1]
ASSEMBLE = ROOT / "workflow" / "harvest" / "pack" / "assemble.py"
COPY_NAMES = (
    "README.md",
    "ARCHITECTURE.md",
    "CAPABILITY-CATALOG.md",
    "EXTRACT-LOG.md",
    "PLAN.md",
    "bin",
    "capabilities",
    "rules",
    "templates",
)


def run(args) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True)


def ignore(directory, names):
    return [n for n in names if n in {".git", "__pycache__", ".pytest_cache"} or n.endswith(".pyc")]


def copy_blueprint(dest: Path) -> list[str]:
    copied = []
    target = dest / "workflow" / "blueprint"
    target.mkdir(parents=True, exist_ok=True)
    for name in COPY_NAMES:
        source = BLUEPRINT / name
        if not source.exists():
            raise RuntimeError(f"blueprint source missing: {name}")
        destination = target / name
        if source.is_dir():
            if destination.exists():
                shutil.copytree(source, destination, dirs_exist_ok=True, ignore=ignore)
            else:
                shutil.copytree(source, destination, ignore=ignore)
        else:
            shutil.copy2(source, destination)
        copied.append("workflow/blueprint/" + name)
    return copied


def verify_here() -> list[str]:
    errors = []
    for name in COPY_NAMES:
        if not (BLUEPRINT / name).exists():
            errors.append(f"missing workflow/blueprint/{name}")
    if not ASSEMBLE.exists():
        errors.append("harvest assemble.py missing")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest", type=Path, default=None)
    parser.add_argument("--extra", default="", help="passed through to assemble.py")
    parser.add_argument("--candidate", action="store_true", help="copy IDEAS + UNIV extracts")
    args = parser.parse_args(argv)
    if args.dest is None:
        errors = verify_here()
        if errors:
            for item in errors:
                print("ERROR   " + item)
            return 1
        print("BOOTSTRAP CHECK PASSED — this repo has the factory tree")
        print("install: python workflow/blueprint/bin/bootstrap.py --dest <clean-git>")
        return 0
    dest = args.dest.resolve()
    assemble_cmd = [sys.executable, str(ASSEMBLE), "--dest", str(dest)]
    if args.extra:
        assemble_cmd.extend(["--extra", args.extra])
    if args.candidate:
        assemble_cmd.append("--candidate")
    result = run(assemble_cmd)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    if result.returncode != 0:
        return result.returncode
    try:
        copied = copy_blueprint(dest)
    except (OSError, RuntimeError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    print("blueprint copied:")
    for rel in copied:
        print("  " + rel)
    print("NEXT in dest: fill START-HERE four lines, then python workflow/blueprint/bin/orient.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
