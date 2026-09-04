#!/usr/bin/env python3
"""Automation: generate_game.py — Main orchestrator: planner → coder → reviewer → fix loop."""
import os, sys, subprocess, argparse
from pathlib import Path

def run_agent(script: str, args: list[str]) -> int:
    cmd = [sys.executable, script] + args
    print(f"  > {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate game from spec")
    parser.add_argument("--spec", default="game_spec.yaml")
    parser.add_argument("--checkpoints", default="checkpoints")
    parser.add_argument("--max-fix-iterations", type=int, default=5)
    args = parser.parse_args()
    base = Path(__file__).parent.parent
    # Step 1: Plan
    print("\n=== Step 1: Plan ===")
    rc = run_agent(str(base / "agents/planner/planner.py"), ["--spec", args.spec, "--checkpoints", args.checkpoints])
    if rc != 0:
        print("❌ Planning failed")
        return rc
    # Step 2: Code
    print("\n=== Step 2: Generate Code ===")
    rc = run_agent(str(base / "agents/coder/coder.py"), ["--checkpoints", args.checkpoints])
    if rc != 0:
        print("❌ Code generation failed")
        return rc
    # Step 3: Review
    print("\n=== Step 3: Review ===")
    rc = run_agent(str(base / "agents/reviewer/reviewer.py"), ["--checkpoints", args.checkpoints])
    # Step 4: Fix loop
    for i in range(args.max_fix_iterations):
        print(f"\n=== Fix iteration {i+1} ===")
        rc = run_agent(str(base / "agents/tester/tester.py"), ["--checkpoints", args.checkpoints])
        if rc == 0:
            print("✅ Tests passed!")
            break
        print(f"Fix iteration {i+1} needed")
    else:
        print("⚠️ Max fix iterations reached")
    # Step 5: Build
    print("\n=== Step 5: Build ===")
    rc = run_agent(str(base / "agents/builder/builder.py"), ["--checkpoints", args.checkpoints])
    print("\n=== Pipeline complete ===")
    return rc

if __name__ == "__main__":
    sys.exit(main())
