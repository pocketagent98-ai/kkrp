#!/usr/bin/env python3
"""Automation: build_game.py — Builds APK/AAB using Godot CLI export."""
import os, sys, subprocess, argparse
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description="Build game APK")
    parser.add_argument("--checkpoints", default="checkpoints")
    parser.add_argument("--project", default="game/godot-project")
    parser.add_argument("--godot", default=os.environ.get("GODOT_PATH", "godot"))
    parser.add_argument("--output", default="build/desert-rush-v1.apk")
    args = parser.parse_args()
    base = Path(__file__).parent.parent
    cmd = [sys.executable, str(base / "agents/builder/builder.py"),
           "--checkpoints", args.checkpoints, "--project", args.project,
           "--godot", args.godot, "--output", args.output]
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd).returncode

if __name__ == "__main__":
    sys.exit(main())
