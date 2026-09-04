#!/usr/bin/env python3
"""
Planner Agent
Reads game_spec.yaml, breaks it into a task graph covering every subsystem.
8 categories: Core / World / NPC / Missions / Combat / Inventory / UI / Audio
Writes checkpoints/task_graph.json and checkpoints/state.json
"""
from __future__ import annotations
import argparse, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

def load_yaml(path: Path) -> dict[str, Any]:
    if _HAS_YAML:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, dict) else {}
    json_path = path.with_suffix(".json")
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    result: dict[str, Any] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            if ":" in line:
                k, _, v = line.partition(":")
                result[k.strip()] = v.strip()
    return result

TASK_TEMPLATES: dict[str, list[tuple[str, str, str, list[str]]]] = {
    "Core": [
        ("core-001", "Project setup", "Create Godot 4.7.2 project, export presets, landscape, min SDK 21.", []),
        ("core-002", "GameConfig autoload", "Implement GameConfig.gd to load config from game_bible JSON.", ["core-001"]),
        ("core-003", "GameManager autoload", "Implement GameManager.gd for level progression, save/load.", ["core-001"]),
        ("core-004", "Main scene", "Create Main.tscn + Main.gd entry point.", ["core-002", "core-003"]),
    ],
    "World": [
        ("world-001", "Terrain system", "Procedural terrain meshes for desert, city, skyline.", ["core-004"]),
        ("world-002", "Lane system", "3-lane runner track with smooth transitions.", ["core-004"]),
        ("world-003", "Level themes", "5 themes: Desert Dawn, Sand Storm, Desert to City, City Rush, Singapore Skyline.", ["world-001"]),
        ("world-004", "Environment lighting", "Directional light, fog, sky per theme.", ["world-001"]),
    ],
    "NPC": [
        ("npc-001", "Player character", "Player car with jump, lane-change, collision.", ["core-004"]),
        ("npc-002", "Obstacle types", "Static/moving obstacles per level.", ["world-002"]),
    ],
    "Missions": [
        ("mis-001", "Level progression", "Sequential unlock: complete N to unlock N+1.", ["core-003"]),
        ("mis-002", "Star rating", "1-3 stars based on coin ratio.", ["mis-001"]),
        ("mis-003", "Timer system", "Per-level countdown, bonus stars for speed.", ["mis-001"]),
    ],
    "Combat": [
        ("combat-001", "Collision detection", "Area3D signals for coin/obstacle.", ["npc-001", "npc-002"]),
        ("combat-002", "Death/respawn", "On hit: bounce back, star penalty, toast.", ["combat-001"]),
    ],
    "Inventory": [
        ("inv-001", "Coin collection", "Coin pool, pickup signal, score increment.", ["npc-001"]),
        ("inv-002", "Power-ups", "Optional: magnet, shield, 2x coin.", ["inv-001"]),
    ],
    "UI": [
        ("ui-001", "HUD overlay", "Score, coins, timer, stars, pause button.", ["inv-001", "mis-003"]),
        ("ui-002", "Main menu", "Start/Continue/Settings/Level-select.", ["ui-001"]),
        ("ui-003", "Pause menu", "Resume/Restart/Quit.", ["ui-001"]),
        ("ui-004", "Localization", "en, ar, hi, ms with RTL.", ["ui-002"]),
    ],
    "Audio": [
        ("aud-001", "Background music", "Looping BGM per level theme.", ["world-003"]),
        ("aud-002", "SFX", "Coin, jump, crash, level-complete sounds.", ["combat-001", "inv-001"]),
    ],
}

def build_task_graph(spec: dict[str, Any]) -> dict[str, Any]:
    tasks = []
    for category, templates in TASK_TEMPLATES.items():
        for task_id, title, desc, deps in templates:
            tasks.append({"id": task_id, "category": category, "title": title, "description": desc, "dependencies": deps, "status": "pending"})
    return {"spec_title": spec.get("title", "Unknown"), "generated_at": datetime.now(timezone.utc).isoformat(), "total_tasks": len(tasks), "categories": list(TASK_TEMPLATES.keys()), "tasks": tasks}

def main() -> int:
    parser = argparse.ArgumentParser(description="Game Factory Planner Agent")
    parser.add_argument("--spec", default="game_spec.yaml")
    parser.add_argument("--checkpoints", default="checkpoints")
    parser.add_argument("--game-bible", default="game_bible")
    args = parser.parse_args()
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"[planner] ERROR: spec not found: {spec_path}", file=sys.stderr)
        return 1
    spec = load_yaml(spec_path)
    print(f"[planner] Loaded spec: {spec.get('title', 'Untitled')}")
    graph = build_task_graph(spec)
    print(f"[planner] Built task graph: {graph['total_tasks']} tasks across {len(graph['categories'])} categories")
    checkpoints_dir = Path(args.checkpoints)
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    with open(checkpoints_dir / "task_graph.json", "w") as f:
        json.dump(graph, f, indent=2)
    with open(checkpoints_dir / "state.json", "w") as f:
        json.dump({"status": "planning_complete", "spec_title": graph["spec_title"], "tasks_total": graph["total_tasks"], "updated_at": datetime.now(timezone.utc).isoformat()}, f, indent=2)
    print(f"[planner] Wrote task graph to {checkpoints_dir / 'task_graph.json'}")
    print(f"[planner] Wrote state to {checkpoints_dir / 'state.json'}")
    print("[planner] Done.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
