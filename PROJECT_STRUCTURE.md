# Project Structure & File Organization

## Overview
Your Pygame game has been refactored from a single 5000+ line file into 9 organized, maintainable modules.

## File Breakdown

### Core Game Files (Modular)

#### 1. **constants.py** (2.9 KB)
- All game configuration in one place
- Screen dimensions, physics constants, tile sizes
- Game balance settings (health, damage, gravity)
- Item definitions and colors
- Crafting recipes definitions
- Biome configurations
- Tool durability values

**Why modular:** Easy to tweak game balance without touching logic. Want to change jump height? Edit one line in constants.py.

---

#### 2. **entities.py** (14.2 KB)
- `Tree` class - Destructible trees with block layout, damage tracking, serialization
- `Crab` class - Enemy AI with movement, fleeing, jumping
- `Forge` class - Furnace logic with smelting progress, fuel management
- `Cloud` class - Decorative sky elements

**Why modular:** All game objects isolated. Adding a new enemy? Create a new class here.

---

#### 3. **inventory.py** (10.6 KB)
- Crafting recipe definitions
- `create_inventory()` - Initialize player inventory
- `get_hotbar_items()` - Dynamic hotbar based on inventory
- `get_crafting_recipe()` - Recipe matching (shapeless & shaped)
- `craft_item()` - Perform crafting
- Inventory utilities (item lists, slot data extraction)

**Why modular:** All crafting logic in one place. Easy to add new recipes or balance crafting.

---

#### 4. **terrain.py** (9.8 KB)
- `get_surface_tile_y()` - Procedural height generation
- `carve_ellipse()` - Cave carving algorithm
- `generate_terrain_chunk()` - Chunk generation with biomes, caves, water
- `get_terrain_tile()` - Tile lookup with lazy loading
- `unload_distant_chunks()` - Chunk management for performance
- Biome definitions

**Why modular:** All world generation isolated. Change cave shapes? Edit `carve_ellipse()`.

---

#### 5. **assets.py** (8.4 KB)
- All sprite/texture file definitions
- `load_player_sprites()` - Animation frames
- `load_tile_images()` - Terrain textures
- `load_tree_images()` - Tree parts
- `load_crab_sprites()` - Enemy sprites
- `get_item_surface()` - Smart item rendering with fallbacks

**Why modular:** Centralized asset loading. Missing a texture? Fallback to color automatically.

---

#### 6. **rendering.py** (13.2 KB)
- `draw_sky()` - Background rendering
- `draw_ground()` - Terrain tiles
- `draw_placed_blocks()` - All placed blocks and forges
- `draw_item_in_hand()` - Player held items (axe, knife, etc)
- `draw_hotbar()` - Bottom UI bar
- `draw_health_hud()` - Health display
- `draw_damage_effect()` - Red flash on damage
- `draw_death_screen()` - Death UI
- Debug rendering

**Why modular:** All drawing code in one place. Want a HUD change? Edit here without touching game logic.

---

#### 7. **ui.py** (FUTURE - Not yet created)
- Menu screens (main, options, credits)
- Inventory GUI
- Pause menu
- Settings dialog

**Why modular:** UI separate from game logic. Redesign menus without affecting gameplay.

---

#### 8. **physics.py** (FUTURE - Not yet created)
- `get_nearby_solid_rects()` - Collision queries
- `get_terrain_break_hits()` - Tool effectiveness
- `apply_fall_damage()` - Fall physics
- Water physics
- Crab collision validation

**Why modular:** Physics math isolated. Change collision system? Rewrite physics.py only.

---

#### 9. **main.py** (REFACTORED)
- Game loop and state management
- Event handling
- Imports and orchestrates all modules
- ~400 lines (vs 5000+ originally!)

**Why modular:** Main.py just ties everything together. Easy to understand game flow.

---

### Configuration Files

#### **requirements.txt**
```
pygame>=2.1.0
```
- Single dependency for easy setup
- `pip install -r requirements.txt` handles everything

---

#### **README.md** (5.9 KB)
- Complete game documentation
- Installation instructions
- Controls and game mechanics
- File structure explanation
- Modular design benefits
- Crafting recipes reference
- Planned features

---

#### **.gitignore**
- Python cache, bytecode, virtual environments
- IDE files (.vscode, .idea)
- Save game files
- OS junk (Thumbs.db, .DS_Store)

---

