# Project Directory Structure

```
pixel-survival-game/
│
├── 📄 MAIN GAME FILES (Modular Python)
│   ├── main.py                    # Game loop & orchestration (400 lines)
│   ├── constants.py               # All game config (140 lines)
│   ├── entities.py                # Game classes: Tree, Crab, Forge, Cloud (550 lines)
│   ├── inventory.py               # Crafting system & items (380 lines)
│   ├── terrain.py                 # World generation & caves (380 lines)
│   ├── assets.py                  # Sprite & texture loading (310 lines)
│   └── rendering.py               # UI drawing & rendering (450 lines)
│
├── 📁 DOCUMENTATION (Guides & Info)
│   ├── README.md                  # Complete game guide & features
│   ├── QUICKSTART.md              # Quick start for players/devs
│   ├── PROJECT_STRUCTURE.md       # Modular design explanation
│   ├── REFACTORING_COMPLETE.md    # This refactoring summary
│   └── PROJECT_TREE.md            # (This file)
│
├── 🌐 WEB VERSION
│   └── index.html                 # GitHub Pages landing page (responsive)
│
├── ⚙️ CONFIGURATION
│   ├── requirements.txt           # Dependencies (Pygame)
│   ├── .gitignore                 # Git ignore rules
│   └── .git/                      # Git repository (when initialized)
│
├── 🎨 ASSETS (Textures & Sprites)
│   └── models/
│       ├── MC-stand-still-look-right.png
│       ├── MC-stand-still-look-left.png
│       ├── MC-walk-right-main.png
│       ├── MC-walk-right-main-2.png
│       ├── MC-walk-right-main-3.png
│       ├── MC-walk-right.png
│       ├── MC-walk-left-main.png
│       ├── MC-walk-left-main-2.png
│       ├── MC-walk-left-main-3.png
│       ├── MC-walk-left.png
│       ├── Hop-til-højre.png
│       ├── Hop-til-venstre.png
│       ├── leaves1.png
│       ├── leaves2.png
│       ├── red-leaves.png
│       ├── wood.png
│       ├── wood-with-hole.png
│       ├── Overgang-Grass-Jord.png
│       ├── Jord.png
│       ├── Stone.png
│       ├── Sand.png
│       ├── Limestone.png
│       ├── Copper-ore.png
│       ├── Iron-ore.png
│       ├── Gold-ore.png
│       ├── Ruby.png
│       ├── Bedrock.png
│       ├── Sky.png
│       ├── Toppen-af-himmlen.png
│       ├── cloud-type-1.png
│       ├── Crab-stand.png
│       ├── Crab-stand-bobing.png
│       ├── Wood-pickaxe-up-standart.png
│       ├── Wood-pickaxe-left.png
│       ├── Wood-pickaxe-right.png
│       ├── knife.png          ← NEW KNIFE TEXTURE (Now integrated!)
│       ├── Pickaxe.png
│       ├── Crafting-table.png
│       ├── watertop.png
│       ├── waterbottom.png
│       ├── Forge.png
│       ├── Forge-bobing.png
│       ├── Forge-fire.png
│       ├── Forge-fire-bobing.png
│       ├── PLANKS.png
│       └── title.png
│
├── 💾 SAVE DATA (Generated at runtime)
│   └── saves/
│       ├── slot_1.json.gz        # Compressed save slot 1
│       ├── slot_2.json.gz        # Compressed save slot 2
│       └── slot_3.json.gz        # Compressed save slot 3
│
└── 🗑️ CACHE (Generated at runtime - ignored by git)
    └── __pycache__/             # Python bytecode cache
        ├── main.cpython-39.pyc
        ├── constants.cpython-39.pyc
        ├── entities.cpython-39.pyc
        └── ... (compiled modules)
```

---

## File Size Summary

| Category | Files | Total Size |
|----------|-------|-----------|
| Python Core | 7 | ~70 KB |
| Documentation | 5 | ~25 KB |
| Website | 1 | ~15 KB |
| Configuration | 2 | ~1 KB |
| **Textures** | ~50 | **~5 MB** |
| **TOTAL** | ~65 | **~5.1 MB** |

---

## Lines of Code Distribution

```
main.py            ████░░░░░░ 400 lines
entities.py        ██████░░░░ 550 lines
rendering.py       █████░░░░░ 450 lines
inventory.py       ████░░░░░░ 380 lines
terrain.py         ████░░░░░░ 380 lines
assets.py          ███░░░░░░░ 310 lines
constants.py       ██░░░░░░░░ 140 lines
────────────────────────────────────────
Total:             ~2,610 lines (modular!)
```

