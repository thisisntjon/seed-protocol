#!/usr/bin/env python3
"""Validate and materialize the SEED factory pack.

--check   MANIFEST vs disk vs transplant.PORTABLE_FILES. Default if no --dest.
--dest    copy CORE + identity templates into a clean git repo (greenfield).
--extra   comma list of optional extras (comms,ops,poc,ci,canon,pack).
--candidate  also copy UNIV-RULES.md and TOOL-REBUILD.md into dest/workflow/factory/.

Does not grow scripts/transplant.py PORTABLE_FILES. Existing projects should keep
using transplant.py. This assembler is the greenfield path plus the pack integrity check.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


PACK = Path(__file__).resolve().parent
# assemble.py lives at workflow/harvest/pack/; repo root is parents[2] of PACK.
ROOT = PACK.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import transplant  # noqa: E402

MANIFEST_PATH = PACK / "MANIFEST.json"
INVENTORY_PATH = PACK.parent / "INVENTORY.json"
VALID_CLASSES = {"CORE", "OPTIONAL", "IDENTITY", "CANDIDATE", "NEVER"}
EMPTY_DIRS = (
    "workflow/dispatches",
    "workflow/experiments",
    "workflow/receipts",
    "workflow/handoffs",
)
IGNORE_DIR_NAMES = {".git", "__pycache__", ".pytest_cache"}


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def load_inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def flatten_optional(manifest: dict) -> list[str]:
    paths = []
    for extra, items in manifest.get("optional", {}).items():
        if not isinstance(items, list):
            raise RuntimeError(f"optional.{extra} must be a list")
        paths.extend(items)
    return paths


def _ignore(directory, names):
    return [n for n in names if n in IGNORE_DIR_NAMES or n.endswith(".pyc")]


def copy_path(source: Path, destination: Path) -> None:
    if source.is_dir():
        if destination.exists():
            shutil.copytree(source, destination, dirs_exist_ok=True, ignore=_ignore)
        else:
            shutil.copytree(source, destination, ignore=_ignore)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def check(manifest: dict, inventory: dict) -> list[str]:
    errors = []
    core = list(manifest.get("core") or [])
    portable = list(transplant.PORTABLE_FILES)
    if core != portable:
        errors.append(
            "MANIFEST core does not match transplant.PORTABLE_FILES: "
            f"manifest={core} portable={portable}"
        )
    never = list(manifest.get("never") or [])
    optional_paths = flatten_optional(manifest)
    identity_src = list((manifest.get("identity_templates") or {}).keys())
    identity_dst = list((manifest.get("identity_templates") or {}).values())
    candidate_docs = list(manifest.get("candidate_docs") or [])

    def must_exist(rel: str, bucket: str) -> None:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"{bucket} path missing: {rel}")

    for rel in core:
        must_exist(rel, "core")
        if rel in never or rel.rstrip("/") + "/" in never:
            errors.append(f"NEVER path listed in core: {rel}")
    for rel in optional_paths:
        must_exist(rel, "optional")
        never_hit = rel in never or any(
            rel.rstrip("/").startswith(n.rstrip("/")) for n in never
        )
        if never_hit:
            errors.append(f"NEVER path listed in optional: {rel}")
    for rel in identity_src + candidate_docs:
        must_exist(rel, "pack")
    live_identity = list(manifest.get("identity_never_copy_from_live_repo") or [])
    for rel in live_identity:
        if rel in core or rel in optional_paths:
            errors.append(f"live identity listed for copy: {rel}")

    extras = set((manifest.get("optional") or {}).keys())
    rows = inventory.get("rows") or []
    classes = {}
    for row in rows:
        klass = row.get("class")
        if klass not in VALID_CLASSES:
            errors.append(f"inventory {row.get('id')} has invalid class {klass!r}")
        classes[klass] = classes.get(klass, 0) + 1
        extra = row.get("extra")
        if klass == "OPTIONAL" and extra and extra not in extras:
            errors.append(f"inventory {row.get('id')} extra {extra!r} not in MANIFEST optional")
    claimed = inventory.get("counts") or {}
    for klass, n in classes.items():
        if claimed.get(klass) not in (None, n):
            errors.append(f"inventory counts.{klass}={claimed.get(klass)} but rows={n}")
    for klass, n in claimed.items():
        if klass not in classes:
            errors.append(f"inventory counts.{klass}={n} but no rows")
    return errors


def apply_dest(manifest: dict, dest: Path, extras: list[str], candidate: bool) -> dict:
    valid, reason = transplant.target_is_clean_git(dest)
    if not valid:
        raise RuntimeError(reason)
    copied = []
    skipped = []
    conflicts = []

    def place(source: Path, destination: Path, rel_out: str) -> None:
        if not source.exists():
            raise RuntimeError(f"source missing: {source}")
        if destination.exists():
            if source.is_file() and destination.is_file() and sha256(source) == sha256(destination):
                skipped.append(rel_out)
                return
            if source.is_dir() and destination.is_dir():
                skipped.append(rel_out + "/")
                return
            conflicts.append(rel_out)
            return
        copy_path(source, destination)
        copied.append(rel_out)

    for rel in manifest["core"]:
        place(ROOT / rel, dest / rel, rel)
    for src_rel, dst_rel in manifest["identity_templates"].items():
        place(ROOT / src_rel, dest / dst_rel, dst_rel)
    optional = manifest.get("optional") or {}
    unknown = [name for name in extras if name not in optional]
    if unknown:
        raise RuntimeError("unknown extra(s): " + ", ".join(unknown))
    for name in extras:
        if name == "canon":
            # Greenfield already wrote identity templates; skip duplicate.
            continue
        for rel in optional[name]:
            place(ROOT / rel, dest / rel, rel)
    if candidate:
        factory = dest / "workflow" / "factory"
        factory.mkdir(parents=True, exist_ok=True)
        for rel in manifest.get("candidate_docs") or []:
            place(ROOT / rel, factory / Path(rel).name, f"workflow/factory/{Path(rel).name}")
    for rel in EMPTY_DIRS:
        path = dest / rel
        path.mkdir(parents=True, exist_ok=True)
        keep = path / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
            copied.append(rel + "/.gitkeep")
    if conflicts:
        raise RuntimeError("refusing to overwrite differing target file(s): " + ", ".join(conflicts))
    provenance = {
        "schema_version": 1,
        "source_project": "Bonkers / SEED harvest pack",
        "source_commit": transplant.source_commit(),
        "copied": copied,
        "identical": skipped,
        "extras": extras,
        "candidate_docs": bool(candidate),
    }
    prov_path = dest / "workflow" / "SEED-PACK.json"
    prov_path.parent.mkdir(parents=True, exist_ok=True)
    prov_path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    copied.append("workflow/SEED-PACK.json")
    return provenance


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate MANIFEST and inventory")
    parser.add_argument("--dest", type=Path, help="greenfield git repo to materialize into")
    parser.add_argument("--extra", default="", help="comma list of optional extras")
    parser.add_argument("--candidate", action="store_true", help="copy UNIV-RULES and TOOL-REBUILD")
    args = parser.parse_args(argv)
    extras = [part.strip() for part in args.extra.split(",") if part.strip()]
    manifest = load_manifest()
    inventory = load_inventory()
    want_check = args.check or args.dest is None
    if want_check:
        errors = check(manifest, inventory)
        if errors:
            for item in errors:
                print("ERROR   " + item)
            print(f"PACK CHECK FAILED ({len(errors)})")
            return 1
        print("PACK CHECK PASSED")
        print(f"  core={len(manifest['core'])} extras={list(manifest['optional'])} "
              f"identity_templates={len(manifest['identity_templates'])}")
        counts = inventory.get("counts") or {}
        print("  inventory " + " ".join(f"{k}={v}" for k, v in counts.items()))
        if args.dest is None:
            return 0
    try:
        result = apply_dest(manifest, args.dest.resolve(), extras, args.candidate)
    except (OSError, RuntimeError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
