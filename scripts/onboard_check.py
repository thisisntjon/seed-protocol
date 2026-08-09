#!/usr/bin/env python3
"""Verify that SEED's documentation and workflow artifacts agree with reality.

Checks:
  1. PATHS       every concrete path claimed in START-HERE.md exists
  2. RETRACT     retracted tokens do not appear in project Markdown outside the ledger
  3. GATES       IDs/statuses/dates are valid and no human gate silently exceeds its SLA
  4. TEMPLATES   artifact templates still expose their required fields
  5. ARTIFACTS   receipts, dispatches, experiments, and handoffs match their schemas
  6. LAWS        every numbered law still names its evidence and enforcement grade

Exit 0 means these checks found no contradiction. It does not prove project success.
ASCII output only (Windows cp1252 console safety).
"""
import argparse
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

SLA_HOURS = 48

TEMPLATE_FIELDS = {
    "DISPATCH.md": ("TO", "OBJECT", "EXACT_REF", "ACTION", "ACCEPTANCE", "FENCES", "NEXT_EVENT"),
    "RECEIPT.md": (
        "STATE", "OBJECT", "EXACT_REF", "EVIDENCE", "PROGRESS", "EFFECT", "BLOCKED_ON",
        "NEXT_OWNER",
    ),
    "EXPERIMENT.md": (
        "HYPOTHESIS", "OBJECT", "DEPLOYED_FORM", "MEASUREMENT", "PASS_BAR", "KILL_BAR",
        "COST", "OUTCOME", "INDEPENDENT_REPRO",
    ),
}
RECEIPT_STATES = {"DONE", "PARTIAL", "BLOCKED", "KILLED", "INVALIDATED"}
PROGRESS_KINDS = {"DECISION", "MEASUREMENT", "INFRASTRUCTURE"}
EXPERIMENT_OUTCOMES = {"PENDING", "PASS", "KILL", "NULL", "INVALID-INSTRUMENT"}
CLAIM_STATUSES = {"HYPOTHESIS", "SUPPORTED", "REFUTED"}
HANDOFF_HEADINGS = (
    "## THE WHOLE JOB, IN FOUR LINES",
    "## BINDING RULES RIGHT NOW",
    "## EVERY NUMBER WORTH CITING",
    "## OPEN QUESTIONS",
    "## WHAT NOT TO DO",
)


def fail(msgs, text):
    msgs.append("ERROR   " + text)


def note(msgs, text):
    msgs.append("warn    " + text)


def check_paths(root, msgs):
    src = root / "START-HERE.md"
    if not src.exists():
        fail(msgs, "START-HERE.md missing -- the skeleton has no front door")
        return
    tokens = re.findall(r"`([^`\n]+)`", src.read_text(encoding="utf-8"))
    for tok in tokens:
        if " " in tok or "*" in tok or tok.startswith("http"):
            continue
        if not ("/" in tok or "\\" in tok or tok.endswith((".md", ".py", ".yml", ".yaml"))):
            continue
        path = root / tok.rstrip("/")
        if not path.exists():
            fail(msgs, f"START-HERE.md claims `{tok}` but it does not exist")


def parse_table_rows(text, id_prefix=None):
    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or set(cells[0]) <= {"-", " ", ":"}:
            continue
        if id_prefix and not cells[0].startswith(id_prefix):
            continue
        rows.append(cells)
    return rows


def project_markdown(root):
    """Include tracked and not-yet-tracked Markdown; exclude only git internals."""
    return sorted(
        path for path in root.rglob("*.md")
        if path.is_file() and ".git" not in path.relative_to(root).parts
    )


def check_retractions(root, msgs):
    ledger = root / "workflow" / "canon" / "RETRACTIONS.md"
    if not ledger.exists():
        fail(msgs, "workflow/canon/RETRACTIONS.md missing")
        return
    tokens = []
    for cells in parse_table_rows(ledger.read_text(encoding="utf-8")):
        if cells[0] != "token":
            tokens.append(cells[0])
    for path in project_markdown(root):
        if path.resolve() == ledger.resolve():
            continue
        body = path.read_text(encoding="utf-8", errors="replace")
        for token in tokens:
            if token and token in body:
                fail(
                    msgs,
                    f"retracted token '{token}' cited in {path.relative_to(root)} -- use the ledger replacement",
                )


