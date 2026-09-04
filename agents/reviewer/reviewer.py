#!/usr/bin/env python3
"""
Reviewer Agent
Reviews generated GDScript code for common issues.
Writes checkpoints/review_report.json
"""
from __future__ import annotations
import argparse, json, os, sys, re
from datetime import datetime, timezone
from pathlib import Path

def review_file(filepath: Path) -> list[dict]:
    issues = []
    with open(filepath, "r", errors="replace") as f:
        content = f.read()
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if "TODO" in stripped or "FIXME" in stripped or "PLACEHOLDER" in stripped.upper():
            issues.append({"line": i, "severity": "warning", "message": f"Placeholder found: {stripped}"})
        if re.search(r'(?:api_key|password|secret)\s*=\s*["\'][^"\']+["\']', stripped, re.IGNORECASE):
            issues.append({"line": i, "severity": "error", "message": f"Potential hardcoded secret: {stripped}"})
    if content and not content.startswith("extends"):
        if not content.startswith("#"):
            issues.append({"line": 1, "severity": "warning", "message": "File does not start with 'extends'"})
    return issues

def main() -> int:
    parser = argparse.ArgumentParser(description="Game Factory Reviewer Agent")
    parser.add_argument("--checkpoints", default="checkpoints")
    parser.add_argument("--source", default="game/godot-project/scripts")
    args = parser.parse_args()
    source_dir = Path(args.source)
    checkpoints_dir = Path(args.checkpoints)
    if not source_dir.exists():
        print(f"[reviewer] ERROR: source dir not found: {source_dir}", file=sys.stderr)
        return 1
    all_issues = []
    files_reviewed = 0
    for gd_file in source_dir.glob("*.gd"):
        issues = review_file(gd_file)
        all_issues.extend([{"file": str(gd_file.name), **issue} for issue in issues])
        files_reviewed += 1
    errors = [i for i in all_issues if i["severity"] == "error"]
    warnings = [i for i in all_issues if i["severity"] == "warning"]
    status = "pass" if len(errors) == 0 else "fail"
    report = {"status": status, "files_reviewed": files_reviewed, "errors": len(errors), "warnings": len(warnings), "reviewed_at": datetime.now(timezone.utc).isoformat(), "issues": all_issues}
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    with open(checkpoints_dir / "review_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"[reviewer] Reviewed {files_reviewed} files")
    print(f"[reviewer] Errors: {len(errors)}, Warnings: {len(warnings)}")
    print(f"[reviewer] Status: {status}")
    print(f"[reviewer] Wrote report to {checkpoints_dir / 'review_report.json'}")
    print("[reviewer] Done.")
    return 0 if status == "pass" else 1

if __name__ == "__main__":
    sys.exit(main())
