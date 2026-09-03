"""evidence_kernel -- validate SEED evidence records against the schema/ contract.

One implementation, two doors. ``scripts/schema_check.py`` (the repo's CI check) and the
``evidence-kernel`` console script both call into this module; neither carries its own copy of
the parser or the validator.

The validator is dependency-free and deliberately small: it implements only the JSON Schema
2020-12 keywords the schemas use (type, enum, const, pattern, minLength, not, properties,
required, additionalProperties, allOf, if/then, $ref to #/$defs and to sibling files).
An unknown keyword is an error, not a silent skip (Law 2: a check that ignores what it does
not understand would stay green on a broken schema).

Public API::

    validate(record_type, text) -> list[str]   # "receipt" | "dispatch" | "experiment" | "handoff"
"""
import json
import re
from pathlib import Path

__version__ = "0.1.0"

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
RECORD_TYPES = ("receipt", "dispatch", "experiment", "handoff")
KERNEL_NAME = "evidence-kernel.schema.json"
BUNDLED_SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"
SCHEMA_FILES = tuple(f"{name}.schema.json" for name in RECORD_TYPES) + (KERNEL_NAME,)


# --- parsing: identical to scripts/onboard_check.py -----------------------------------------

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


def parse_record(schema_name, body):
    """Turn record text into the instance shape its schema describes."""
    if schema_name == "handoff.schema.json":
        return parse_handoff(body)
    return normalize_record(parse_fields(body))


# --- validator -----------------------------------------------------------------------------

class Validator:
    def __init__(self, schema_dir=None):
        self.schema_dir = Path(schema_dir) if schema_dir else BUNDLED_SCHEMA_DIR
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

    def validate_text(self, schema_name, body):
        instance = parse_record(schema_name, body)
        return self.validate(instance, self.load(schema_name), schema_name)

    def record_directories(self):
        """Directory -> schema file name, as declared by the kernel."""
        records = self.load(KERNEL_NAME)["properties"]["records"]["properties"]
        return {directory: ref["$ref"] for directory, ref in records.items()}


def validate(record_type, text, schema_dir=None):
    """Validate one record's text. Returns a list of error strings; empty means it conforms."""
    if record_type not in RECORD_TYPES:
        raise ValueError(f"unknown record type {record_type!r}; expected one of {RECORD_TYPES}")
    return Validator(schema_dir).validate_text(f"{record_type}.schema.json", text)


def check_tree(root, schema_dir=None):
    """Validate every banked record under ``root`` per the kernel's directory map.

    Returns (messages, counted, record_map). Messages use the exact
    ``ERROR   <dir>/<file> [<schema>] <detail>`` form scripts/schema_check.py prints.
    """
    root = Path(root)
    validator = Validator(schema_dir)
    records = validator.record_directories()
    msgs = []
    counted = 0
    for directory, schema_name in sorted(records.items()):
        folder = root / directory
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md")):
            body = path.read_text(encoding="utf-8", errors="replace")
            counted += 1
            for err in validator.validate_text(schema_name, body):
                msgs.append(f"ERROR   {directory}/{path.name} [{schema_name}] {err}")
    return msgs, counted, records


__all__ = [
    "BUNDLED_SCHEMA_DIR", "HANDOFF_HEADINGS", "KERNEL_NAME", "RECORD_TYPES", "SCHEMA_FILES",
    "SUPPORTED_KEYWORDS", "Validator", "check_tree", "normalize_record", "parse_fields",
    "parse_handoff", "parse_record", "validate", "__version__",
]