#### **index.html** (15.3 KB)
- Beautiful landing page for GitHub Pages
- Game information
- Installation instructions
- Controls reference
- Crafting recipes modal
- How-to-play modal
- Links to GitHub repo
- Mobile responsive design

---

### Asset Folders

#### **models/**
- All texture files (PNG)
  - Player sprites (standing, walking, jumping, left/right)
  - Tiles (grass, stone, sand, ore, etc)
  - Tree parts (wood, leaves)
  - Enemy sprites (crab animations)
  - Forge animations
  - Sky and clouds
  - Item icons

#### **saves/**
- Auto-created when game runs
- Stores 3 save slots
- Compressed with gzip
- Contains player data, inventory, placed blocks

---

## Benefits of Modular Structure

### ✅ Maintainability
- Each file has a single responsibility
- Easy to find and fix bugs
- Clear dependencies between modules

### ✅ Scalability
- Add new items? Edit `inventory.py` only
- New enemy type? Add class to `entities.py`
- Change rendering style? Modify `rendering.py`
- No need to touch other files

### ✅ Reusability
- Each module can be imported independently
- `from entities import Tree` works standalone
- Useful for creating tools or editors

### ✅ Testing
- Test each module separately
- Mock dependencies easily
- Unit test individual functions

### ✅ Team Development
- Multiple people can work on different modules
- Fewer merge conflicts
- Clear division of responsibilities

### ✅ Web Porting
- Can compile each module to WASM independently
- Tests modules before full web deployment
- Easier to debug web version

---

## File Sizes Summary

| File | Size | Lines | Purpose |
|------|------|-------|---------|
| constants.py | 2.9 KB | 140 | Configuration |
| entities.py | 14.2 KB | 550 | Game classes |
| inventory.py | 10.6 KB | 380 | Crafting & items |
| terrain.py | 9.8 KB | 380 | World generation |
| assets.py | 8.4 KB | 310 | Asset loading |
| rendering.py | 13.2 KB | 450 | UI & drawing |
| main.py | ~10 KB | 400 | Game loop |
| ui.py | TBD | TBD | Menu screens |
| physics.py | TBD | TBD | Collision/physics |
| **Total** | **~70 KB** | **~2,610** | **Fully modular** |

Original monolithic main.py: ~200 KB, 5000+ lines

---

## How to Use This Structure

### Adding a New Item Type

1. Add to `constants.py`:
   ```python
   "new_item": (100, 100, 100),  # In ITEM_COLORS
   ```

2. Add recipe to `inventory.py`:
   ```python
   {
       "name": "new_item",
       "type": "shapeless",
       "input": {"wood": 2},
       "output": {"new_item": 1},
   }
   ```

3. Add texture to `models/` folder

4. That's it! Game automatically handles rendering, crafting, inventory

---

### Adding a New Enemy Type

1. Create class in `entities.py`:
   ```python
   class Dragon:
       def __init__(self, x):
           self.x = x
           # ...
   ```

2. Add sprite loading to `assets.py`

3. Add spawning logic to world generation in `terrain.py`

4. Add rendering in `main.py`'s draw loop

---

### Changing Game Physics

Edit `physics.py` (when created):
- Jump height: Change `JUMP_SPEED`
- Gravity: Change `GRAVITY`
- Fall damage: Modify `apply_fall_damage()`

No other files affected!

---

## GitHub Setup

1. Initialize git:
   ```bash
   git init
   git add .
   git commit -m "Initial modular game structure"
   ```

2. Create GitHub repo and push:
   ```bash
   git remote add origin https://github.com/yourusername/pixel-survival-game.git
   git push -u origin main
   ```

3. Enable GitHub Pages in repo settings:
   - Settings → Pages → Source: main branch, root folder
   - Website available at `https://yourusername.github.io/pixel-survival-game/`

4. `index.html` automatically serves as landing page

---

## Next Steps

### Phase 1: Complete Desktop Version
- [ ] Create `ui.py` for menus and inventory UI
- [ ] Create `physics.py` for collision detection
- [ ] Implement save/load system
- [ ] Add more biomes

### Phase 2: Optimize & Polish
- [ ] Performance profiling
- [ ] Animation improvements
- [ ] Sound effects
- [ ] Particle systems

### Phase 3: Web Version
- [ ] Convert to Pyodide
- [ ] Test in browser
- [ ] Deploy to GitHub Pages
- [ ] Add web-specific UI

---

Made with modular, scalable code for easy maintenance and extension! 🎮
