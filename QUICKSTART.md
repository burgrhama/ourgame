# Quick Start Guide

## 🎮 For Players - Run the Game

### Windows/Mac/Linux

1. **Install Python 3.8+**
   - Download from https://www.python.org/

2. **Download the game**
   ```bash
   git clone https://github.com/yourusername/pixel-survival-game.git
   cd pixel-survival-game
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Play!**
   ```bash
   python main.py
   ```

---

## 👨‍💻 For Developers - Modify the Game

### Adding a New Crafting Recipe

Edit `inventory.py`:
```python
CRAFTING_RECIPES = [
    # ... existing recipes ...
    {
        "name": "diamond_sword",
        "type": "shaped",
        "pattern": [
            "D",
            "D",
            "S",
        ],
        "key": {"D": "diamond", "S": "sticks"},
        "output": {"diamond_sword": 1},
        "mirror": False,
    },
]
```

### Adding a New Biome

Edit `terrain.py`:
```python
BIOMES.append([
    ("leaves1", "wood"),
    ("leaves2", "wood"),
    # ...
])
BIOME_TYPES.append("snowy_forest")
```

### Changing Game Physics

Edit `constants.py`:
```python
GRAVITY = 0.35  # Higher = faster falling
JUMP_SPEED = -7.5  # More negative = higher jump
PLAYER_SPEED = 4  # Player movement speed
```

### Adding a New Enemy

Create in `entities.py`:
```python
class Zombie:
    def __init__(self, x):
        self.x = float(x)
        self.health = 10
        # ...
```

Then spawn in `terrain.py` similar to crabs.

---

## 📁 Project Files Explained

| File | Does What |
|------|-----------|
| `main.py` | Game loop & state management |
| `constants.py` | All game settings |
| `entities.py` | Player, enemies, objects |
| `inventory.py` | Crafting & items |
| `terrain.py` | World generation |
| `assets.py` | Texture/sprite loading |
| `rendering.py` | Drawing & UI |
| `index.html` | Website landing page |

---

## 🔧 Build & Deploy

### Local Testing
```bash
python main.py
```

### Push to GitHub
```bash
git add .
git commit -m "Your changes"
git push origin main
```

### Deploy Website
1. Go to GitHub repo settings
2. Enable "GitHub Pages"
3. Select "main branch" as source
4. Your site is live at `yourusername.github.io/pixel-survival-game/`

---

## 🎯 Common Tasks

### Change screen size
Edit `constants.py`:
```python
WIDTH, HEIGHT = 1280, 720  # Larger screen
```

### Modify tool durability
Edit `constants.py`:
```python
TOOL_DURABILITY = {
    "axe": 100,  # More uses
    "pickaxe": 75,
    "knife": 60,
}
```

### Add item to inventory  
Edit `inventory.py`:
```python
def create_inventory():
    return {
        # ... existing items ...
        "diamond": 0,  # New item!
        "emerald": 0,
    }
```

### Change fall damage
Edit `constants.py`:
```python
FALL_DAMAGE_START_BLOCKS = 3  # Take damage from 3 blocks instead of 5
```

---

## 🐛 Debugging

### Enable debug info in-game
Press **F9** during gameplay to show:
- FPS
- Player coordinates
- Current biome

### Check logs
Look at console output for errors. Common issues:
- Missing `models/` folder
- Missing texture files
- Python version too old

### Clear cache
```bash
rm -rf __pycache__
rm -rf .pytest_cache
```

---

## 📚 Learn More

- **Game Development**: [Pygame Docs](https://www.pygame.org/docs/)
- **Python**: [Python.org](https://www.python.org/)
- **Procedural Generation**: [Perlin Noise](https://en.wikipedia.org/wiki/Perlin_noise)

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/cool-new-thing`
3. Make changes
4. Test locally: `python main.py`
5. Commit: `git commit -m "Add cool new thing"`
6. Push: `git push origin feature/cool-new-thing`
7. Open a Pull Request

---

## ❓ FAQ

**Q: Can I run this without Python?**  
A: Not yet, but a web version is coming!

**Q: Can I modify the code for my own game?**  
A: Yes! Fork it and make it your own.

**Q: How do I add more save slots?**  
A: Edit `constants.py` and change `SAVE_SLOTS = 3` to higher number.

**Q: What's the max world size?**  
A: Infinite! Terrain generates on-demand.

---

Happy coding! 🎮✨
