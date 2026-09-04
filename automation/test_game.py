#!/usr/bin/env python3
"""Automation: test_game.py — Runs GdUnit4 + headless + telemetry + crash detection."""
import os, sys, subprocess, argparse, json
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description="Test game")
    parser.add_argument("--checkpoints", default="checkpoints")
    parser.add_argument("--project", default="game/godot-project")
    parser.add_argument("--godot", default=os.environ.get("GODOT_PATH", "godot"))
    args = parser.parse_args()
    base = Path(__file__).parent.parent
    cmd = [sys.executable, str(base / "agents/tester/tester.py"),
           "--checkpoints", args.checkpoints, "--project", args.project, "--godot", args.godot]
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd).returncode

if __name__ == "__main__":
    sys.exit(main())
