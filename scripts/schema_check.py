#!/usr/bin/env python3
"""Validate every banked evidence record against schema/*.schema.json.

schema/evidence-kernel.schema.json maps each record directory to its schema. Every *.md file
directly under workflow/receipts, workflow/dispatches, workflow/experiments, and
workflow/handoffs is parsed exactly as scripts/onboard_check.py parses it (FIELD: value lines
for records; first line + '## ' headings for handoffs) and validated against the schema.

The validator is dependency-free and deliberately small: it implements only the JSON Schema
2020-12 keywords the schemas use (type, enum, const, pattern, minLength, not, properties,
required, additionalProperties, allOf, if/then, $ref to #/$defs and to sibling files).
An unknown keyword is an error, not a silent skip (Law 2: a check that ignores what it does
not understand would stay green on a broken schema).

It also refuses to run if the kernel's closed vocabularies drift from the checker's constants.
Exit 0 means every record satisfies the machine form of its template. ASCII output only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

SUPPORTED_KEYWORDS = {
    "$schema", "$id", "$defs", "$ref", "title", "version", "description",
    "type", "enum", "const", "pattern", "minLength", "not",
    "properties", "required", "additionalProperties", "allOf", "if", "then",
}
HANDOFF_HEADINGS = (
    "## THE WHOLE JOB, IN FOUR LINES",
    "## BINDING RULES RIGHT NOW",
    "## EVERY NUMBER WORTH CITING",
    "## OPEN QUESTIONS",
    "## WHAT NOT TO DO",
)


# --- parsing: identical to onboard_check ---------------------------------------------------

def parse_fields(body):
    fields = {}
    for line in body.splitlines():
        match = re.match(r"^([A-Z][A-Z0-9_]*):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def normalize_record(fields):
    """Apply the checker's case handling so the schema enums compare the same way it does."""
    out = dict(fields)
    for key in ("STATE", "PROGRESS"):
        if key in out:
            out[key] = out[key].upper()
    if "OUTCOME" in out and out["OUTCOME"]:
        parts = out["OUTCOME"].split(maxsplit=1)
        out["OUTCOME"] = parts[0].upper() + (" " + parts[1] if len(parts) > 1 else "")
    return out


def parse_handoff(body):
    lines = body.splitlines()
    sections = {}
    current = None
    for line in lines[1:]:
        if line.startswith("## "):
            current = line.strip()
            for canonical in HANDOFF_HEADINGS:
                if canonical in line:
                    current = canonical
                    break
            sections.setdefault(current, "")
        elif current is not None:
            sections[current] += line + "\n"
    return {"header": lines[0] if lines else "", "sections": sections}


# --- validator -----------------------------------------------------------------------------

class Validator:
    def __init__(self, schema_dir):
        self.schema_dir = schema_dir
        self.cache = {}

    def load(self, name):
        if name not in self.cache:
            self.cache[name] = json.loads((self.schema_dir / name).read_text(encoding="utf-8"))
        return self.cache[name]

    def resolve(self, ref, root_name):
        if ref.startswith("#/"):
            node = self.load(root_name)
            for part in ref[2:].split("/"):
                node = node[part]
            return node, root_name
        if "#" in ref:
            raise ValueError(f"unsupported $ref form: {ref}")
        return self.load(ref), ref

    def validate(self, instance, schema, root_name, path="$"):
        errors = []
        unknown = set(schema) - SUPPORTED_KEYWORDS
        if unknown:
            raise ValueError(f"schema {root_name} uses unsupported keyword(s): {sorted(unknown)}")
        if "$ref" in schema:
            target, target_root = self.resolve(schema["$ref"], root_name)
            errors += self.validate(instance, target, target_root, path)
        if "type" in schema:
            expected = schema["type"]
            ok = {
                "object": isinstance(instance, dict),
                "string": isinstance(instance, str),
                "array": isinstance(instance, list),
            }.get(expected)
            if ok is None:
                raise ValueError(f"schema {root_name} uses unsupported type {expected}")
            if not ok:
                errors.append(f"{path}: expected {expected}")
                return errors
        if "enum" in schema and instance not in schema["enum"]:
            errors.append(f"{path}: {instance!r} not in {schema['enum']}")
        if "const" in schema and instance != schema["const"]:
            errors.append(f"{path}: {instance!r} != {schema['const']!r}")
        if "pattern" in schema and isinstance(instance, str) and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: {instance[:60]!r} does not match /{schema['pattern']}/")
        if "minLength" in schema and isinstance(instance, str) and len(instance) < schema["minLength"]:
            errors.append(f"{path}: empty")
        if "not" in schema and not self.validate(instance, schema["not"], root_name, path):
            errors.append(f"{path}: {str(instance)[:60]!r} matches forbidden form {schema['not']}")
        if isinstance(instance, dict):
            for key in schema.get("required", []):
                if key not in instance:
                    errors.append(f"{path}: missing required field {key}")
            props = schema.get("properties", {})
            for key, sub in props.items():
                if key in instance:
                    errors += self.validate(instance[key], sub, root_name, f"{path}.{key}")
            if schema.get("additionalProperties") is False:
                for key in instance:
                    if key not in props:
                        errors.append(f"{path}: unexpected field {key}")
        for sub in schema.get("allOf", []):
            errors += self.validate(instance, sub, root_name, path)
        if "if" in schema:
            if not self.validate(instance, schema["if"], root_name, path) and "then" in schema:
                errors += self.validate(instance, schema["then"], root_name, path)
        return errors


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None, help="repo root (default: parent of this script)")
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    schema_dir = root / "schema"
    msgs = []
    kernel_path = schema_dir / "evidence-kernel.schema.json"
    if not kernel_path.exists():
        print("ERROR   schema/evidence-kernel.schema.json missing")
        print("\nSCHEMA CHECK FAILED")
        return 1
    validator = Validator(schema_dir)
    kernel = validator.load("evidence-kernel.schema.json")
    check_vocabularies(root, kernel, msgs)

    records = kernel["properties"]["records"]["properties"]
    counted = 0
    for directory, ref in sorted(records.items()):
        schema_name = ref["$ref"]
        folder = root / directory
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md")):
            body = path.read_text(encoding="utf-8", errors="replace")
            if schema_name == "handoff.schema.json":
                instance = parse_handoff(body)
            else:
                instance = normalize_record(parse_fields(body))
            errors = validator.validate(instance, validator.load(schema_name), schema_name)
            counted += 1
            for err in errors:
                msgs.append(f"ERROR   {directory}/{path.name} [{schema_name}] {err}")

    for msg in msgs:
        print(msg)
    errors = [m for m in msgs if m.startswith("ERROR")]
    verdict = "SCHEMA CHECK PASSED" if not errors else "SCHEMA CHECK FAILED -- a record does not match its schema"
    print(f"\n{counted} record(s) validated against {len(records)} schema(s); {len(errors)} error(s). {verdict}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
