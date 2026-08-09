#!/usr/bin/env python3
"""The known-bad evaluator: it checks source, not the artifact that would be delivered."""

from pathlib import Path
import importlib.util


path = Path(__file__).with_name("source") / "decision.py"
spec = importlib.util.spec_from_file_location("source_decision", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert module.select_policy() == "verified"
print("GREEN: editable source contains intended behavior")
