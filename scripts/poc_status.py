#!/usr/bin/env python3
"""Render one-glance functionality progress for the ten SEED POCs."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WIDTH = 24


def bar(percent):
    filled = round(percent * WIDTH / 100)
    return "[" + "#" * filled + "-" * (WIDTH - filled) + f"] {percent:3d}%"


def main():
    registry = json.loads((ROOT / "pocs" / "POC-REGISTRY.json").read_text(encoding="utf-8"))
    pocs = registry["pocs"]
    overall = round(sum(item["progress_percent"] for item in pocs) / len(pocs))
    print("SEED POC STATUS")
    print(f"  overall  {bar(overall)}  functionality, not activity")
    print()
    for item in pocs:
        print(
            f"  {item['id']}  {bar(item['progress_percent'])}  "
            f"{item['status']:<6}  {item['name']}"
        )
        if item["status"] != "DONE":
            print(f"          missing: {item['missing']}")


if __name__ == "__main__":
    main()
