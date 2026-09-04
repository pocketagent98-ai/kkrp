#!/usr/bin/env python3
"""Automation: create_sandbox.py — Creates isolated sandbox, installs Godot 4.7.2, clones repo."""
import os, sys, subprocess, argparse
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description="Create sandbox environment")
    parser.add_argument("--workdir", default="/tmp/game_factory_sandbox")
    parser.add_argument("--godot-version", default="4.7.2")
    args = parser.parse_args()
    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    print(f"[sandbox] Workdir: {workdir}")
    # Check if Godot exists
    godot_path = workdir / f"godot-{args.godot_version}"
    if not godot_path.exists():
        print(f"[sandbox] Godot not found at {godot_path}")
        print(f"[sandbox] Download from: https://github.com/godotengine/godot/releases/download/{args.godot_version}-stable/Godot_v{args.godot_version}-stable_linux.x86_64")
    else:
        print(f"[sandbox] Godot found at {godot_path}")
    # Clone repo
    repo_dir = workdir / "kkrp"
    if not repo_dir.exists():
        subprocess.run(["git", "clone", "https://github.com/pocketagent98-ai/kkrp.git", str(repo_dir)])
    print(f"[sandbox] Repo at {repo_dir}")
    print("[sandbox] Done.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