Original: 5000+ lines (monolithic)

---

## Quick File Lookup

**Looking for...**  |  **Find in...**
--- | ---
Game loop | `main.py`
Screen size settings | `constants.py`
Tree/Enemy/Forge code | `entities.py`
Crafting recipes | `inventory.py`
Biomes & caves | `terrain.py`
Sprite loading | `assets.py`
UI drawing | `rendering.py`
Player stats | `constants.py`
Physics | `constants.py` (gravity, jump, etc)
Item colors | `constants.py`
Controls | `main.py`
Save system | `main.py`
Game balance | `constants.py`
Knife texture | `assets.py` & `rendering.py`

---

## Installation Files Needed

To run the game, you need:
- ✅ All 7 `.py` files
- ✅ All files in `models/` folder
- ✅ `requirements.txt`

Optional for sharing:
- ✅ `README.md` & other docs
- ✅ `index.html` for website
- ✅ `.gitignore` for GitHub

---

## Creating Each File

When setting up from scratch:

1. Copy all `.py` files to project root
2. Create `models/` folder with all textures
3. Run: `pip install -r requirements.txt`
4. Run: `python main.py`

---

## Directory Initialization

After first run, game auto-creates:
- `saves/` folder (empty, fills with `.json.gz` files)
- `__pycache__/` folder (Python bytecode, safe to delete)

---

## GitHub Structure

When pushed to GitHub:
```
yourusername/pixel-survival-game/
├── All files above
├── .git/              (GitHub metadata)
└── README.md          (GitHub shows this on front page)
```

GitHub Pages serves `index.html` as landing page.

---

## Web Hosting Structure

On GitHub Pages:
```
https://yourusername.github.io/pixel-survival-game/
├── index.html         (Landing page users see)
├── README.md          (Linked from index)
└── All other files    (Available for download)
```

Users can:
1. View beautiful landing page
2. Click "GitHub" to see source code
3. Click "Download" to get game files
4. Follow instructions in README

---

## Best Practices

✅ **Do:**
- Keep all `.py` files in root directory
- Keep `models/` folder at same level as `main.py`
- Use relative paths (`./models/filename.png`)
- Commit everything to git except `__pycache__` and saves

❌ **Don't:**
- Move `.py` files to subdirectories (breaks imports)
- Delete `models/` files (game won't work)
- Commit save files (they're local player data)
- Commit `__pycache__/` (auto-generated)

---

## Modifying Structure

If you want to reorganize:

### Example: Create `src/` subdirectory
```bash
mkdir src
mv *.py src/
# Update imports in all files:
# Add "from src." prefix or adjust sys.path in main.py
```

### Example: Separate game logic
```bash
mkdir core
mkdir rendering_ui
mkdir world
# Move related files to each folder
# Update all imports accordingly
```

**Note:** Currently everything is in root for simplicity. Modular enough without deep nesting.

---

## Asset Organization (Optional)

If textures grow large, you could organize:
```
models/
├── sprites/
│   ├── player/
│   ├── enemies/
│   └── items/
├── tiles/
│   ├── terrain/
│   ├── biomes/
│   └── blocks/
└── ui/
    └── menus/
```

Just update `MODEL_DIR` references in code.

---

## Version Control

```bash
# Initial setup
git init
git add .
git commit -m "Initial project setup - 9 modular files"
git remote add origin https://github.com/you/pixel-game
git push -u origin main

# Daily development
git add .
git commit -m "Feature: Add new biome"
git push

# .gitignore automatically excludes:
# - __pycache__/
# - saves/*.gz
# - .vscode/
# - .DS_Store
# - *.pyc
```

---

## Deploying Website

Once pushed to GitHub:

1. Settings → Pages
2. Select "main branch"
3. Wait 1-2 minutes
4. Website live at `github.com/yourusername/pixel-game`

`index.html` serves automatically!

---

## Summary

You now have:
- ✅ 7 modular Python files (~2,600 lines total)
- ✅ Complete documentation (5 guides)
- ✅ Professional website ready
- ✅ Clean git structure
- ✅ Asset organization
- ✅ Configuration management

Everything organized, documented, and ready for GitHub! 🎉

---

*Last updated: 2024*  
*All files ready for deployment*
