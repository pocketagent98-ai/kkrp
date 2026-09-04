# Game Factory

An autonomous, AI-driven game generation system that takes a YAML game specification and produces a fully playable, tested Android APK — no manual coding required.

Built around **"Desert Rush: City Builder Escape"**, a hyper-casual 3-lane endless runner that journeys from the Gulf deserts to the Singapore skyline.

---

## How It Works

```
game_spec.yaml ──► Planner ──► Coder ──► Reviewer ──► Tester ──► Builder ──► APK
                      │            │           │            │           │
                      ▼            ▼           ▼            ▼           ▼
                 task_graph    scripts/   review_report  test_report  build_report
```

1. You write `game_spec.yaml` — the master specification.
2. The **planner** breaks it into a task graph across 8 categories (Core, World, NPC, Missions, Combat, Inventory, UI, Audio).
3. The **coder** generates functional GDScript for each task.
4. The **reviewer** checks the code for syntax errors, missing type hints, hardcoded secrets, and leftover placeholders.
5. The **tester** runs GdUnit4 tests + headless gameplay, detects crashes, and implements a Generate→Test→Diagnose→Fix→Test loop.
6. The **builder** exports an APK using the Godot 4.7.2 CLI.
7. Every stage writes a checkpoint to `checkpoints/` so the pipeline is resumable.

---

## Project Structure

```
game-agent/
├── game/godot-project/      # Godot 4.7.2 game project
│   ├── project.godot
│   ├── scenes/Main.tscn
│   └── scripts/ (Main.gd, GameManager.gd, GameConfig.gd)
├── agents/                   # AI agents (Python)
│   ├── planner/              # Reads spec → creates task graph
│   ├── coder/                # Task graph → GDScript code
│   ├── reviewer/             # Code review & static analysis
│   ├── tester/               # GdUnit4 + headless test loop
│   └── builder/              # Godot CLI → APK export
├── game_bible/               # Game design documents (YAML + JSON)
├── automation/               # Orchestration scripts
├── supabase/                 # Backend (migrations + edge functions)
├── checkpoints/              # Pipeline state (resumable)
├── .github/workflows/        # CI/CD pipelines (build, test, autonomous)
├── capabilities.yaml         # Capability registry + LLM providers
├── game_spec.yaml            # Master game specification (THE INPUT)
└── README.md
```

## Game: Desert Rush

**Genre:** Hyper-casual 3-lane endless runner
**Platform:** Android (offline-first)
**Engine:** Godot 4.7.2 (Mobile renderer)
**Languages:** English, Arabic, Hindi, Malay
**Target Markets:** UAE, Singapore, Gulf, SE Asia
**Monetization:** None at launch

### Levels
| # | Name | Theme | Time Limit |
|---|------|-------|------------|
| 1 | Desert Dawn | Desert | 60s |
| 2 | Sand Storm | Sandstorm | 55s |
| 3 | Desert to City | Transition | 50s |
| 4 | City Rush | City | 45s |
| 5 | Singapore Skyline | City Night | 40s |

## CI/CD

### Build Pipeline (`build.yml`)
14-stage pipeline: `01_parse_spec → 02_plan_game → ... → 14_cleanup`

### Autonomous Pipeline (`autonomous-agent.yml`)
Manual trigger with `game_bible_path`, `build_target`, `skip_tests`, `max_fix_iterations` inputs.

## Backend (Supabase)
11 tables with RLS: users, profiles, player_progress, inventory, quests, achievements, settings, friends, cloud_saves, purchases, game_sessions.

## License
MIT
