#!/usr/bin/env python3
"""Protected evaluator: execute the deployable artifact, never its editable source."""

from pathlib import Path
import importlib.util


path = Path(__file__).with_name("bundle") / "decision.py"
spec = importlib.util.spec_from_file_location("deployed_decision", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
observed = module.select_policy()
assert observed == "verified", f"deployed artifact mismatch: expected verified, observed {observed}"
print("GREEN: deployed artifact contains intended behavior")