def check_gates(root, msgs, now=None):
    gates = root / "GATES.md"
    if not gates.exists():
        fail(msgs, "GATES.md missing -- the human-key boundary is undefined")
        return
    now = now or datetime.now()
    seen = set()
    open_count = 0
    rows = parse_table_rows(gates.read_text(encoding="utf-8"), id_prefix="G-")
    for cells in rows:
        if len(cells) != 5:
            fail(msgs, f"gate row malformed (need exactly 5 cells): {cells}")
            continue
        gid, what, _owner, opened_s, status = cells
        if gid in seen:
            fail(msgs, f"duplicate gate ID: {gid}")
        seen.add(gid)
        try:
            opened = datetime.strptime(opened_s, "%Y-%m-%d")
        except ValueError:
            fail(msgs, f"gate {gid}: opened date '{opened_s}' not YYYY-MM-DD")
            continue

        normalized = status.upper()
        if normalized == "OPEN":
            open_count += 1
            age = now - opened
            if age > timedelta(hours=SLA_HOURS):
                fail(
                    msgs,
                    f"gate {gid} OPEN for {age.days}d ({what[:60]}) -- SLA is {SLA_HOURS}h; answer or defer it",
                )
        elif normalized == "ANSWERED":
            pass
        else:
            match = re.fullmatch(r"DEFERRED\((\d{4}-\d{2}-\d{2})\)", normalized)
            if not match:
                fail(msgs, f"gate {gid}: invalid status '{status}'")
                continue
            revisit = datetime.strptime(match.group(1), "%Y-%m-%d")
            if revisit.date() < now.date():
                fail(msgs, f"gate {gid}: deferral date {match.group(1)} has passed -- re-decide it")
    if open_count:
        note(msgs, f"{open_count} gate(s) OPEN and inside SLA -- fine, but they are on the clock")


