# constants.py - All game configuration constants
import os

# Screen dimensions
WIDTH, HEIGHT = 640, 480
FPS = 60

# Physics
PLAYER_SPEED = 4
GRAVITY = 0.35
JUMP_SPEED = -7.5
MAX_FALL_SPEED = 12

# Animations
ANIMATION_INTERVAL = 100

# Tree mechanics
TREE_HITS_HAND = 10
TREE_HITS_AXE = 8
AXE_TREE_DAMAGE = TREE_HITS_HAND / TREE_HITS_AXE
TREE_BLOCK_HITS = 8
WOOD_BLOCK_HITS_AXE = 7
TREE_REGROW_TIME = 60000  # ms

# Player health and damage
PLAYER_MAX_HEALTH = 20
PLAYER_DAMAGE_COOLDOWN = 700
FALL_DAMAGE_START_BLOCKS = 5
PLAYER_DAMAGE_FLASH_MS = 220
PLAYER_DAMAGE_SHAKE_MS = 180
PLAYER_DAMAGE_SHAKE_PX = 5

# Enemy mechanics
CRAB_HITS_HAND = 3
CRAB_FLEE_DISTANCE = 150
CRAB_FLEE_SPEED = 1.8
CRAB_ACTIVE_UPDATE_RANGE = WIDTH * 2
CRAB_CULL_RANGE = WIDTH * 12
CRAB_GROUND_SINK_PX = 4
CRAB_JUMP_IMPULSE = -5.8
CRAB_GRAVITY = 0.38

# Block mechanics
STONE_HITS_HAND = 20
STONE_HITS_PICKAXE = 10
CRAFTING_TABLE_GROUND_SINK_PX = 9

# Terrain
TILE_SIZE = 32
GROUND_ROWS = 2
BIOME_TRANSITION_WIDTH = 3
WORLD_WIDTH = WIDTH * 6
CHUNK_WIDTH = WIDTH
CHUNK_TILES = CHUNK_WIDTH // TILE_SIZE
SURFACE_TILE_Y = (HEIGHT - GROUND_ROWS * TILE_SIZE) // TILE_SIZE
TERRAIN_DEPTH_ROWS = 28
SEED = 0xDEAD_BEEF

# Chunk management
MAX_LOADED_CHUNKS = 15
UNLOAD_DISTANCE_CHUNKS = 8

# Inventory
HOTBAR_SLOTS = 9
HOTBAR_SLOT_SIZE = 32
HOTBAR_Y = HEIGHT - 40
INVENTORY_COLS = 5
INVENTORY_ROWS = 4
INVENTORY_SLOT_SIZE = 48
CRAFTING_SMALL_COLS = 2
CRAFTING_SMALL_ROWS = 2
CRAFTING_LARGE_COLS = 3
CRAFTING_LARGE_ROWS = 3

# Save system
SAVE_SLOTS = 3

# Biomes
BIOME_NAMES = [
    "Green Forest",
    "Red Forest",
    "Mixed Forest",
    "Autumn Grove",
    "Sunbaked Desert",
    "Coastal Ocean",
]

TREE_WOOD_DROP_COUNT = 3
TREE_LEAF_DROP_COUNT = 2

# Colors
ITEM_COLORS = {
    "wood": (139, 69, 19),
    "leaves": (34, 139, 34),
    "planks": (178, 100, 30),
    "sticks": (170, 120, 70),
    "axe": (130, 130, 130),
    "crafting_table": (120, 75, 35),
    "forge": (100, 100, 100),
    "grass": (70, 150, 70),
    "jord": (110, 80, 50),
    "stone": (120, 120, 120),
    "sand": (224, 194, 135),
    "limestone": (210, 210, 200),
    "copper_ore": (184, 115, 51),
    "iron_ore": (156, 156, 156),
    "gold_ore": (212, 175, 55),
    "ruby": (170, 0, 0),
    "bedrock": (80, 80, 80),
    "knife": (150, 150, 150),
    "pickaxe": (140, 140, 140),
}

# Tool durability
TOOL_DURABILITY = {
    "axe": 60,
    "pickaxe": 50,
    "knife": 40,
}

# Smelting recipes
SMELT_RECIPES = {
    "wood": {"output": "planks", "smelt_time": 10000},
    "stone": {"output": "stone", "smelt_time": 14000},
    "jord": {"output": "stone", "smelt_time": 16000},
}

# Fuel recipes
FUEL_RECIPES = {
    "wood": {"burn_time": 15000},
    "planks": {"burn_time": 10000},
    "sticks": {"burn_time": 5000},
}

# File paths
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")
SAVE_DIR = os.path.join(BASE_DIR, "saves")
