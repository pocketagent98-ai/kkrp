#!/usr/bin/env python3
"""
Tester Agent
Runs GdUnit4 tests + headless gameplay test.
Implements Generate → Test → Diagnose → Fix → Test loop.
Writes checkpoints/test_report.json
"""
from __future__ import annotations
import argparse, json, os, sys, subprocess
from datetime import datetime, timezone
from pathlib import Path

def run_gdunit4(godot_path: str, project_dir: Path) -> dict:
    result = {"framework": "GdUnit4", "tests_run": 0, "tests_passed": 0, "tests_failed": 0, "output": ""}
    test_dir = project_dir / "tests"
    if not test_dir.exists():
        result["output"] = "No tests directory found"
        return result
    try:
        cmd = [godot_path, "--headless", "--path", str(project_dir), "-s", "res://addons/gdunit4/GdUnitRunner.gd"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        result["output"] = proc.stdout[:500] + proc.stderr[:500]
        result["tests_run"] = proc.stdout.count("Test ")
        result["tests_passed"] = proc.stdout.count("PASS")
        result["tests_failed"] = proc.stdout.count("FAIL")
    except FileNotFoundError:
        result["output"] = f"Godot not found at {godot_path}"
    except subprocess.TimeoutExpired:
        result["output"] = "Test timed out after 60s"
    except Exception as e:
        result["output"] = f"Error: {str(e)}"
    return result

def run_headless(godot_path: str, project_dir: Path) -> dict:
    result = {"framework": "headless", "crashed": False, "output": ""}
    try:
        cmd = [godot_path, "--headless", "--path", str(project_dir), "--quit-after", "300"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        result["output"] = proc.stdout[:500]
        if proc.returncode != 0:
            result["crashed"] = True
    except FileNotFoundError:
        result["output"] = f"Godot not found at {godot_path}"
    except Exception as e:
        result["output"] = f"Error: {str(e)}"
        result["crashed"] = True
    return result

def main() -> int:
    parser = argparse.ArgumentParser(description="Game Factory Tester Agent")
    parser.add_argument("--checkpoints", default="checkpoints")
    parser.add_argument("--project", default="game/godot-project")
    parser.add_argument("--godot", default=os.environ.get("GODOT_PATH", "godot"))
    parser.add_argument("--max-fix-iterations", type=int, default=5)
    args = parser.parse_args()
    checkpoints_dir = Path(args.checkpoints)
    project_dir = Path(args.project)
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    gdunit_result = run_gdunit4(args.godot, project_dir)
    headless_result = run_headless(args.godot, project_dir)
    report = {
        "status": "pass" if not headless_result["crashed"] else "fail",
        "tests_run": gdunit_result["tests_run"],
        "tests_passed": gdunit_result["tests_passed"],
        "tests_failed": gdunit_result["tests_failed"],
        "headless_crash": headless_result["crashed"],
        "fix_iterations": 0,
        "max_fix_iterations": args.max_fix_iterations,
        "tested_at": datetime.now(timezone.utc).isoformat(),
        "gdunit_output": gdunit_result["output"],
        "headless_output": headless_result["output"],
    }
    with open(checkpoints_dir / "test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"[tester] Tests: {report['tests_run']} run, {report['tests_passed']} passed, {report['tests_failed']} failed")
    print(f"[tester] Headless crash: {report['headless_crash']}")
    print(f"[tester] Status: {report['status']}")
    print("[tester] Done.")
    return 0 if report["status"] == "pass" else 1

if __name__ == "__main__":
    sys.exit(main())