def parse_fields(body):
    fields = {}
    for line in body.splitlines():
        match = re.match(r"^([A-Z][A-Z0-9_]*):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def check_required_fields(path, required, msgs):
    body = path.read_text(encoding="utf-8", errors="replace")
    fields = parse_fields(body)
    missing = [key for key in required if key not in fields]
    empty = [key for key in required if key in fields and not fields[key]]
    placeholder = [key for key in required if key in fields and "<" in fields[key] and ">" in fields[key]]
    if missing:
        fail(msgs, f"{path.relative_to(path.parents[2])} missing field(s): {', '.join(missing)}")
    if empty:
        fail(msgs, f"{path.name} has empty field(s): {', '.join(empty)}")
    if placeholder:
        fail(msgs, f"{path.name} retains placeholder field(s): {', '.join(placeholder)}")
    return fields


def check_templates(root, msgs):
    template_dir = root / "workflow" / "templates"
    for name, required in TEMPLATE_FIELDS.items():
        path = template_dir / name
        if not path.exists():
            fail(msgs, f"workflow/templates/{name} missing")
            continue
        fields = parse_fields(path.read_text(encoding="utf-8", errors="replace"))
        missing = [key for key in required if key not in fields]
        if missing:
            fail(msgs, f"template {name} missing schema field(s): {', '.join(missing)}")
    handoff = template_dir / "HANDOFF.md"
    if not handoff.exists():
        fail(msgs, "workflow/templates/HANDOFF.md missing")
    else:
        body = handoff.read_text(encoding="utf-8", errors="replace")
        for heading in HANDOFF_HEADINGS:
            if heading not in body:
                fail(msgs, f"template HANDOFF.md missing heading: {heading}")


def check_receipts(root, msgs):
    directory = root / "workflow" / "receipts"
    if not directory.exists():
        fail(msgs, "workflow/receipts/ missing")
        return
    required = ("STATE", "OBJECT", "EXACT_REF", "EVIDENCE", "PROGRESS", "EFFECT", "NEXT_OWNER")
    for path in sorted(directory.glob("*.md")):
        fields = check_required_fields(path, required, msgs)
        state = fields.get("STATE", "").upper()
        if state and state not in RECEIPT_STATES:
            fail(msgs, f"receipt {path.name} has invalid STATE '{fields['STATE']}'")
        if state == "BLOCKED" and not fields.get("BLOCKED_ON"):
            fail(msgs, f"receipt {path.name} is BLOCKED but has no BLOCKED_ON")
        progress = fields.get("PROGRESS", "").upper()
        if progress and progress not in PROGRESS_KINDS:
            fail(msgs, f"receipt {path.name} has invalid PROGRESS '{fields['PROGRESS']}'")
        effect = fields.get("EFFECT", "").lower()
        if state == "DONE" and progress in {"DECISION", "MEASUREMENT"} and effect.startswith("none"):
            fail(msgs, f"receipt {path.name} claims {progress} progress but EFFECT is none")
        exact_ref = fields.get("EXACT_REF", "")
        if (root / ".git").exists() and re.fullmatch(r"[0-9a-f]{7,40}", exact_ref):
            result = subprocess.run(
                ["git", "-C", str(root), "cat-file", "-e", f"{exact_ref}^{{commit}}"],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                fail(msgs, f"receipt {path.name} cites missing git commit {exact_ref}")


def check_claims(root, msgs):
    path = root / "CLAIMS.md"
    if not path.exists():
        fail(msgs, "CLAIMS.md missing -- public claims have no falsification registry")
        return
    rows = parse_table_rows(path.read_text(encoding="utf-8"), id_prefix="C-")
    if not rows:
        fail(msgs, "CLAIMS.md contains no claim rows")
        return
    seen = set()
    for cells in rows:
        if len(cells) != 5:
            fail(msgs, f"claim row malformed (need exactly 5 cells): {cells}")
            continue
        claim_id, claim, status, falsifier, evidence = cells
        if claim_id in seen:
            fail(msgs, f"duplicate claim ID: {claim_id}")
        seen.add(claim_id)
        if not claim or not falsifier:
            fail(msgs, f"claim {claim_id} must state both claim and falsifier")
        normalized = status.upper()
        if normalized not in CLAIM_STATUSES:
            fail(msgs, f"claim {claim_id} has invalid status '{status}'")
        if normalized in {"SUPPORTED", "REFUTED"}:
            matches = re.findall(r"`([^`]+)`", evidence)
            if not matches:
                fail(msgs, f"claim {claim_id} is {normalized} without repository-bound evidence")
            for token in matches:
                if not (root / token).exists():
                    fail(msgs, f"claim {claim_id} cites missing evidence path `{token}`")


def check_dispatches(root, msgs):
    directory = root / "workflow" / "dispatches"
    if not directory.exists():
        return
    required = TEMPLATE_FIELDS["DISPATCH.md"]
    for path in sorted(directory.glob("*.md")):
        check_required_fields(path, required, msgs)


def check_experiments(root, msgs):
    directory = root / "workflow" / "experiments"
    if not directory.exists():
        return
    required = TEMPLATE_FIELDS["EXPERIMENT.md"]
    for path in sorted(directory.glob("*.md")):
        fields = check_required_fields(path, required, msgs)
        outcome = fields.get("OUTCOME", "").split(maxsplit=1)[0].upper()
        if outcome and outcome not in EXPERIMENT_OUTCOMES:
            fail(msgs, f"experiment {path.name} has invalid OUTCOME '{fields['OUTCOME']}'")
        if outcome == "PASS" and not fields.get("INDEPENDENT_REPRO"):
            fail(msgs, f"experiment {path.name} is PASS but has no INDEPENDENT_REPRO")


def check_handoffs(root, msgs):
    directory = root / "workflow" / "handoffs"
    if not directory.exists():
        fail(msgs, "workflow/handoffs/ missing")
        return
    for path in sorted(directory.glob("*.md")):
        body = path.read_text(encoding="utf-8", errors="replace")
        if not body.startswith("# RESUME HERE"):
            fail(msgs, f"handoff {path.name} must start with '# RESUME HERE'")
        for heading in HANDOFF_HEADINGS:
            if heading not in body:
                fail(msgs, f"handoff {path.name} missing heading: {heading}")


def check_laws(root, msgs):
    path = root / "LAWS.md"
    if not path.exists():
        fail(msgs, "LAWS.md missing")
        return
    body = path.read_text(encoding="utf-8", errors="replace")
    sections = re.split(r"(?=^## Law \d+)", body, flags=re.MULTILINE)[1:]
    if not sections:
        fail(msgs, "LAWS.md contains no numbered laws")
    for section in sections:
        title = section.splitlines()[0]
        if "**Earned by:**" not in section:
            fail(msgs, f"{title} has no Earned by evidence")
        if "**Enforcement:**" not in section:
            fail(msgs, f"{title} has no Enforcement grade")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None, help="repo root (default: parent of this script)")
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    msgs = []
    check_paths(root, msgs)
    check_retractions(root, msgs)
    check_gates(root, msgs)
    check_templates(root, msgs)
    check_receipts(root, msgs)
    check_claims(root, msgs)
    check_dispatches(root, msgs)
    check_experiments(root, msgs)
    check_handoffs(root, msgs)
    check_laws(root, msgs)
    errors = [msg for msg in msgs if msg.startswith("ERROR")]
    warns = [msg for msg in msgs if msg.startswith("warn")]
    for msg in msgs:
        print(msg)
    verdict = "ONBOARD CHECK PASSED" if not errors else "ONBOARD CHECK FAILED -- docs are lying somewhere"
    print(f"\n{len(errors)} error(s), {len(warns)} warning(s). {verdict}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
