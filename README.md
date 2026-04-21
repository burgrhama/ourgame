# 2D Pixel Art Survival Game

A Minecraft-inspired 2D pixel art survival game built with Pygame. Mine, craft, and explore an infinite procedurally-generated world!

## Features

- 🌍 **Infinite Procedural World Generation** - Explore biomes, caves, and terrain shaped by Perlin-like noise
- ⛏️ **Mining & Crafting System** - Gather resources and craft tools, weapons, and structures
- 🪵 **Destructible Environments** - Cut down trees, break stone, and reshape the world
- 🌲 **Biome System** - Green forests, red forests, desert, and ocean biomes
- 👹 **Enemy AI** - Crabs that patrol and flee from the player
- 🔥 **Furnace/Forge System** - Smelt items with fuel management
- 💾 **Save System** - 3 save slots with auto-save support
- 🎮 **Inventory & Hotbar** - Easy item management with crafting interface

## File Structure

```
├── main.py                 # Main game loop and state management
├── constants.py            # All game configuration constants
├── entities.py             # Game classes (Tree, Crab, Forge, Cloud)
├── inventory.py            # Crafting recipes and inventory management
├── terrain.py              # Procedural terrain generation
├── assets.py               # Asset loading (sprites, textures, images)
├── rendering.py            # All UI and drawing functions
├── ui.py                   # Menu and inventory UI screens
├── physics.py              # Collision detection and physics
├── models/                 # All texture and sprite files
├── saves/                  # Save game files
└── requirements.txt        # Python dependencies
```

## Installation

### Desktop Version

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pixel-survival-game.git
cd pixel-survival-game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## Controls

### Gameplay
- **A/D** or **Arrow Keys** - Move left/right
- **W/Up Arrow** - Jump (hold in water to swim up)
- **S/Down Arrow** - Swim down in water
- **1-9** - Select hotbar slot
- **I** - Open inventory/crafting
- **Left Click** - Break blocks/punch entities
- **Right Click** - Place blocks/interact
- **F9** - Toggle debug info
- **F11** - Toggle fullscreen
- **ESC** - Return to menu

### Inventory
- **Left Click** - Pick up/place item
- **Right Click** - Take/drop one item
- **Drag & Drop** - Move items between slots
- **Click Recipe** - Craft items

## Crafting Recipes

### Basic
- **Planks** - 1 Wood → 4 Planks
- **Sticks** - 2 Planks → 4 Sticks
- **Crafting Table** - 4 Planks

### Tools
- **Axe** - 2 Planks + 2 Sticks (shaped, left and right variants)
- **Pickaxe** - 3 Planks + 2 Sticks (3x3 shape)
- **Knife** - 2 Planks + 1 Stick (vertical shape)

### Structures
- **Forge** - 5 Stone blocks (cross pattern)
- **Water** - Place water blocks in ocean biomes

## Game Mechanics

### Mining
- **Bare Hand**: Break wood blocks slowly, stone takes forever
- **Axe**: Cuts wood blocks 1.25x faster (uses durability)
- **Pickaxe**: Breaks stone blocks much faster (uses durability)

### Tools Durability
- **Axe**: 60 uses
- **Pickaxe**: 50 uses
- **Knife**: 40 uses (for future combat)

### Smelting
1. Place a Forge with 5 stone blocks
2. Right-click to open
3. Add fuel (wood/planks/sticks) to the fuel slot
4. Add items to smelt to the input slot
5. Collect smelted items from output slot

### Biomes
- **Forest**: Trees and grass terrain
- **Desert**: Sand and no trees
- **Ocean**: Water surfaces with sand beaches

### Physics
- Fall damage on drops > 5 blocks
- Water buoyancy and swimming
- Simple gravity and collision detection

## Modular Code Structure

Each Python file has a specific purpose:

- **constants.py** - Centralized config (screen size, physics, item definitions)
- **entities.py** - Game object classes with methods and serialization
- **inventory.py** - Crafting logic and item management
- **terrain.py** - Infinite terrain generation algorithms
- **assets.py** - Image/sprite loading with fallbacks
- **rendering.py** - Draw functions for UI and world
- **ui.py** - Menu screens and inventory UI
- **physics.py** - Collision, movement, gravity
- **main.py** - Game loop tying everything together

This modular approach makes it easy to:
- Add new items/recipes
- Create new biomes
- Extend crafting mechanics
- Modify game balance
- Port to web (Pygame → Pyodide)

## Save System

The game supports 3 save slots with automatic progress tracking:
- Player position and health
- All inventory items
- Placed blocks and forges
- Tree states
- Generated chunk info

Saves are compressed with gzip to reduce file size.

## Performance Features

- Chunk-based terrain generation (only visible chunks load)
- Entity culling (distant crabs despawn)
- Camera-based rendering (only draw visible objects)
- Cached sprite scaling
- Optimized collision detection

## Planned Features

- [ ] Combat system with sword
- [ ] More enemy types
- [ ] Mob spawning system
- [ ] Day/night cycle
- [ ] Weather effects
- [ ] More biomes (snow, jungle, mountains)
- [ ] Mob drops and loot
- [ ] More crafting recipes
- [ ] Animation improvements

## Web Version (Future)

This game can be compiled to WebAssembly using:
- Pygame → Pyodide
- Hosted on GitHub Pages
- No installation needed

See `index.html` for web version setup.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source. Texture and sprite assets may have separate licenses.

## Credits

- Built with [Pygame](https://www.pygame.org/)
- Inspired by Minecraft
- Procedural generation techniques

## Support

Found a bug or have a suggestion? Please open an issue on GitHub!

---

Made with ❤️ by developers who love pixel art and survival games
