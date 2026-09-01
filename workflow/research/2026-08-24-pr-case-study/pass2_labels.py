#!/usr/bin/env python3
"""Pass-2 intent labels for the 80-PR sample (human inspection of subject+paths).

Categories (exclusive):
  PRODUCT      — changes the playing agent or ship payload
  INSTRUMENT   — harness/eval/test/tooling that measures or guards
  EVIDENCE     — analysis receipts, JSON measurements, verify writeups
  GOVERNANCE   — board, inbox, proposals, design docs, writeup, onboarding
  CEREMONY     — cycle logs, index bumps, changelogs, bus rotation
  OTHER        — empty merge, unclassifiable
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PASS2 = {
    91: "GOVERNANCE",
    2780: "EVIDENCE",
    853: "GOVERNANCE",
    350: "EVIDENCE",
    1278: "CEREMONY",
    1145: "EVIDENCE",
    705: "GOVERNANCE",
    1151: "EVIDENCE",
    812: "GOVERNANCE",
    765: "GOVERNANCE",
    2772: "GOVERNANCE",
    326: "EVIDENCE",
    376: "EVIDENCE",
    769: "GOVERNANCE",
    2152: "OTHER",
    2377: "GOVERNANCE",
    251: "EVIDENCE",
    2310: "GOVERNANCE",
    342: "EVIDENCE",
    2524: "GOVERNANCE",
    2096: "INSTRUMENT",
    2334: "INSTRUMENT",
    1072: "INSTRUMENT",
    987: "INSTRUMENT",
    1287: "EVIDENCE",
    2463: "INSTRUMENT",
    2590: "INSTRUMENT",
    2778: "GOVERNANCE",
    2644: "INSTRUMENT",
    2150: "OTHER",
    734: "INSTRUMENT",
    807: "EVIDENCE",
    2556: "INSTRUMENT",
    113: "PRODUCT",
    198: "INSTRUMENT",
    2460: "EVIDENCE",
    977: "INSTRUMENT",
    2912: "INSTRUMENT",
    2320: "GOVERNANCE",
    2526: "EVIDENCE",
    1024: "EVIDENCE",
    1039: "EVIDENCE",
    781: "GOVERNANCE",
    2143: "OTHER",
    961: "EVIDENCE",
    2328: "GOVERNANCE",
    1283: "EVIDENCE",
    1346: "EVIDENCE",
    441: "EVIDENCE",
    1316: "EVIDENCE",
    123: "CEREMONY",
    1027: "EVIDENCE",
    625: "EVIDENCE",
    1408: "GOVERNANCE",
    2898: "GOVERNANCE",
    1663: "OTHER",
    2011: "GOVERNANCE",
    995: "EVIDENCE",
    2938: "GOVERNANCE",
    417: "EVIDENCE",
    2275: "CEREMONY",
    2916: "EVIDENCE",
    2562: "CEREMONY",
    1970: "GOVERNANCE",
    94: "GOVERNANCE",
    2444: "INSTRUMENT",
    724: "GOVERNANCE",
    2176: "INSTRUMENT",
    317: "EVIDENCE",
    1572: "EVIDENCE",
    1465: "GOVERNANCE",
    1493: "EVIDENCE",
    2122: "INSTRUMENT",
    286: "EVIDENCE",
    2216: "GOVERNANCE",
    11: "GOVERNANCE",
    1423: "PRODUCT",
    1458: "EVIDENCE",
    2075: "GOVERNANCE",
    2239: "GOVERNANCE",
}


def main() -> None:
    rows = [
        json.loads(line)
        for line in (HERE / "artifacts" / "sample80_pass1.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    out = []
    agree = 0
    missing = []
    for row in rows:
        lab = PASS2.get(row["pr"])
        if lab is None:
            missing.append(row["pr"])
            continue
        # collapse pass1 MIXED/CONSTRUCTION vs pass2
        p1 = row["pass1_intent"]
        match = (p1 == lab) or (p1 == "CONSTRUCTION" and lab == "INSTRUMENT") or (
            p1 == "MIXED" and lab in {"INSTRUMENT", "EVIDENCE", "GOVERNANCE"}
        )
        if p1 == lab:
            agree += 1
        row2 = dict(row)
        row2["pass2_intent"] = lab
        row2["exact_agree"] = p1 == lab
        out.append(row2)
    assert not missing, missing
    summary = {
        "n": len(out),
        "pass2": dict(Counter(r["pass2_intent"] for r in out)),
        "pass1": dict(Counter(r["pass1_intent"] for r in out)),
        "exact_agree": agree,
        "exact_agree_rate": round(agree / len(out), 4),
        "product_or_instrument": sum(
            1 for r in out if r["pass2_intent"] in {"PRODUCT", "INSTRUMENT"}
        ),
        "governance_or_ceremony": sum(
            1 for r in out if r["pass2_intent"] in {"GOVERNANCE", "CEREMONY"}
        ),
        "evidence": sum(1 for r in out if r["pass2_intent"] == "EVIDENCE"),
        "note": "Sample is stratified by file_class (20 docs/code/other + 20 extra small). Not a simple random sample of all merges.",
    }
    dest = HERE / "artifacts" / "sample80_pass2.jsonl"
    dest.write_text("\n".join(json.dumps(x) for x in out) + "\n", encoding="utf-8")
    (HERE / "artifacts" / "sample80_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
