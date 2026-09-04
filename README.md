# 🎮 KKRP Game Factory

> AI-powered game development pipeline — give a Game Bible, get a playable game.
> Built with Godot 4.7.2, GitHub Actions, and a capability-based AI agent system.

## 🏜️ Current Game: Desert Rush — City Builder Escape

A 3D offline hyper-casual game designed for UAE, Singapore, and Gulf/SE Asia markets.

- **No Ads, No Paywall — Pure Fun**
- 5 levels: Desert → City progression
- 3-lane endless runner with coins, obstacles, star ratings
- Offline ready, mobile-first
- Languages: English, Arabic, Hindi, Malay

### Play Now
Open `index.html` in any modern browser. Works offline.

## 🏗️ Architecture

```
YOU
  ↓
Game Bible (YAML)
  ↓
GitHub Actions Workflow
  ↓
┌─────────────────────────┐
│   Game Factory Pipeline  │
│  ├─ Parse Bible          │
│  ├─ Build Task Graph     │
│  ├─ Select Capabilities  │
│  ├─ Generate Code        │
│  ├─ Generate Assets      │
│  ├─ Build (Godot/Web)    │
│  ├─ Run Tests            │
│  ├─ QA (Gameplay/Perf)   │
│  ├─ Security Scan       │
│  └─ Release Artifact     │
└─────────────────────────┘
  ↓
Build Output (HTML5 / APK / Desktop)
```

### Storage Architecture

| Service | Purpose |
|---------|---------|
| GitHub | Source code, workflows, configs |
| Hugging Face | AI models, datasets, large assets |
| Cloudflare R2 | Production assets, CDN, builds |
| Backblaze B2 | Secondary backup |
| Supabase | Users, auth, database, cloud saves |

### Server Architecture

```
INTERNET
    │
    ├── Cloudflare (Edge/Durable Objects) ── Matchmaking, Lobby, Presence
    │
    ├── Supabase ── Auth, DB, Cloud Save, Inventory
    │
    └── Oracle Cloud (Always Free VM)
        └── Godot Dedicated Server
            ├── Room 1 (Players)
            ├── Room 2 (Players)
            └── Room 3 (Players)
```

## 🚀 Quick Start

### Play the Game
```bash
# Just open in browser
open index.html
# Or serve locally
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Run the Game Factory Workflow
1. Edit `game_bible.yaml` with your game spec
2. Go to GitHub Actions tab
3. Select "Game Factory" workflow
4. Click "Run workflow"
5. Choose build target (web/android/desktop)
6. Download the artifact

### Create Your Own Game
1. Copy `game_bible.yaml`
2. Fill in your game details (title, genre, levels, etc.)
3. Commit to repository
4. Run the workflow
5. Get your game build

## 🎮 Game Controls

| Action | Keyboard | Touch |
|--------|----------|-------|
| Move Left | ← / A | Swipe Left / ◀ Button |
| Move Right | → / D | Swipe Right / ▶ Button |
| Jump | ↑ / W / Space | Swipe Up / ⤴ Button |
| Pause | P / ⏸ | ⏸ Button |

## 📁 Project Structure

```
kkrp/
├── index.html              # Playable game (HTML5, offline)
├── game_bible.yaml         # Game specification template
├── README.md               # This file
├── .github/
│   └── workflows/
│       └── game_factory.yml  # CI/CD pipeline
└── projects/               # Generated game builds (auto-created)
    └── GME-YYYYMMDD-HHMMSS/
        ├── builds/
        │   └── web/
        │       └── index.html
        ├── releases/
        ├── assets/
        └── reports/
            └── release_report.md
```

## 🔧 Technical Stack

| Component | Technology |
|-----------|-----------|
| Game Engine | Godot 4.7.2 Stable |
| Web Runtime | Three.js (HTML5) |
| CI/CD | GitHub Actions |
| AI Orchestrator | DeepSeek Harness / OpenManus |
| Sandbox | OpenSandbox |
| Asset Generation | Blender, ComfyUI, NVIDIA Cosmos |
| Testing | GdUnit4 |
| Security | Strix SAST + dependency scan |

## 🌍 Future Monetization (2-3 months post-launch)

- Cosmetic skins (vehicles, characters)
- Season pass (new cities: Abu Dhabi, Kuala Lumpur, Bangkok)
- Optional ads (game-over screen only)
- Branded levels (Emirates, Singapore Airlines)

## 📄 License

MIT License — Free to use, modify, and distribute.

---

Built with ❤️ by KKRP Game Factory
