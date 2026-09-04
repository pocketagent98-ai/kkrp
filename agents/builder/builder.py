#!/usr/bin/env python3
"""
Builder Agent
Builds Godot project and exports APK using Godot CLI.
Writes checkpoints/build_report.json
"""
from __future__ import annotations
import argparse, json, os, sys, subprocess
from datetime import datetime, timezone
from pathlib import Path

def create_export_presets(project_dir: Path) -> None:
    presets_content = '''[preset.0]
name="Android"
platform="Android"
runnable=true
dedicated_server=false
custom_features=""
export_filter="all_resources"
export_files=[]
include_filter=""
exclude_filter=""
export_label=""
encrypt_export=false
script_encryption_key=""
[preset.0.options]
custom_template/debug=""
custom_template/release=""
gradle_build/use_gradle_build=true
package/unique_name="com.kkrp.desertrush"
package/name="Desert Rush"
package/signed=true"
version/code=1
version/name="1.0.0"
min_sdk=21
target_sdk=34
'''
    presets_path = project_dir / "export_presets.cfg"
    with open(presets_path, "w") as f:
        f.write(presets_content)

def build_apk(godot_path: str, project_dir: Path, output_path: Path) -> dict:
    result = {"status": "pending", "apk_path": str(output_path), "build_time": None, "errors": []}
    create_export_presets(project_dir)
    try:
        cmd = [godot_path, "--headless", "--path", str(project_dir), "--export-release", "Android", str(output_path)]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if proc.returncode == 0:
            result["status"] = "success" if output_path.exists() else "failed"
        else:
            result["status"] = "failed"
            result["errors"].append(proc.stderr[:500])
    except FileNotFoundError:
        result["status"] = "failed"
        result["errors"].append(f"Godot not found at {godot_path}")
    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["errors"].append("Build timed out after 300s")
    except Exception as e:
        result["status"] = "failed"
        result["errors"].append(str(e))
    return result

def main() -> int:
    parser = argparse.ArgumentParser(description="Game Factory Builder Agent")
    parser.add_argument("--checkpoints", default="checkpoints")
    parser.add_argument("--project", default="game/godot-project")
    parser.add_argument("--godot", default=os.environ.get("GODOT_PATH", "godot"))
    parser.add_argument("--output", default="build/desert-rush-v1.apk")
    args = parser.parse_args()
    checkpoints_dir = Path(args.checkpoints)
    project_dir = Path(args.project)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    build_result = build_apk(args.godot, project_dir, output_path)
    report = {"status": build_result["status"], "apk_path": build_result["apk_path"], "built_at": datetime.now(timezone.utc).isoformat(), "errors": build_result["errors"]}
    if output_path.exists():
        report["apk_size"] = output_path.stat().st_size
    with open(checkpoints_dir / "build_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"[builder] Build status: {report['status']}")
    if "apk_size" in report:
        print(f"[builder] APK size: {report['apk_size']:,} bytes ({report['apk_size']/1024/1024:.1f} MB)")
    print(f"[builder] Wrote report to {checkpoints_dir / 'build_report.json'}")
    print("[builder] Done.")
    return 0 if report["status"] == "success" else 1

if __name__ == "__main__":
    sys.exit(main())
