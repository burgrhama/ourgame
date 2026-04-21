import os
import json
import gzip
import math
import random
import pygame

global hotbar_items

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")
PLAYER_SPRITES = {
    "stand_right": ["MC-stand-still-look-right.png"],
    "stand_left": ["MC-stand-still-look-left.png"],
    "walk_right": [
        "MC-walk-right-main.png",
        "MC-walk-right-main-2.png",
        "MC-walk-right-main-3.png",
        "MC-walk-right.png",
    ],
    "walk_left": [
        "MC-walk-left-main.png",
        "MC-walk-left-main-2.png",
        "MC-walk-left-main-3.png",
        "MC-walk-left.png",
    ],
    "jump_right": ["Hop-til-højre.png"],
    "jump_left": ["Hop-til-venstre.png"],
}
TILE_FILENAMES = {
    "grass": "Overgang-Grass-Jord.png",
    "jord": "Jord.png",
    "transition": "Overgang-Grass-Jord.png",
    "stone": "Stone.png",
    "sand": "Sand.png",
    "limestone": "Limestone.png",
    "copper_ore": "Copper-ore.png",
    "iron_ore": "Iron-ore.png",
    "gold_ore": "Gold-ore.png",
    "ruby": "Ruby.png",
    "bedrock": "Bedrock.png",
}
TREE_FILENAMES = {
    "leaves1": "leaves1.png",
    "leaves2": "leaves2.png",
    "red_leaves": "red-leaves.png",
    "wood": "wood.png",
    "wood_hole": "wood-with-hole.png",
}
SKY_FILENAMES = {
    "sky": "Sky.png",
    "sky_top": "Toppen-af-himmlen.png",
    "cloud": "cloud-type-1.png",
}
CRAB_FILENAMES = {
    "stand": "Crab-stand.png",
    "bob": "Crab-stand-bobing.png",
}
ITEM_FILENAMES = {
    "planks": "PLANKS.png",
    "axe": "Wood-pickaxe-up-standart.png",
    "axe_left": "Wood-pickaxe-left.png",
    "axe_right": "Wood-pickaxe-right.png",
    "crafting_table": "Crafting-table.png",
    "knife": "knife.png",
    "Pickaxe": "Pickaxe.png",
    "water_top": "watertop.png",
    "water_bottom": "waterbottom.png",
}
FORGE_FILENAMES = {
    "idle": "Forge.png",
    "idle_bobing": "Forge-bobing.png",
    "fire": "Forge-fire.png",
    "fire_bobing": "Forge-fire-bobing.png",
}
MAIN_NAME_FILENAME = "title.png"

WIDTH, HEIGHT = 640, 480
FPS = 60
PLAYER_SPEED = 4
TILE_SIZE = 32
GROUND_ROWS = 2
GRAVITY = 0.35
JUMP_SPEED = -7.5
MAX_FALL_SPEED = 12
ANIMATION_INTERVAL = 100
TREE_HITS_HAND = 10
TREE_HITS_AXE = 8
AXE_TREE_DAMAGE = TREE_HITS_HAND / TREE_HITS_AXE
TREE_BLOCK_HITS = 8
WOOD_BLOCK_HITS_AXE = 7
TREE_REGROW_TIME = 60000  # ms until a cut tree regrows
PLAYER_MAX_HEALTH = 20
PLAYER_DAMAGE_COOLDOWN = 700  # ms of invulnerability after getting hit
FALL_DAMAGE_START_BLOCKS = 5
PLAYER_DAMAGE_FLASH_MS = 220
PLAYER_DAMAGE_SHAKE_MS = 180
PLAYER_DAMAGE_SHAKE_PX = 5
STONE_HITS_HAND = 20
STONE_HITS_PICKAXE = 10
CRAB_HITS_HAND = 3
CRAB_FLEE_DISTANCE = 150
CRAB_FLEE_SPEED = 1.8
CRAB_ACTIVE_UPDATE_RANGE = WIDTH * 2
CRAB_CULL_RANGE = WIDTH * 12
CRAB_GROUND_SINK_PX = 4
CRAFTING_TABLE_GROUND_SINK_PX = 9
CRAB_JUMP_IMPULSE = -5.8
CRAB_GRAVITY = 0.38
TREE_WOOD_DROP_COUNT = 3
TREE_LEAF_DROP_COUNT = 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Pixel Art Game")
clock = pygame.time.Clock()

SAVE_DIR = os.path.join(BASE_DIR, "saves")
SAVE_SLOTS = 3


def load_sprite(path):
    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (48, 48))
    return None


def create_placeholder(color):
    sprite = pygame.Surface((48, 48), pygame.SRCALPHA)
    sprite.fill(color)
    pygame.draw.rect(sprite, (0, 0, 0), sprite.get_rect(), 2)
    return sprite


def load_player_sprites():
    sprites = {}
    for key, filenames in PLAYER_SPRITES.items():
        frame_list = []
        for filename in filenames:
            path = os.path.join(MODEL_DIR, filename)
            loaded = load_sprite(path)
            if loaded is None:
                fallback_color = (120, 120, 255) if key.startswith("stand") else (180, 180, 255)
                loaded = create_placeholder(fallback_color)
            frame_list.append(loaded)
        sprites[key] = frame_list
    return sprites


def load_tile_images():
    tiles = {}
    for key, filename in TILE_FILENAMES.items():
        path = os.path.join(MODEL_DIR, filename)
        loaded = load_sprite(path)
        if loaded is None:
            fallback = (70, 130, 180) if key == "water" else (140, 90, 60)
            loaded = create_placeholder(fallback)
        tiles[key] = pygame.transform.scale(loaded, (TILE_SIZE, TILE_SIZE))
    return tiles


def load_tree_images():
    trees = {}
    for key, filename in TREE_FILENAMES.items():
        path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            trees[key] = image
        else:
            trees[key] = create_placeholder((100, 150, 80))
    return trees


def load_sky_images():
    sky_imgs = {}
    for key, filename in SKY_FILENAMES.items():
        path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            sky_imgs[key] = image
        else:
            sky_imgs[key] = create_placeholder((100, 150, 200))
    return sky_imgs


def load_item_images():
    items = {}
    for key, filename in ITEM_FILENAMES.items():
        path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(path):
            items[key] = pygame.image.load(path).convert_alpha()
        else:
            items[key] = None
    return items


def load_crab_sprites():
    sprites = {}
    for key, filename in CRAB_FILENAMES.items():
        path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            sprites[key] = pygame.transform.scale(image, (42, 30))
        else:
            sprites[key] = create_placeholder((180, 80, 60))
    return sprites


def load_forge_images():
    forges = {}
    for key, filename in FORGE_FILENAMES.items():
        path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            forges[key] = image
        else:
            forges[key] = create_placeholder((150, 150, 100))
    return forges


def load_main_name_image():
    path = os.path.join(MODEL_DIR, MAIN_NAME_FILENAME)
    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (420, 100))
    return None


class Tree:
    BLOCK_LAYOUT = [
        ("leaves", 0, 0),
        ("leaves", TILE_SIZE, 0),
        ("leaves", 0, TILE_SIZE),
        ("leaves", TILE_SIZE, TILE_SIZE),
        ("wood", 16, TILE_SIZE),
        ("wood", 16, TILE_SIZE * 2),
        ("wood", 16, TILE_SIZE * 3),
    ]

    def __init__(self, x, y, leaves_type="leaves1", wood_type="wood"):
        self.x = x
        self.y = y
        self.leaves_type = leaves_type
        self.wood_type = wood_type
        self.height = TILE_SIZE * 4
        self.width = 64
        self.broken_blocks = set()
        self.block_damage = {}
        self.health = float(len(self.BLOCK_LAYOUT))
        self.max_health = float(len(self.BLOCK_LAYOUT))
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def sync_to_surface(self):
        trunk_x = self.x + self.width // 2
        self.y = get_surface_world_y(trunk_x) - self.height
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface, camera_x=0, camera_y=0):
        self.sync_to_surface()
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        if draw_x < -150 or draw_x > WIDTH + 150 or draw_y < -220 or draw_y > HEIGHT + 80:
            return
        # Draw wood first, then leaves so leaves visually overlap wood.
        draw_order = ["wood", "leaves"]
        for layer_type in draw_order:
            for idx, (block_type, off_x, off_y) in enumerate(self.BLOCK_LAYOUT):
                if block_type != layer_type:
                    continue
                if idx in self.broken_blocks:
                    continue
                tile = get_item_surface(block_type, TILE_SIZE)
                surface.blit(tile, (draw_x + off_x, draw_y + off_y))

    def break_block_at(self, world_x, world_y):
        self.sync_to_surface()
        for idx, (block_type, off_x, off_y) in enumerate(self.BLOCK_LAYOUT):
            if idx in self.broken_blocks:
                continue
            rect = pygame.Rect(int(self.x + off_x), int(self.y + off_y), TILE_SIZE, TILE_SIZE)
            if rect.collidepoint(world_x, world_y):
                hits = self.block_damage.get(idx, 0) + 1
                self.block_damage[idx] = hits
                selected_item = hotbar_items[hotbar_selected]
                has_axe = selected_item and selected_item.get("type") == "axe" and inventory.get("axe", 0) > 0
                needed_hits = WOOD_BLOCK_HITS_AXE if block_type == "wood" and has_axe else TREE_BLOCK_HITS
                if hits < needed_hits:
                    return None
                self.block_damage.pop(idx, None)
                self.broken_blocks.add(idx)
                self.health = float(self.max_health - len(self.broken_blocks))
                
                # Use tool durability if axe was used
                if has_axe:
                    use_tool("axe")
                
                return block_type
        return None

    def is_fully_broken(self):
        return len(self.broken_blocks) >= len(self.BLOCK_LAYOUT)


class Forge:
    """Minecraft-style furnace/forge for smelting items."""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.width = TILE_SIZE * 3
        self.height = TILE_SIZE * 2
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Smelting state
        self.input_item = None  # {"type": item_type, "count": count}
        self.fuel_item = None   # {"type": item_type, "count": count}
        self.output_items = {}  # {item_type: count}
        
        # Timers
        self.fuel_remaining_ms = 0  # How long current fuel will burn
        self.smelt_progress_ms = 0  # Time spent smelting current item
        self.is_smelting = False
    
    def try_start_smelt(self):
        """Attempt to start smelting if conditions are met."""
        if self.is_smelting or not self.input_item or self.fuel_remaining_ms <= 0:
            return
        
        item_type = self.input_item["type"]
        recipe = get_smelt_recipe(item_type)
        if not recipe:
            return
        
        self.is_smelting = True
        self.smelt_progress_ms = 0
    
    def update(self, delta_ms):
        """Update smelting and fuel state."""
        if self.fuel_remaining_ms > 0:
            self.fuel_remaining_ms = max(0, self.fuel_remaining_ms - delta_ms)
        
        if self.is_smelting:
            self.smelt_progress_ms += delta_ms
            item_type = self.input_item["type"] if self.input_item else None
            recipe = get_smelt_recipe(item_type) if item_type else None
            
            if recipe and self.smelt_progress_ms >= recipe.get("smelt_time", 10000):
                output_type = recipe["output"]
                self.output_items[output_type] = self.output_items.get(output_type, 0) + 1
                self.input_item["count"] -= 1
                if self.input_item["count"] <= 0:
                    self.input_item = None
                self.is_smelting = False
                self.smelt_progress_ms = 0
                self.try_start_smelt()
            elif self.fuel_remaining_ms <= 0:
                self.is_smelting = False
                self.smelt_progress_ms = 0
        
        if not self.is_smelting and self.fuel_remaining_ms > 0 and self.input_item:
            self.try_start_smelt()
        
        if self.fuel_remaining_ms <= 0 and self.fuel_item:
            self.fuel_item = None
    
    def add_fuel(self, item_type):
        """Add fuel to the forge."""
        fuel_recipe = get_fuel_recipe(item_type)
        if not fuel_recipe:
            return False
        
        if self.fuel_item and self.fuel_item["type"] != item_type:
            return False
        self.fuel_item = self.fuel_item or {"type": item_type, "count": 0}
        self.fuel_item["count"] += 1
        self.fuel_remaining_ms += fuel_recipe.get("burn_time", 10000)
        return True
    
    def add_input(self, item_type):
        """Add an item to be smelted."""
        recipe = get_smelt_recipe(item_type)
        if not recipe:
            return False
        if self.input_item and self.input_item["type"] != item_type:
            return False
        self.input_item = self.input_item or {"type": item_type, "count": 0}
        self.input_item["count"] += 1
        self.try_start_smelt()
        return True
    
    def collect_output(self):
        collected = dict(self.output_items)
        self.output_items.clear()
        return collected
    
    def get_smelting_progress(self):
        """Return progress 0-1 of current smelting."""
        if not self.is_smelting or not self.input_item:
            return 0.0
        
        recipe = get_smelt_recipe(self.input_item["type"])
        if not recipe:
            return 0.0
        
        smelt_time = recipe.get("smelt_time", 10000)
        return min(1.0, self.smelt_progress_ms / smelt_time)


class Crab:
    def __init__(self, x):
        self.x = float(x)
        self.width = 42
        self.height = 30
        self.direction = random.choice([-1, 1])
        self.speed = 0.55
        self.y = get_surface_world_y(self.x) - self.height
        self.move_until = pygame.time.get_ticks() + random.randint(900, 2200)
        self.pause_until = 0
        self.frame_toggle = False
        self.health = CRAB_HITS_HAND
        self.flee_until = 0
        self.vy = 0.0
        self.airborne = False

    def update(self, current_time):
        distance_to_player = player_world_x - self.x
        flee_player = abs(distance_to_player) < CRAB_FLEE_DISTANCE or current_time < self.flee_until

        if flee_player:
            self.direction = -1 if distance_to_player > 0 else 1
            move_speed = CRAB_FLEE_SPEED
        else:
            if current_time >= self.move_until and current_time >= self.pause_until:
                self.pause_until = current_time + random.randint(600, 1600)
                self.move_until = self.pause_until + random.randint(900, 2200)
                self.direction = random.choice([-1, 1])
            move_speed = self.speed if current_time >= self.pause_until else 0.0

        if self.airborne:
            self.vy += CRAB_GRAVITY
            self.y += self.vy

            # Keep some horizontal momentum while airborne.
            if move_speed > 0:
                test_x = self.x + self.direction * move_speed * 0.7
                body_rect = pygame.Rect(int(test_x), int(self.y), self.width, self.height)
                if not any(body_rect.colliderect(r) for r in get_local_solid_rects(body_rect.centerx, body_rect.centery)):
                    self.x = test_x

            settle_y = get_crab_ground_y(self.x, self.width, self.height, self.y)
            if settle_y is not None and self.vy >= 0 and self.y >= settle_y:
                self.y = settle_y
                self.vy = 0.0
                self.airborne = False
        elif move_speed > 0:
            next_x = self.x + self.direction * move_speed
            moved = False

            # Normal forward move on current level.
            if crab_position_valid(next_x, self.y, self.width, self.height):
                self.x = next_x
                moved = True
            else:
                # Try stepping up to one full tile.
                for step_up in range(4, TILE_SIZE + 1, 4):
                    try_y = self.y - step_up
                    if crab_position_valid(next_x, try_y, self.width, self.height):
                        self.x = next_x
                        self.y = try_y
                        moved = True
                        break

            if not moved:
                self.direction *= -1

            settle_y = get_crab_ground_y(self.x, self.width, self.height, self.y)
            if settle_y is not None:
                self.y = settle_y
        else:
            settle_y = get_crab_ground_y(self.x, self.width, self.height, self.y)
            if settle_y is not None:
                self.y = settle_y

        self.frame_toggle = (current_time // 280) % 2 == 1 and move_speed == 0

    def jump_on_hit(self):
        self.airborne = True
        self.vy = CRAB_JUMP_IMPULSE

    def get_world_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface, camera_x, camera_y):
        draw_x = int(self.x - camera_x)
        draw_y = int(self.y - camera_y + CRAB_GROUND_SINK_PX)
        if draw_x < -self.width or draw_x > WIDTH + self.width or draw_y < -self.height or draw_y > HEIGHT + self.height:
            return

        sprite_key = "bob" if self.frame_toggle else "stand"
        sprite = crab_sprites[sprite_key].copy()
        if self.direction < 0:
            sprite = pygame.transform.flip(sprite, True, False)
        surface.blit(sprite, (draw_x, draw_y))


tile_images = load_tile_images()
tree_images = load_tree_images()
sky_images = load_sky_images()
item_images = load_item_images()
crab_sprites = load_crab_sprites()
forge_images = load_forge_images()
main_name_image = load_main_name_image()
ground_top = HEIGHT - GROUND_ROWS * TILE_SIZE
sky_top_height = TILE_SIZE
player_sprites = load_player_sprites()
player_rect = player_sprites["stand_right"][0].get_rect(midbottom=(WIDTH // 2, ground_top - 8))
player_world_x = WIDTH // 2
player_direction = "right"
player_moving = False
player_frame = 0
player_last_frame_time = pygame.time.get_ticks()
player_vel_y = 0
player_fall_start_bottom = None
player_health = PLAYER_MAX_HEALTH
player_last_damage_time = -PLAYER_DAMAGE_COOLDOWN
player_death_message_until = 0
player_damage_flash_until = 0
last_water_spread_time = -999999
player_damage_shake_until = 0
last_crab_cleanup_time = 0
dropped_items = []
show_info = False
is_fullscreen = False
info_font = pygame.font.Font(None, 20)
button_font = pygame.font.Font(None, 16)

# Menu UI
menu_button_font = pygame.font.Font(None, 30)
menu_small_font = pygame.font.Font(None, 24)
menu_new_button_rect = pygame.Rect(60, 300, 180, 44)
menu_save_button_rect = pygame.Rect(60, 356, 180, 44)
menu_slot_rects = [pygame.Rect(300, 220 + i * 65, 280, 54) for i in range(SAVE_SLOTS)]
menu_selected_slot = 1
menu_status_text = ""
menu_status_until = 0

# Fullscreen button
fullscreen_button_rect = pygame.Rect(WIDTH - 90, 10, 80, 30)
fullscreen_button_color = (100, 100, 100)
fullscreen_button_hover_color = (150, 150, 150)

# Inventory and hotbar
inventory = {
    "wood": 0,
    "leaves": 0,
    "planks": 0,
    "sticks": 0,
    "axe": 0,
    "crafting_table": 0,
    "forge": 0,
    "grass": 0,
    "jord": 0,
    "stone": 0,
    "sand": 0,
    "limestone": 0,
    "copper_ore": 0,
    "iron_ore": 0,
    "gold_ore": 0,
    "ruby": 0,
    "knife": 0,
    "pickaxe": 0,
}
hotbar_slots = 9
hotbar_selected = 0
# Available hotbar items (items that can appear in hotbar when crafted)
AVAILABLE_HOTBAR_ITEMS = [
    {"type": "wood", "name": "Wood"},
    {"type": "leaves", "name": "Leaves"},
    {"type": "planks", "name": "Planks"},
    {"type": "axe", "name": "Axe"},
    {"type": "crafting_table", "name": "Crafting Table"},
    {"type": "forge", "name": "Forge"},
    {"type": "stone", "name": "Stone"},
    {"type": "knife", "name": "Knife"},
    {"type": "pickaxe", "name": "Pickaxe"},
]

def get_hotbar_items():
    """Generate hotbar items dynamically based on inventory and available items."""
    hotbar_items = [None] * hotbar_slots
    slot_index = 0
    
    # Add items that player has in inventory to hotbar
    for item in AVAILABLE_HOTBAR_ITEMS:
        if inventory.get(item["type"], 0) > 0 and slot_index < hotbar_slots:
            hotbar_items[slot_index] = item
            slot_index += 1
    
    return hotbar_items

# Initialize hotbar_items
hotbar_items = get_hotbar_items()
HOTBAR_SLOT_SIZE = 32
HOTBAR_Y = HEIGHT - 40
PLACEABLE_ITEMS = {
    "wood",
    "leaves",
    "planks",
    "crafting_table",
    "forge",
    "stone",
    "jord",
    "grass",
    "sand",
    "limestone",
    "copper_ore",
    "iron_ore",
    "gold_ore",
    "ruby",
    "bedrock",
}

# Fix 10: Add tool durability system
TOOL_DURABILITY = {
    "axe": 60,  # Number of uses
    "pickaxe": 50,
    "knife": 40,
}

tool_durability = {}  # Track durability of each tool instance

def use_tool(tool_type):
    """Reduce tool durability and break if depleted."""
    if tool_type not in TOOL_DURABILITY:
        return True
    
    durability = tool_durability.get(tool_type, TOOL_DURABILITY[tool_type])
    durability -= 1
    
    if durability <= 0:
        # Tool breaks
        inventory[tool_type] = max(0, inventory.get(tool_type, 0) - 1)
        if tool_type in tool_durability:
            del tool_durability[tool_type]
        return False
    
    tool_durability[tool_type] = durability
    return True

# Crafting recipes (Minecraft-style)
CRAFTING_RECIPES = [
    {
        "name": "planks",
        "type": "shapeless",
        "input": {"wood": 1},
        "output": {"planks": 4},
    },
    {
        "name": "sticks",
        "type": "shaped",
        "pattern": [
            "P",
            "P",
        ],
        "key": {"P": "planks"},
        "output": {"sticks": 4},
        "mirror": False,
    },
    {
        "name": "crafting_table",
        "type": "shaped",
        "pattern": [
            "PP",
            "PP",
        ],
        "key": {"P": "planks"},
        "output": {"crafting_table": 1},
        "mirror": False,
    },
    {
        "name": "forge",
        "type": "shaped",
        "pattern": [
            " P ",
            "P P",
            "P P",
        ],
        "key": {"P": "stone"},
        "output": {"forge": 1},
        "mirror": False,
    },
    {
        "name": "axe",
        "type": "shaped",
        "pattern": [
            "PP ",
            "PS ",
            " S ",
        ],
        "key": {"P": "planks", "S": "sticks"},
        "output": {"axe": 1},
        "mirror": True,
    },
    {
        "name": "knife",
        "type": "shaped",
         "pattern": [
            "P",
            "P",
            "S",
],
        "key": {"P": "planks", "S": "sticks"},
        "output": {"knife": 1},
        "mirror": False,
    },
    {
        "name": "pickaxe",
        "type": "shaped",
        "pattern": [
            "PPP",
            " S ",
            " S ",
        ],
        "key": {"P": "planks", "S": "sticks"},
        "output": {"pickaxe": 1},
        "mirror": False,
    },
]

# Smelting recipes - item_type: {output: output_type, smelt_time: ms}
SMELT_RECIPES = {
    "wood": {"output": "planks", "smelt_time": 10000},
    "stone": {"output": "stone", "smelt_time": 14000},  # Stone becomes smooth stone
    "jord": {"output": "stone", "smelt_time": 16000},   # Dirt becomes baked clay-like
}

# Fuel recipes - item_type: {burn_time: ms}
FUEL_RECIPES = {
    "wood": {"burn_time": 15000},
    "planks": {"burn_time": 10000},
    "sticks": {"burn_time": 5000},
}


def get_smelt_recipe(item_type):
    """Get smelting recipe for an item type."""
    return SMELT_RECIPES.get(item_type)


def get_fuel_recipe(item_type):
    """Get fuel recipe for an item type."""
    return FUEL_RECIPES.get(item_type)


def apply_fall_damage(fall_distance):
    """Apply fall damage to the player based on fall distance."""
    if fall_distance > FALL_DAMAGE_START_BLOCKS * TILE_SIZE:
        damage = min(10, (fall_distance - FALL_DAMAGE_START_BLOCKS * TILE_SIZE) // (TILE_SIZE // 2))
        global player_health, player_damage_flash_until, player_damage_shake_until, player_death_message_until
        player_health -= damage
        player_damage_flash_until = pygame.time.get_ticks() + PLAYER_DAMAGE_FLASH_MS
        player_damage_shake_until = pygame.time.get_ticks() + PLAYER_DAMAGE_SHAKE_MS
        if player_health <= 0:
            player_health = PLAYER_MAX_HEALTH
            # Respawn logic could be added here
            player_death_message_until = pygame.time.get_ticks() + 3000


def spread_water():
    """Spread water like Minecraft - flows down and horizontally."""
    global placed_blocks
    new_water = []
    water_blocks = [b for b in placed_blocks if b["type"] == "water"]
    
    for water in water_blocks:
        water_x = int(water["x"] // TILE_SIZE)
        water_y = int(water["y"] // TILE_SIZE)
        
        # Flow downward
        below_y = water_y + 1
        below_pos = (water_x * TILE_SIZE, below_y * TILE_SIZE)
        if not any(b["x"] == below_pos[0] and b["y"] == below_pos[1] and b["type"] == "water" for b in placed_blocks):
            if not any(b["x"] == below_pos[0] and b["y"] == below_pos[1] and b["type"] != "water" for b in placed_blocks):
                # No block below, check if it's air or terrain
                if not get_terrain_tile(water_x, below_y):
                    new_water.append({"x": below_pos[0], "y": below_pos[1], "type": "water"})
        
        # Flow horizontally (limited distance)
        for dx in [-1, 1]:
            side_x = water_x + dx
            side_pos = (side_x * TILE_SIZE, water_y * TILE_SIZE)
            if not any(b["x"] == side_pos[0] and b["y"] == side_pos[1] and b["type"] == "water" for b in placed_blocks):
                if not any(b["x"] == side_pos[0] and b["y"] == side_pos[1] and b["type"] != "water" for b in placed_blocks):
                    if not get_terrain_tile(side_x, water_y):
                        new_water.append({"x": side_pos[0], "y": side_pos[1], "type": "water"})
    
    # Add new water blocks
    for w in new_water:
        if not any(b["x"] == w["x"] and b["y"] == w["y"] and b["type"] == "water" for b in placed_blocks):
            placed_blocks.append(w)


def is_player_in_water(player_world_x, player_rect):
    """Check if player is in water by colliding with water blocks."""
    player_rect_world = pygame.Rect(int(player_world_x - player_rect.width // 2), int(player_rect.y), player_rect.width, player_rect.height)
    for block in placed_blocks:
        if block["type"] == "water":
            if player_rect_world.colliderect(get_block_world_rect(block)):
                return True
    return False


# Item colors/textures for display
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

# Item textures mapping
ITEM_TEXTURES = {
    "wood": "wood",
    "leaves": "leaves1",
    "planks": "planks",
    "axe": "axe",
    "sticks": None,
    "crafting_table": None,
    "sand": "sand",
    "limestone": "limestone",
    "copper_ore": "copper_ore",
    "iron_ore": "iron_ore",
    "gold_ore": "gold_ore",
    "ruby": "ruby",
    "bedrock": "bedrock",
    "knife": "knife",
    "pickaxe": "pickaxe",
}

def get_item_surface(item_type, size=40):
    """Get a pygame surface for an item (texture or color)"""
    if item_type == "grass" and tile_images.get("grass"):
        img = pygame.transform.scale(tile_images["grass"], (size, size))
        return img.copy()
    elif item_type == "jord" and tile_images.get("jord"):
        img = pygame.transform.scale(tile_images["jord"], (size, size))
        return img.copy()
    elif item_type == "stone" and tile_images.get("stone"):
        img = pygame.transform.scale(tile_images["stone"], (size, size))
        return img.copy()
    elif item_type in {"sand", "limestone", "copper_ore", "iron_ore", "gold_ore", "ruby"} and tile_images.get(item_type):
        img = pygame.transform.scale(tile_images[item_type], (size, size))
        return img.copy()
    elif item_type == "wood" and tree_images.get("wood"):
        img = pygame.transform.scale(tree_images["wood"], (size, size))
        return img.copy()
    elif item_type == "leaves" and tree_images.get("leaves1"):
        img = pygame.transform.scale(tree_images["leaves1"], (size, size))
        return img.copy()
    elif item_type == "planks" and item_images.get("planks"):
        img = pygame.transform.scale(item_images["planks"], (size, size))
        return img.copy()
    elif item_type == "axe" and item_images.get("axe"):
        img = pygame.transform.scale(item_images["axe"], (size, size))
        return img.copy()
    elif item_type == "crafting_table" and item_images.get("crafting_table"):
        img = pygame.transform.scale(item_images["crafting_table"], (size, size))
        return img.copy()
    elif item_type == "crafting_table":
        surface = pygame.Surface((size, size))
        surface.fill((120, 75, 35))
        pygame.draw.rect(surface, (85, 50, 25), (0, 0, size, size), 2)
        pygame.draw.line(surface, (90, 55, 30), (0, size // 2), (size, size // 2), 1)
        pygame.draw.line(surface, (90, 55, 30), (size // 2, 0), (size // 2, size), 1)
        return surface
    elif item_type == "forge" and forge_images.get("idle"):
        img = pygame.transform.scale(forge_images["idle"], (size, size))
        return img.copy()
    elif item_type == "forge":
        surface = pygame.Surface((size, size))
        surface.fill((100, 100, 100))
        pygame.draw.rect(surface, (60, 60, 60), (0, 0, size, size), 2)
        # Draw a simple furnace icon
        pygame.draw.rect(surface, (80, 80, 80), (4, 4, size - 8, size - 8))
        pygame.draw.rect(surface, (200, 100, 50), (size // 4, size // 4, size // 2, size // 2))  # Fire color
        return surface
    elif item_type == "water_top" and item_images.get("water_top"):
        img = pygame.transform.scale(item_images["water_top"], (size, size))
        return img.copy()
    elif item_type == "water_bottom" and item_images.get("water_bottom"):
        img = pygame.transform.scale(item_images["water_bottom"], (size, size))
        return img.copy()
    elif item_type == "water" and item_images.get("water_top"):
        img = pygame.transform.scale(item_images["water_top"], (size, size))
        return img.copy()
    else:
        # Fallback to color
        surface = pygame.Surface((size, size))
        color = ITEM_COLORS.get(item_type, (100, 100, 100))
        surface.fill(color)
        return surface

# Game states
GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_INVENTORY = "inventory"
GAME_STATE_FORGE = "forge"
current_state = GAME_STATE_MENU

# Inventory grid
INVENTORY_COLS = 5
INVENTORY_ROWS = 4
INVENTORY_SLOT_SIZE = 48
CRAFTING_SMALL_COLS = 2
CRAFTING_SMALL_ROWS = 2
CRAFTING_LARGE_COLS = 3
CRAFTING_LARGE_ROWS = 3
CRAFTING_COLS = CRAFTING_LARGE_COLS
CRAFTING_ROWS = CRAFTING_LARGE_ROWS
using_crafting_table = False

# Drag and drop state
drag_item = None
drag_source = None
crafting_grid = [[None for _ in range(CRAFTING_COLS)] for _ in range(CRAFTING_ROWS)]

# Block placement
placed_blocks = []  # List of {"x": world_x, "y": world_y, "type": item_type}
placed_forges = []  # List of Forge objects for active smelting
opened_forge = None  # Currently open forge for UI, or None

class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface, camera_x, camera_y):
        if sky_images["cloud"]:
            cloud = pygame.transform.scale(sky_images["cloud"], (80, 40))
            draw_x = self.x - camera_x
            draw_y = self.y - camera_y
            surface.blit(cloud, (draw_x, draw_y))

clouds = [
    Cloud(50, 40),
    Cloud(200, 60),
    Cloud(400, 30),
    Cloud(580, 50),
]

# Fix 11: Add configuration constants for magic numbers
# Replace magic numbers with named constants

BIOME_TRANSITION_WIDTH = 3  # Number of tiles for smooth biome transitions

BIOME_NAMES = [
    "Green Forest",
    "Red Forest",
    "Mixed Forest",
    "Autumn Grove",
    "Sunbaked Desert",
    "Coastal Ocean",
]
BIOMES = [
    [("leaves1", "wood"), ("leaves2", "wood"), ("leaves1", "wood"), ("red_leaves", "wood")],
    [("red_leaves", "wood"), ("red_leaves", "wood_hole"), ("red_leaves", "wood"), ("red_leaves", "wood")],
    [("leaves2", "wood"), ("leaves1", "wood"), ("leaves2", "wood_hole"), ("leaves1", "wood")],
    [("leaves1", "wood_hole"), ("red_leaves", "wood"), ("leaves2", "wood"), ("red_leaves", "wood_hole")],
    [],  # Desert biome has no trees, only sand dunes
    [],  # Ocean biome uses shallow sandy shorelines and water
]
BIOME_TYPES = [
    "forest",
    "forest",
    "forest",
    "forest",
    "desert",
    "ocean",
]
WORLD_WIDTH = WIDTH * len(BIOMES)
CHUNK_WIDTH = WIDTH  # one chunk per screen-width
_CHUNK_SEED = 0xDEAD_BEEF
CHUNK_TILES = CHUNK_WIDTH // TILE_SIZE
SURFACE_TILE_Y = ground_top // TILE_SIZE
TERRAIN_DEPTH_ROWS = 28


def get_surface_tile_y(tile_x):
    broad_hills = math.sin(tile_x * 0.075) * 1.4
    small_hills = math.sin(tile_x * 0.21 + 1.4) * 0.9
    mountain_band = (max(0.0, math.sin(tile_x * 0.032 - 0.8)) ** 3) * 7.5
    ridge_band = (max(0.0, math.sin(tile_x * 0.017 + 2.1)) ** 4) * 9.0
    surface_offset = broad_hills + small_hills - mountain_band - ridge_band
    return max(5, min(SURFACE_TILE_Y + 2, SURFACE_TILE_Y + int(round(surface_offset))))


def get_surface_world_y(world_x):
    tile_x = int(world_x // TILE_SIZE)
    return get_surface_tile_y(tile_x) * TILE_SIZE


def carve_ellipse(tile_map, center_x, center_y, radius_x, radius_y):
    min_x = int(center_x - radius_x - 1)
    max_x = int(center_x + radius_x + 1)
    min_y = int(center_y - radius_y - 1)
    max_y = int(center_y + radius_y + 1)
    carved = []
    for tile_x in range(min_x, max_x + 1):
        for tile_y in range(min_y, max_y + 1):
            norm_x = (tile_x - center_x) / max(radius_x, 0.1)
            norm_y = (tile_y - center_y) / max(radius_y, 0.1)
            if norm_x * norm_x + norm_y * norm_y <= 1.0:
                if (tile_x, tile_y) in tile_map:
                    tile_map.pop((tile_x, tile_y), None)
                    carved.append((tile_x, tile_y))
    return carved


def flood_fill_water(chunk_tiles, water_chunk, start_tile_x, start_tile_y, chunk_idx):
    """Flood fill water from a starting point."""
    from collections import deque
    queue = deque([(start_tile_x, start_tile_y)])
    visited = set()
    max_iterations = 10000  # Prevent infinite loop
    iterations = 0
    while queue and iterations < max_iterations:
        x, y = queue.popleft()
        iterations += 1
        if (x, y) in visited or (x, y) in chunk_tiles:
            continue
        visited.add((x, y))
        water_chunk.add((x, y))
        # Check neighbors within chunk
        start_tile_x_chunk = chunk_idx * CHUNK_TILES
        end_tile_x_chunk = start_tile_x_chunk + CHUNK_TILES
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if start_tile_x_chunk <= nx < end_tile_x_chunk:
                if (nx, ny) not in visited and (nx, ny) not in chunk_tiles:
                    queue.append((nx, ny))


def generate_terrain_chunk(chunk_idx):
    global placed_blocks
    if chunk_idx in terrain_chunks:
        return

    rng = random.Random((chunk_idx * 92821) ^ (_CHUNK_SEED >> 4))
    chunk_tiles = {}
    start_tile_x = chunk_idx * CHUNK_TILES

    biome_index = abs(chunk_idx) % len(BIOMES)
    biome_type = BIOME_TYPES[biome_index]

    for tile_x in range(start_tile_x, start_tile_x + CHUNK_TILES):
        surface_tile_y = get_surface_tile_y(tile_x)
        for tile_y in range(surface_tile_y, surface_tile_y + TERRAIN_DEPTH_ROWS):
            if tile_y == surface_tile_y:
                if biome_type == "desert" or biome_type == "ocean":
                    chunk_tiles[(tile_x, tile_y)] = "sand"
                else:
                    chunk_tiles[(tile_x, tile_y)] = "grass"
            elif tile_y <= surface_tile_y + 3:
                chunk_tiles[(tile_x, tile_y)] = "jord"
            else:
                depth = tile_y - surface_tile_y
                if depth >= 4 and rng.random() < 0.08:
                    chunk_tiles[(tile_x, tile_y)] = "limestone"
                elif depth >= 6 and rng.random() < 0.012:
                    chunk_tiles[(tile_x, tile_y)] = "copper_ore"
                elif depth >= 8 and rng.random() < 0.009:
                    chunk_tiles[(tile_x, tile_y)] = "iron_ore"
                elif depth >= 11 and rng.random() < 0.004:
                    chunk_tiles[(tile_x, tile_y)] = "gold_ore"
                elif depth >= 14 and rng.random() < 0.002:
                    chunk_tiles[(tile_x, tile_y)] = "ruby"
                else:
                    chunk_tiles[(tile_x, tile_y)] = "stone"

    # Beach transitions: convert shoreline grass and dirt to sand near water.
    # Removed water logic

    # Carve caves
    carved_positions = set()
    # Some chunks get a cave entrance cut into a hillside from the side.
    if rng.random() < 0.65:
        side_from_left = rng.choice([True, False])
        if side_from_left:
            entrance_x = rng.randint(start_tile_x + 2, start_tile_x + 5)
            tunnel_dir = 1
        else:
            entrance_x = rng.randint(start_tile_x + CHUNK_TILES - 6, start_tile_x + CHUNK_TILES - 3)
            tunnel_dir = -1

        entrance_surface_y = get_surface_tile_y(entrance_x)
        entry_y = entrance_surface_y + rng.randint(1, 2)
        tunnel_len = rng.randint(9, 14)
        carved_positions.update(carve_ellipse(chunk_tiles, entrance_x + 0.5, entry_y + 0.2, 1.8, 1.4))
        for step in range(tunnel_len):
            offset_x = entrance_x + 0.5 + tunnel_dir * step * 0.95
            offset_y = entry_y + min(2.8, step * 0.18)
            carved_positions.update(carve_ellipse(chunk_tiles, offset_x, offset_y, 1.5, 1.15))
            if step > 2 and rng.random() < 0.25:
                carved_positions.update(carve_ellipse(chunk_tiles, offset_x, offset_y + 0.9, 1.2, 1.0))

    chamber_count = rng.randint(2, 4)
    for _ in range(chamber_count):
        center_x = rng.uniform(start_tile_x + 2, start_tile_x + CHUNK_TILES - 2)
        local_surface = get_surface_tile_y(int(center_x))
        center_y = rng.uniform(local_surface + 6, local_surface + TERRAIN_DEPTH_ROWS - 4)
        radius_x = rng.uniform(2.0, 4.2)
        radius_y = rng.uniform(1.8, 3.4)
        carved_positions.update(carve_ellipse(chunk_tiles, center_x, center_y, radius_x, radius_y))

    for pos in list(chunk_tiles.keys()):
        if pos in removed_terrain_tiles:
            chunk_tiles.pop(pos, None)

    terrain_chunks[chunk_idx] = chunk_tiles
    
    # Generate water blocks for ocean biomes with Minecraft-like spreading
    if biome_type == "ocean":
        for tile_x in range(start_tile_x, start_tile_x + CHUNK_TILES):
            surface_tile_y = get_surface_tile_y(tile_x)
            # Place initial water block AT the surface level (one row above terrain)
            water_start_y = surface_tile_y - 1
            if water_start_y >= 0:
                world_x = tile_x * TILE_SIZE
                world_y = water_start_y * TILE_SIZE
                block_exists = any(b["x"] == world_x and b["y"] == world_y and b["type"] == "water" for b in placed_blocks)
                if not block_exists:
                    placed_blocks.append({"x": world_x, "y": world_y, "type": "water"})
        
        # Water spread logic - make water flow down and to sides like Minecraft
        new_water_blocks = []
        for block in placed_blocks:
            if block["type"] != "water":
                continue
            block_x = int(block["x"] // TILE_SIZE)
            block_y = int(block["y"] // TILE_SIZE)
            
            # Spread downward (gravity)
            below_y = block_y + 1
            below_world_x = block_x * TILE_SIZE
            below_world_y = below_y * TILE_SIZE
            below_exists = any(b["x"] == below_world_x and b["y"] == below_world_y and b["type"] == "water" for b in placed_blocks)
            if not below_exists and below_y < surface_tile_y + 5:
                new_water_blocks.append({"x": below_world_x, "y": below_world_y, "type": "water"})
            
            # Spread horizontally (up to 3 blocks away)
            for dx in [-1, 1]:
                spread_x = block_x + dx
                side_world_x = spread_x * TILE_SIZE
                side_world_y = block_y * TILE_SIZE
                side_exists = any(b["x"] == side_world_x and b["y"] == side_world_y and b["type"] == "water" for b in placed_blocks)
                if not side_exists and abs(spread_x - chunk_idx * CHUNK_TILES) < 5:  # Limit spread within chunk area
                    new_water_blocks.append({"x": side_world_x, "y": side_world_y, "type": "water"})
        
        # Add new water blocks
        for new_block in new_water_blocks:
            block_exists = any(b["x"] == new_block["x"] and b["y"] == new_block["y"] and b["type"] == "water" for b in placed_blocks)
            if not block_exists:
                placed_blocks.append(new_block)


def generate_chunk(chunk_idx):
    """Procedurally add trees for a chunk if not already generated."""
    generate_terrain_chunk(chunk_idx)
    if chunk_idx in generated_chunks:
        return
    generated_chunks.add(chunk_idx)
    biome_trees = BIOMES[abs(chunk_idx) % len(BIOMES)]
    num_trees = len(biome_trees)
    section_w = CHUNK_WIDTH // max(num_trees, 1)
    rng = random.Random(chunk_idx ^ _CHUNK_SEED)
    for i, (leaves, wood) in enumerate(biome_trees):
        x_offset = rng.randint(30, max(31, section_w - 30))
        x = chunk_idx * CHUNK_WIDTH + i * section_w + x_offset
        trunk_tile_x = int((x + 16) // TILE_SIZE)
        surface_tile_y = get_surface_tile_y(trunk_tile_x)
        if get_terrain_tile(trunk_tile_x, surface_tile_y) != "grass":
            continue
        
        # Skip if there's water at this location
        surface_world_x = trunk_tile_x * TILE_SIZE
        surface_world_y = surface_tile_y * TILE_SIZE
        has_water = any(b["type"] == "water" and abs(b["x"] - surface_world_x) < TILE_SIZE and abs(b["y"] - surface_world_y) < TILE_SIZE for b in placed_blocks)
        if has_water:
            continue
        
        left_surface = get_surface_tile_y(trunk_tile_x - 1)
        right_surface = get_surface_tile_y(trunk_tile_x + 1)
        if abs(left_surface - right_surface) > 2:
            continue
        # Align tree so all blocks (leaves at 0,32 and wood at 16) land on tile boundaries
        # Wood at offset 16 should land on multiples of TILE_SIZE
        aligned_x = trunk_tile_x * TILE_SIZE - TILE_SIZE // 2
        trees.append(Tree(aligned_x, surface_tile_y * TILE_SIZE - 160, leaves, wood))


def generate_crabs_for_chunk(chunk_idx):
    if chunk_idx in generated_crab_chunks:
        return
    generated_crab_chunks.add(chunk_idx)

    rng = random.Random((chunk_idx * 18617) ^ (_CHUNK_SEED << 1))
    crab_count = rng.randint(0, 2)
    for _ in range(crab_count):
        world_x = chunk_idx * CHUNK_WIDTH + rng.randint(40, CHUNK_WIDTH - 40)
        tile_x = int(world_x // TILE_SIZE)
        surface_tile_y = get_surface_tile_y(tile_x)
        if get_terrain_tile(tile_x, surface_tile_y) != "grass":
            continue
        if abs(get_surface_tile_y(tile_x - 1) - get_surface_tile_y(tile_x + 1)) > 2:
            continue
        crabs.append(Crab(world_x))


# Fix 3: Add chunk unloading for performance
MAX_LOADED_CHUNKS = 15  # Keep this many chunks loaded around player
UNLOAD_DISTANCE_CHUNKS = 8  # Unload chunks beyond this distance

def unload_distant_chunks(player_chunk_idx):
    """Unload chunks that are too far from the player."""
    chunks_to_unload = []
    for chunk_idx in list(terrain_chunks.keys()):
        if abs(chunk_idx - player_chunk_idx) > UNLOAD_DISTANCE_CHUNKS:
            chunks_to_unload.append(chunk_idx)
    
    for chunk_idx in chunks_to_unload:
        if chunk_idx in terrain_chunks:
            del terrain_chunks[chunk_idx]
        if chunk_idx in water_chunks:
            del water_chunks[chunk_idx]
        # Note: Don't unload generated_chunks flag to prevent regeneration


# Fix 4: Add entity update throttling
def update_crabs_efficiently(current_time, player_world_x):
    """Update crabs with distance-based throttling."""
    global last_crab_cleanup_time
    
    for crab in crabs[:]:
        distance_to_player = abs(crab.x - player_world_x)
        
        if distance_to_player <= CRAB_ACTIVE_UPDATE_RANGE:
            crab.update(current_time)
        elif distance_to_player > CRAB_CULL_RANGE * 1.5:
            # Despawn very distant crabs
            crabs.remove(crab)
            continue
        
        # Periodic cleanup
        if current_time - last_crab_cleanup_time > 5000:
            if distance_to_player > CRAB_CULL_RANGE:
                crabs.remove(crab)
    
    if current_time - last_crab_cleanup_time > 5000:
        last_crab_cleanup_time = current_time


# Fix 5: Add underwater entity cleanup
def cleanup_underwater_entities():
    """Remove trees and crabs that are underwater."""
    global trees, crabs
    
    # Cleanup underwater trees
    trees_to_remove = []
    for tree in trees_to_remove:
        trees.remove(tree)
        print(f"Removed underwater tree at x={tree.x}")
    
    # Cleanup underwater crabs
    crabs_to_remove = []
    for crab in crabs_to_remove:
        crabs.remove(crab)
        print(f"Removed underwater crab at x={crab.x}")


trees = []
pending_trees = []  # [{x, y, leaves_type, wood_type, regrow_at}]
generated_chunks = set()
terrain_chunks = {}
water_chunks = {}
removed_terrain_tiles = set()
terrain_damage_states = {}
crabs = []
generated_crab_chunks = set()


def ensure_save_dir():
    os.makedirs(SAVE_DIR, exist_ok=True)


def save_path_for_slot(slot):
    return os.path.join(SAVE_DIR, f"slot_{slot}.json.gz")


def legacy_save_path_for_slot(slot):
    return os.path.join(SAVE_DIR, f"slot_{slot}.json")


def get_existing_save_path(slot):
    compressed = save_path_for_slot(slot)
    if os.path.exists(compressed):
        return compressed

    legacy = legacy_save_path_for_slot(slot)
    if os.path.exists(legacy):
        return legacy

    return None


def read_save_data(path):
    if path.endswith(".gz"):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return json.load(f)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_save_data(path, data):
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))


def tree_to_dict(tree):
    return {
        "x": int(tree.x),
        "y": int(tree.y),
        "leaves_type": tree.leaves_type,
        "wood_type": tree.wood_type,
        "health": float(tree.health),
        "max_health": float(tree.max_health),
        "broken_blocks": sorted(list(tree.broken_blocks)),
        "block_damage": {str(idx): int(hits) for idx, hits in tree.block_damage.items()},
    }


def tree_from_dict(data):
    tree = Tree(
        int(data.get("x", 0)),
        int(data.get("y", ground_top - 160)),
        data.get("leaves_type", "leaves1"),
        data.get("wood_type", "wood"),
    )
    tree.sync_to_surface()
    broken = data.get("broken_blocks", [])
    if isinstance(broken, list):
        tree.broken_blocks = {
            int(idx)
            for idx in broken
            if isinstance(idx, (int, float)) and 0 <= int(idx) < len(Tree.BLOCK_LAYOUT)
        }
    saved_damage = data.get("block_damage", {})
    if isinstance(saved_damage, dict):
        tree.block_damage = {
            int(idx): int(hits)
            for idx, hits in saved_damage.items()
            if str(idx).isdigit() and isinstance(hits, (int, float)) and 0 < int(hits) < TREE_BLOCK_HITS
        }
    tree.max_health = float(len(Tree.BLOCK_LAYOUT))
    tree.health = float(tree.max_health - len(tree.broken_blocks))
    return tree


def save_game(slot):
    ensure_save_dir()
    now = pygame.time.get_ticks()
    data = {
        "saved_at": now,
        "player_world_x": float(player_world_x),
        "player_y": float(player_rect.y),
        "player_vel_y": float(player_vel_y),
        "player_direction": player_direction,
        "player_health": int(player_health),
        "hotbar_selected": int(hotbar_selected),
        "inventory": dict(inventory),
        "dropped_items": list(dropped_items),
        "placed_blocks": list(placed_blocks),
        "removed_terrain_tiles": [list(pos) for pos in removed_terrain_tiles],
        "trees": [tree_to_dict(t) for t in trees],
        "placed_forges": [forge_to_dict(f) for f in placed_forges],
        "generated_chunks": list(generated_chunks),
        "pending_trees": [
            {
                "x": t["x"], "y": t["y"],
                "leaves_type": t["leaves_type"],
                "wood_type": t["wood_type"],
                "regrow_in_ms": max(0, t["regrow_at"] - now),
            }
            for t in pending_trees
        ],
    }

    save_path = save_path_for_slot(slot)
    write_save_data(save_path, data)

    # If a legacy uncompressed save exists for this slot, remove it after successful compressed save.
    legacy_path = legacy_save_path_for_slot(slot)
    if os.path.exists(legacy_path):
        try:
            os.remove(legacy_path)
        except OSError:
            pass


def load_game(slot):
    global player_world_x, player_vel_y, player_direction, hotbar_selected, trees, placed_blocks, pending_trees, player_health, removed_terrain_tiles, dropped_items, placed_forges
    path = get_existing_save_path(slot)
    if path is None:
        return False

    try:
        data = read_save_data(path)
    except (OSError, gzip.BadGzipFile, json.JSONDecodeError, TypeError, ValueError):
        return False

    player_world_x = float(data.get("player_world_x", WIDTH // 2))
    player_rect.y = int(data.get("player_y", get_surface_world_y(player_world_x) - player_rect.height))
    player_vel_y = float(data.get("player_vel_y", 0))
    player_direction = data.get("player_direction", "right")
    player_health = max(1, min(int(data.get("player_health", PLAYER_MAX_HEALTH)), PLAYER_MAX_HEALTH))
    hotbar_selected = max(0, min(int(data.get("hotbar_selected", 0)), hotbar_slots - 1))

    saved_inventory = data.get("inventory", {})
    for item_type in inventory.keys():
        inventory[item_type] = int(saved_inventory.get(item_type, 0))

    placed_blocks = []
    for block in data.get("placed_blocks", []):
        if isinstance(block, dict) and "x" in block and "y" in block and "type" in block:
            placed_blocks.append(
                {
                    "x": int(block["x"]),
                    "y": int(block["y"]),
                    "type": str(block["type"]),
                }
            )

    placed_forges = []
    for forge_data in data.get("placed_forges", []):
        if isinstance(forge_data, dict) and "x" in forge_data and "y" in forge_data:
            placed_forges.append(forge_from_dict(forge_data))

    dropped_items = []
    for drop in data.get("dropped_items", []):
        if isinstance(drop, dict) and {"x", "y", "type", "count"}.issubset(drop.keys()):
            dropped_items.append(
                {
                    "x": float(drop["x"]),
                    "y": float(drop["y"]),
                    "type": str(drop["type"]),
                    "count": int(drop["count"]),
                }
            )

    removed_terrain_tiles = {
        (int(pos[0]), int(pos[1]))
        for pos in data.get("removed_terrain_tiles", [])
        if isinstance(pos, (list, tuple)) and len(pos) == 2
    }
    terrain_damage_states.clear()

    trees = [tree_from_dict(t) for t in data.get("trees", [])]
    # Restore which chunks were already generated so we don't double-spawn trees.
    generated_chunks.clear()
    generated_crab_chunks.clear()
    terrain_chunks.clear()
    water_chunks.clear()
    crabs.clear()
    saved_chunks = data.get("generated_chunks", [])
    if saved_chunks:
        generated_chunks.update(saved_chunks)
        for chunk_idx in saved_chunks:
            generate_terrain_chunk(chunk_idx)
            generate_crabs_for_chunk(chunk_idx)
    else:
        # Legacy save: infer from tree x positions
        for _t in trees:
            generated_chunks.add(int(_t.x // CHUNK_WIDTH))
        for chunk_idx in generated_chunks:
            generate_terrain_chunk(chunk_idx)
            generate_crabs_for_chunk(chunk_idx)
        if not generated_chunks:
            for _ci in range(-1, 5):
                generate_chunk(_ci)
                generate_crabs_for_chunk(_ci)

    now = pygame.time.get_ticks()
    pending_trees = []
    for t in data.get("pending_trees", []):
        pending_trees.append({
            "x": int(t["x"]), "y": int(t["y"]),
            "leaves_type": t.get("leaves_type", "leaves1"),
            "wood_type": t.get("wood_type", "wood"),
            "regrow_at": now + int(t.get("regrow_in_ms", TREE_REGROW_TIME)),
        })

    # Run cleanup for old saves
    cleanup_underwater_entities()

    return True


# Fix 6: Add error handling for file operations
def safe_load_game(slot):
    """Safely load game with error handling."""
    try:
        return load_game(slot)
    except (OSError, gzip.BadGzipFile, json.JSONDecodeError) as e:
        print(f"Error loading save slot {slot}: {e}")
        return False

def safe_save_game(slot):
    """Safely save game with error handling."""
    try:
        save_game(slot)
        return True
    except (OSError, json.JSONEncodeError) as e:
        print(f"Error saving to slot {slot}: {e}")
        return False


def get_slot_label(slot):
    path = get_existing_save_path(slot)
    if path is None:
        return "Empty"

    try:
        data = read_save_data(path)
        trees_left = len(data.get("trees", []))
        px = int(data.get("player_world_x", 0))
        return f"Saved - X:{px} Trees:{trees_left}"
    except (OSError, gzip.BadGzipFile, json.JSONDecodeError, TypeError, ValueError):
        return "Corrupted save"


def respawn_player():
    global player_world_x, player_vel_y, player_health, player_fall_start_bottom
    player_world_x = WIDTH // 2
    player_rect.bottom = get_surface_world_y(player_world_x)
    player_vel_y = 0
    player_health = PLAYER_MAX_HEALTH
    player_fall_start_bottom = None
    terrain_damage_states.clear()


def drop_inventory_on_death(world_x, world_y):
    drop_y = world_y
    for item_type, count in list(inventory.items()):
        if count <= 0:
            continue
        dropped_items.append(
            {
                "x": float(world_x + random.randint(-50, 50)),
                "y": float(drop_y),
                "type": item_type,
                "count": int(count),
            }
        )
        inventory[item_type] = 0


def update_dropped_items_and_pickup(current_time):
    player_rect_world = get_player_world_rect()
    for drop in dropped_items[:]:
        # Let dropped items settle onto the local surface.
        target_y = get_surface_world_y(drop["x"]) - 18
        if drop["y"] < target_y:
            drop["y"] = min(target_y, drop["y"] + 2.4)

        item_rect = pygame.Rect(int(drop["x"] - 10), int(drop["y"] - 10), 20, 20)
        if player_rect_world.colliderect(item_rect):
            inventory[drop["type"]] = inventory.get(drop["type"], 0) + int(drop["count"])
            dropped_items.remove(drop)


def draw_dropped_items(surface, camera_x, camera_y, current_time):
    for drop in dropped_items:
        draw_x = int(drop["x"] - camera_x)
        bob_y = int(math.sin((current_time + int(drop["x"])) * 0.008) * 2)
        draw_y = int(drop["y"] - camera_y + bob_y)
        if draw_x < -20 or draw_x > WIDTH + 20 or draw_y < -20 or draw_y > HEIGHT + 20:
            continue
        icon = get_item_surface(drop["type"], 18)
        surface.blit(icon, (draw_x - 9, draw_y - 9))

        count_text = pygame.font.Font(None, 14).render(str(drop["count"]), True, (255, 255, 255))
        surface.blit(count_text, (draw_x + 4, draw_y + 2))


def apply_damage(amount):
    global player_health, player_last_damage_time, player_death_message_until
    global player_damage_flash_until, player_damage_shake_until
    if amount <= 0:
        return

    now = pygame.time.get_ticks()
    if now - player_last_damage_time < PLAYER_DAMAGE_COOLDOWN:
        return

    player_last_damage_time = now
    player_damage_flash_until = now + PLAYER_DAMAGE_FLASH_MS
    player_damage_shake_until = now + PLAYER_DAMAGE_SHAKE_MS
    player_health = max(0, player_health - int(amount))
    if player_health <= 0:
        drop_inventory_on_death(player_world_x, player_rect.y)
        player_death_message_until = now + 2200
        respawn_player()


def get_player_world_rect():
    return pygame.Rect(int(player_world_x - player_rect.width // 2), int(player_rect.y), player_rect.width, player_rect.height)


def get_block_dimensions(block_type):
    if block_type == "crafting_table" or block_type == "forge":
        return TILE_SIZE * 3, TILE_SIZE * 2
    return TILE_SIZE, TILE_SIZE


def get_block_world_rect(block):
    width, height = get_block_dimensions(block["type"])
    return pygame.Rect(int(block["x"]), int(block["y"]), width, height)


def get_terrain_tile(tile_x, tile_y):
    surface_tile_y = get_surface_tile_y(tile_x)
    if tile_y < surface_tile_y:
        return None
    if (tile_x, tile_y) in removed_terrain_tiles:
        return None

    # Check for bedrock
    if tile_y >= surface_tile_y + TERRAIN_DEPTH_ROWS + 5:
        return "bedrock"  # Unbreakable block

    chunk_idx = int((tile_x * TILE_SIZE) // CHUNK_WIDTH)
    generate_terrain_chunk(chunk_idx)

    if tile_y >= surface_tile_y + TERRAIN_DEPTH_ROWS:
        return "stone"

    return terrain_chunks.get(chunk_idx, {}).get((tile_x, tile_y))


def get_terrain_break_hits(tile_key):
    stone_like = {"stone", "sand", "limestone", "copper_ore", "iron_ore", "gold_ore", "ruby"}
    if tile_key not in stone_like:
        return 1

    selected_item = hotbar_items[hotbar_selected]
    has_pickaxe = selected_item and selected_item.get("type") == "pickaxe" and inventory.get("pickaxe", 0) > 0
    return STONE_HITS_PICKAXE if has_pickaxe else STONE_HITS_HAND


def apply_fall_damage(fall_distance):
    fallen_blocks = int(fall_distance // TILE_SIZE)
    if fallen_blocks < FALL_DAMAGE_START_BLOCKS:
        return
    damage = fallen_blocks - (FALL_DAMAGE_START_BLOCKS - 1)
    apply_damage(max(1, damage))



def draw_sky(surface, camera_x, camera_y):
    if sky_images["sky"]:
        sky_img = pygame.transform.scale(sky_images["sky"], (TILE_SIZE, TILE_SIZE))
        start_x = int(-(camera_x % TILE_SIZE) - TILE_SIZE)
        start_y = int(-(camera_y % TILE_SIZE) - TILE_SIZE)
        for y in range(start_y, HEIGHT + TILE_SIZE, TILE_SIZE):
            for x in range(start_x, WIDTH + TILE_SIZE, TILE_SIZE):
                surface.blit(sky_img, (x, y))


def draw_grid(surface, camera_x, camera_y, cell_size=32, color=(50, 50, 50)):
    start_x = int(-(camera_x % cell_size))
    start_y = int(-(camera_y % cell_size))
    for x in range(start_x, WIDTH + cell_size, cell_size):
        pygame.draw.line(surface, color, (x, 0), (x, HEIGHT))
    for y in range(start_y, HEIGHT + cell_size, cell_size):
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))


def draw_ground(surface, camera_x, camera_y):
    start_tile_x = int(camera_x // TILE_SIZE) - 1
    end_tile_x = int((camera_x + WIDTH) // TILE_SIZE) + 1
    start_tile_y = int(camera_y // TILE_SIZE) - 1
    end_tile_y = int((camera_y + HEIGHT) // TILE_SIZE) + 1

    for tile_x in range(start_tile_x, end_tile_x + 1):
        for tile_y in range(start_tile_y, end_tile_y + 1):
            tile_key = get_terrain_tile(tile_x, tile_y)
            if not tile_key:
                continue
            draw_x = tile_x * TILE_SIZE - camera_x
            draw_y = tile_y * TILE_SIZE - camera_y
            surface.blit(tile_images[tile_key], (draw_x, draw_y))


def draw_mountains(surface, camera_x, camera_y):
    return


def draw_placed_blocks(surface, camera_x, camera_y):
    """Draw all placed blocks in the world"""
    # Draw crafting tables first so other placed blocks can appear in front of them.
    for block in placed_blocks:
        if block.get("type") != "crafting_table":
            continue
        block_rect = get_block_world_rect(block)
        draw_x = block_rect.x - camera_x
        draw_y = block_rect.y - camera_y + CRAFTING_TABLE_GROUND_SINK_PX
        if draw_x < -block_rect.width or draw_x > WIDTH or draw_y < -block_rect.height or draw_y > HEIGHT:
            continue
        item_surface = get_item_surface(block["type"], max(block_rect.width, block_rect.height))
        if item_surface.get_width() != block_rect.width or item_surface.get_height() != block_rect.height:
            item_surface = pygame.transform.scale(item_surface, (block_rect.width, block_rect.height))
        surface.blit(item_surface, (draw_x, draw_y))

    for block in placed_blocks:
        if block.get("type") == "crafting_table":
            continue
        block_rect = get_block_world_rect(block)
        draw_x = block_rect.x - camera_x
        draw_y = block_rect.y - camera_y
        if draw_x < -block_rect.width or draw_x > WIDTH or draw_y < -block_rect.height or draw_y > HEIGHT:
            continue
        if block["type"] == "water":
            # Check if there's water above
            has_water_above = any(b["type"] == "water" and b["x"] == block["x"] and b["y"] == block["y"] - TILE_SIZE for b in placed_blocks)
            water_type = "water_top" if not has_water_above else "water_bottom"
            item_surface = get_item_surface(water_type, max(block_rect.width, block_rect.height))
        else:
            item_surface = get_item_surface(block["type"], max(block_rect.width, block_rect.height))
        if item_surface.get_width() != block_rect.width or item_surface.get_height() != block_rect.height:
            item_surface = pygame.transform.scale(item_surface, (block_rect.width, block_rect.height))
        surface.blit(item_surface, (draw_x, draw_y))
    
    # Draw forges with proper rendering
    for forge in placed_forges:
        draw_x = forge.rect.x - camera_x
        draw_y = forge.rect.y - camera_y + CRAFTING_TABLE_GROUND_SINK_PX
        if draw_x < -forge.rect.width or draw_x > WIDTH or draw_y < -forge.rect.height or draw_y > HEIGHT:
            continue
        
        # Use animated forge image if burning
        if forge.is_smelting and forge.fuel_remaining_ms > 0:
            # Choose animation frame based on time
            frame_key = "fire_bobing" if (pygame.time.get_ticks() // 300) % 2 else "fire"
            forge_img = forge_images.get(frame_key)
        else:
            frame_key = "idle_bobing" if (pygame.time.get_ticks() // 500) % 2 else "idle"
            forge_img = forge_images.get(frame_key)
        
        if forge_img:
            scaled_img = pygame.transform.scale(forge_img, (forge.rect.width, forge.rect.height))
            surface.blit(scaled_img, (draw_x, draw_y))
        else:
            item_surface = get_item_surface("forge", max(forge.rect.width, forge.rect.height))
            scaled_img = pygame.transform.scale(item_surface, (forge.rect.width, forge.rect.height))
            surface.blit(scaled_img, (draw_x, draw_y))


def draw_item_in_hand(surface, player_x, player_y, direction):
    """Draw selected hotbar item in the player's hand."""
    if hotbar_selected < 0 or hotbar_selected >= len(hotbar_items):
        return  # Invalid hotbar selection
    
    hotbar_slot = hotbar_items[hotbar_selected]
    if not hotbar_slot:
        return

    item_type = hotbar_slot["type"]
    if inventory.get(item_type, 0) <= 0:
        return

    hand_size = 18
    if item_type == "axe":
        axe_key = "axe_left" if direction == "left" else "axe_right"
        axe_img = item_images.get(axe_key)
        if axe_img:
            hand_item = pygame.transform.scale(axe_img, (hand_size, hand_size)).copy()
        else:
            hand_item = get_item_surface(item_type, hand_size).copy()
            if direction == "left":
                hand_item = pygame.transform.flip(hand_item, True, False)
    elif item_type == "knife":
        knife_img = item_images.get("knife")
        if knife_img:
            hand_item = pygame.transform.scale(knife_img, (hand_size, hand_size)).copy()
            if direction == "left":
                hand_item = pygame.transform.flip(hand_item, True, False)
        else:
            hand_item = get_item_surface(item_type, hand_size).copy()
            if direction == "left":
                hand_item = pygame.transform.flip(hand_item, True, False)
    else:
        hand_item = get_item_surface(item_type, hand_size).copy()
        if direction == "left":
            hand_item = pygame.transform.flip(hand_item, True, False)

    hand_x = player_x - 6 if direction == "left" else player_x + 34
    hand_y = player_y + 20
    surface.blit(hand_item, (hand_x, hand_y))


def get_forge_at(world_x, world_y):
    """Get forge at a given world position, if any."""
    for forge in placed_forges:
        if forge.rect.collidepoint(world_x, world_y):
            return forge
    return None


def forge_to_dict(forge):
    return {
        "x": int(forge.x),
        "y": int(forge.y),
        "input_item": dict(forge.input_item) if forge.input_item else None,
        "fuel_item": dict(forge.fuel_item) if forge.fuel_item else None,
        "output_items": dict(forge.output_items),
        "fuel_remaining_ms": int(forge.fuel_remaining_ms),
        "smelt_progress_ms": int(forge.smelt_progress_ms),
        "is_smelting": bool(forge.is_smelting),
    }


def forge_from_dict(data):
    forge = Forge(int(data.get("x", 0)), int(data.get("y", 0)))
    input_item = data.get("input_item")
    if isinstance(input_item, dict) and isinstance(input_item.get("type"), str):
        forge.input_item = {"type": input_item["type"], "count": max(1, int(input_item.get("count", 0)))}
    fuel_item = data.get("fuel_item")
    if isinstance(fuel_item, dict) and isinstance(fuel_item.get("type"), str):
        forge.fuel_item = {"type": fuel_item["type"], "count": max(1, int(fuel_item.get("count", 0)))}
    output_items = data.get("output_items", {})
    if isinstance(output_items, dict):
        forge.output_items = {str(k): int(v) for k, v in output_items.items() if isinstance(k, str) and isinstance(v, (int, float)) and int(v) > 0}
    forge.fuel_remaining_ms = max(0, int(data.get("fuel_remaining_ms", 0)))
    forge.smelt_progress_ms = max(0, int(data.get("smelt_progress_ms", 0)))
    forge.is_smelting = bool(data.get("is_smelting", False))
    return forge


def get_nearby_block_rects(world_x):
    """Return rects of placed blocks near the player (solid blocks, forges, and walkable items)."""
    rects = []
    # Always exclude water and crafting tables from collision
    for block in placed_blocks:
        if block.get("type") == "water" or block.get("type") == "crafting_table":
            continue
        # All other blocks are solid (including arrows)
        block_rect = get_block_world_rect(block)
        dx = block_rect.x - world_x
        if abs(dx) < WIDTH:
            rects.append(pygame.Rect(int(world_x + dx), block_rect.y, block_rect.width, block_rect.height))
    for forge in placed_forges:
        dx = forge.rect.x - world_x
        if abs(dx) < WIDTH:
            rects.append(pygame.Rect(int(world_x + dx), forge.rect.y, forge.rect.width, forge.rect.height))
    return rects


def get_nearby_terrain_rects(world_x, world_y=None, half_w_tiles=24, up_tiles=18, down_tiles=22):
    rects = []
    center_tile_x = int(world_x // TILE_SIZE)
    if world_y is None:
        world_y = player_rect.centery
    center_tile_y = int(world_y // TILE_SIZE)
    for tile_x in range(center_tile_x - half_w_tiles, center_tile_x + half_w_tiles + 1):
        for tile_y in range(center_tile_y - up_tiles, center_tile_y + down_tiles + 1):
            if get_terrain_tile(tile_x, tile_y):
                rects.append(pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    return rects


def get_nearby_solid_rects(world_x, world_y=None, half_w_tiles=24, up_tiles=18, down_tiles=22):
    return get_nearby_terrain_rects(world_x, world_y, half_w_tiles, up_tiles, down_tiles) + get_nearby_block_rects(world_x)


def get_local_solid_rects(center_x, center_y, half_w_tiles=4, up_tiles=2, down_tiles=5):
    rects = []
    center_tile_x = int(center_x // TILE_SIZE)
    center_tile_y = int(center_y // TILE_SIZE)

    for tile_x in range(center_tile_x - half_w_tiles, center_tile_x + half_w_tiles + 1):
        for tile_y in range(center_tile_y - up_tiles, center_tile_y + down_tiles + 1):
            if get_terrain_tile(tile_x, tile_y):
                rects.append(pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    for block in placed_blocks:
        if block.get("type") == "crafting_table":
            continue
        block_rect = get_block_world_rect(block)
        if abs(block_rect.centerx - center_x) < half_w_tiles * TILE_SIZE * 2 and abs(block_rect.centery - center_y) < down_tiles * TILE_SIZE * 2:
            rects.append(block_rect)

    return rects


def get_crab_ground_y(world_x, crab_width, crab_height, current_y):
    crab_rect = pygame.Rect(int(world_x), int(current_y), crab_width, crab_height)
    solid_rects = get_local_solid_rects(crab_rect.centerx, crab_rect.bottom)

    foot_left = crab_rect.left + 4
    foot_right = crab_rect.right - 4
    # Allow stepping up roughly one tile so crabs can climb terrain blocks.
    min_support_y = crab_rect.bottom - TILE_SIZE - 4
    max_support_y = crab_rect.bottom + 10

    support_top = None
    for rect in solid_rects:
        if rect.right <= foot_left or rect.left >= foot_right:
            continue
        if rect.top < min_support_y or rect.top > max_support_y:
            continue
        if support_top is None or rect.top < support_top:
            support_top = rect.top

    if support_top is None:
        return None

    candidate = pygame.Rect(int(world_x), int(support_top - crab_height), crab_width, crab_height)
    for rect in solid_rects:
        if candidate.colliderect(rect):
            return None
    return float(candidate.y)


def crab_position_valid(world_x, world_y, crab_width, crab_height):
    rect = pygame.Rect(int(world_x), int(world_y), crab_width, crab_height)
    solid_rects = get_local_solid_rects(rect.centerx, rect.bottom)

    # Crab body cannot overlap solids.
    for tile_rect in solid_rects:
        if rect.colliderect(tile_rect):
            return False

    # Crab must have support under both feet area.
    feet = pygame.Rect(rect.left + 4, rect.bottom, rect.width - 8, 2)
    return any(feet.colliderect(tile_rect) for tile_rect in solid_rects)


def get_nearby_occupied_rects(world_x, world_y=None, half_w_tiles=24, up_tiles=18, down_tiles=22):
    occupied = get_nearby_terrain_rects(world_x, world_y, half_w_tiles, up_tiles, down_tiles)
    for block in placed_blocks:
        block_rect = get_block_world_rect(block)
        if abs(block_rect.x - world_x) < (half_w_tiles * TILE_SIZE * 2):
            occupied.append(block_rect)
    for forge in placed_forges:
        if abs(forge.rect.x - world_x) < (half_w_tiles * TILE_SIZE * 2):
            occupied.append(forge.rect)
    return occupied


# Seed a few chunks around spawn so trees and terrain are visible immediately.
for _ci in range(-1, 5):
    generate_chunk(_ci)
    generate_crabs_for_chunk(_ci)

player_rect.bottom = get_surface_world_y(player_world_x)


def break_terrain_at(world_x, world_y):
    tile_x = int(world_x // TILE_SIZE)
    tile_y = int(world_y // TILE_SIZE)
    tile_key = get_terrain_tile(tile_x, tile_y)
    if not tile_key or tile_key == "bedrock":  # Prevent breaking bedrock
        return False
    
    # Prevent breaking water blocks
    for block in placed_blocks:
        if block["type"] == "water":
            block_rect = get_block_world_rect(block)
            if abs(block_rect.centerx - world_x) < TILE_SIZE and abs(block_rect.centery - world_y) < TILE_SIZE:
                return False

    selected_item = hotbar_items[hotbar_selected]
    tool_used = None
    if selected_item and selected_item.get("type") in TOOL_DURABILITY:
        tool_type = selected_item["type"]
        if inventory.get(tool_type, 0) > 0:
            tool_used = tool_type

    tile_pos = (tile_x, tile_y)
    current_hits = terrain_damage_states.get(tile_pos, 0) + 1
    needed_hits = get_terrain_break_hits(tile_key)
    if current_hits < needed_hits:
        terrain_damage_states[tile_pos] = current_hits
        return True

    terrain_damage_states.pop(tile_pos, None)
    
    removed_terrain_tiles.add(tile_pos)
    if tile_y < SURFACE_TILE_Y + TERRAIN_DEPTH_ROWS:
        chunk_idx = int((tile_x * TILE_SIZE) // CHUNK_WIDTH)
        generate_terrain_chunk(chunk_idx)
        terrain_chunks.get(chunk_idx, {}).pop(tile_pos, None)
    inventory[tile_key] = inventory.get(tile_key, 0) + 1
    
    # Use tool durability if a tool was used
    if tool_used:
        use_tool(tool_used)
    
    return True


def get_slot_item_data(slot_item):
    if not slot_item:
        return None, 0
    if isinstance(slot_item, dict):
        item_type = slot_item.get("type")
        item_count = int(slot_item.get("count", 0))
    else:
        item_type = slot_item
        item_count = 1
    if not item_type or item_count <= 0:
        return None, 0
    return item_type, item_count


def build_crafting_grid_data():
    active_rows, active_cols = get_active_crafting_size()
    grid_types = [[None for _ in range(CRAFTING_COLS)] for _ in range(CRAFTING_ROWS)]
    grid_counts = [[0 for _ in range(CRAFTING_COLS)] for _ in range(CRAFTING_ROWS)]
    for r in range(active_rows):
        for c in range(active_cols):
            item_type, item_count = get_slot_item_data(crafting_grid[r][c])
            grid_types[r][c] = item_type
            grid_counts[r][c] = item_count
    return grid_types, grid_counts


def match_shapeless_recipe(recipe, grid_types, grid_counts):
    active_rows, active_cols = get_active_crafting_size()
    totals = {}
    slot_positions = {}
    for r in range(active_rows):
        for c in range(active_cols):
            item_type = grid_types[r][c]
            if not item_type:
                continue
            totals[item_type] = totals.get(item_type, 0) + grid_counts[r][c]
            slot_positions.setdefault(item_type, []).append((r, c))

    required = recipe["input"]
    if set(totals.keys()) != set(required.keys()):
        return None

    craft_count = None
    for item_type, req_amount in required.items():
        have = totals.get(item_type, 0)
        if req_amount <= 0 or have < req_amount:
            return None
        possible = have // req_amount
        craft_count = possible if craft_count is None else min(craft_count, possible)

    if not craft_count or craft_count <= 0:
        return None

    consume_plan = []
    for item_type, req_amount in required.items():
        needed = req_amount * craft_count
        for r, c in slot_positions[item_type]:
            if needed <= 0:
                break
            take = min(grid_counts[r][c], needed)
            if take > 0:
                consume_plan.append((r, c, take))
                needed -= take
        if needed > 0:
            return None

    output = {item: count * craft_count for item, count in recipe["output"].items()}
    return recipe["name"], output, consume_plan


def match_shaped_recipe(recipe, grid_types, grid_counts):
    active_rows, active_cols = get_active_crafting_size()
    patterns = [recipe["pattern"]]
    if recipe.get("mirror"):
        mirrored = [row[::-1] for row in recipe["pattern"]]
        if mirrored != recipe["pattern"]:
            patterns.append(mirrored)

    for pattern in patterns:
        pat_rows = len(pattern)
        pat_cols = len(pattern[0]) if pat_rows else 0
        if pat_rows == 0 or pat_cols == 0:
            continue
        if pat_rows > active_rows or pat_cols > active_cols:
            continue

        for off_r in range(active_rows - pat_rows + 1):
            for off_c in range(active_cols - pat_cols + 1):
                used_positions = []
                valid = True

                for r in range(active_rows):
                    for c in range(active_cols):
                        in_pattern = off_r <= r < off_r + pat_rows and off_c <= c < off_c + pat_cols
                        symbol = " "
                        if in_pattern:
                            symbol = pattern[r - off_r][c - off_c]

                        have_type = grid_types[r][c]
                        if symbol == " ":
                            if have_type is not None:
                                valid = False
                                break
                        else:
                            expected_item = recipe["key"].get(symbol)
                            if expected_item is None or have_type != expected_item:
                                valid = False
                                break
                            used_positions.append((r, c))
                    if not valid:
                        break

                if not valid or not used_positions:
                    continue

                craft_count = min(grid_counts[r][c] for r, c in used_positions)
                if craft_count <= 0:
                    continue

                output = {item: count * craft_count for item, count in recipe["output"].items()}
                consume_plan = [(r, c, craft_count) for r, c in used_positions]
                return recipe["name"], output, consume_plan

    return None


def get_crafting_recipe():
    """Return matching recipe name, output items, and per-slot consume plan."""
    grid_types, grid_counts = build_crafting_grid_data()

    for recipe in CRAFTING_RECIPES:
        if recipe["type"] == "shapeless":
            result = match_shapeless_recipe(recipe, grid_types, grid_counts)
        else:
            result = match_shaped_recipe(recipe, grid_types, grid_counts)
        if result:
            return result

    return None, None, None


def draw_menu(surface):
    surface.fill((0, 0, 0))

    accent_red = (165, 20, 20)
    soft_red = (95, 18, 18)
    text_red = (210, 60, 60)
    border_red = (120, 28, 28)
    panel_dark = (14, 14, 14)

    pygame.draw.rect(surface, soft_red, (0, 0, WIDTH, 6))
    pygame.draw.rect(surface, soft_red, (0, HEIGHT - 6, WIDTH, 6))

    # Main name area (image if available, placeholder otherwise)
    name_rect = pygame.Rect(WIDTH // 2 - 210, 35, 420, 100)
    if main_name_image:
        image_rect = main_name_image.get_rect(center=name_rect.center)
        surface.blit(main_name_image, image_rect.topleft)
    else:
        pygame.draw.rect(surface, panel_dark, name_rect)
        pygame.draw.rect(surface, border_red, name_rect, 2)
        placeholder = menu_button_font.render("TITLE", True, text_red)
        surface.blit(placeholder, placeholder.get_rect(center=name_rect.center))

    pygame.draw.line(surface, accent_red, (name_rect.left, name_rect.bottom + 8), (name_rect.right, name_rect.bottom + 8), 2)

    subtitle = menu_small_font.render("Choose a save slot, then save or load", True, (185, 70, 70))
    surface.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 150))

    # Buttons
    pygame.draw.rect(surface, panel_dark, menu_new_button_rect)
    pygame.draw.rect(surface, accent_red, menu_new_button_rect, 2)
    new_text = menu_button_font.render("Play", True, (255, 255, 255))
    surface.blit(new_text, new_text.get_rect(center=menu_new_button_rect.center))

    pygame.draw.rect(surface, panel_dark, menu_save_button_rect)
    pygame.draw.rect(surface, accent_red, menu_save_button_rect, 2)
    save_text = menu_button_font.render("Save", True, (255, 255, 255))
    surface.blit(save_text, save_text.get_rect(center=menu_save_button_rect.center))

    # Save slots
    for i, rect in enumerate(menu_slot_rects, start=1):
        selected = i == menu_selected_slot
        bg = (28, 8, 8) if selected else panel_dark
        border = (220, 65, 65) if selected else border_red
        pygame.draw.rect(surface, bg, rect)
        pygame.draw.rect(surface, border, rect, 2)

        slot_title = menu_small_font.render(f"Slot {i}", True, (240, 240, 240))
        slot_info = pygame.font.Font(None, 20).render(get_slot_label(i), True, (185, 185, 185))
        surface.blit(slot_title, (rect.x + 10, rect.y + 8))
        surface.blit(slot_info, (rect.x + 10, rect.y + 30))

    hint = pygame.font.Font(None, 20).render("ESC in-game returns to menu", True, (160, 160, 160))
    surface.blit(hint, (60, 430))

    if menu_status_text and pygame.time.get_ticks() < menu_status_until:
        status = pygame.font.Font(None, 24).render(menu_status_text, True, text_red)
        surface.blit(status, (60, 405))


def get_inventory_items_list():
    all_items = []
    for item_type in inventory.keys():
        if inventory[item_type] > 0:
            all_items.append({"type": item_type, "count": inventory[item_type]})
    return all_items


def get_active_crafting_size():
    if using_crafting_table:
        return CRAFTING_LARGE_ROWS, CRAFTING_LARGE_COLS
    return CRAFTING_SMALL_ROWS, CRAFTING_SMALL_COLS


def set_crafting_mode(use_table):
    """Switch crafting size. When shrinking to 2x2, return out-of-range items to inventory."""
    global using_crafting_table
    using_crafting_table = use_table

    active_rows, active_cols = get_active_crafting_size()
    for row in range(CRAFTING_ROWS):
        for col in range(CRAFTING_COLS):
            if row < active_rows and col < active_cols:
                continue
            item = crafting_grid[row][col]
            if not item:
                continue
            item_type, item_count = get_slot_item_data(item)
            if item_type and item_count > 0:
                inventory[item_type] = inventory.get(item_type, 0) + item_count
            crafting_grid[row][col] = None


def start_from_menu():
    """Start game by loading selected slot if present, otherwise continue as new world."""
    global current_state, menu_status_text, menu_status_until
    set_crafting_mode(False)
    if load_game(menu_selected_slot):
        menu_status_text = f"Loaded slot {menu_selected_slot}"
        menu_status_until = pygame.time.get_ticks() + 1200
    current_state = GAME_STATE_PLAYING


def draw_inventory(surface):
    surface.fill((80, 80, 80))
    
    # Title
    title_font = pygame.font.Font(None, 40)
    title = title_font.render("Inventory", True, (255, 255, 255))
    title_rect = title.get_rect(center=(WIDTH // 2, 15))
    surface.blit(title, title_rect)
    
    # Inventory grid
    inv_start_x = 50
    inv_start_y = 80
    inv_font = pygame.font.Font(None, 24)
    
    inv_title = inv_font.render("Inventory", True, (200, 200, 200))
    surface.blit(inv_title, (inv_start_x, inv_start_y - 30))
    
    # Get all items as a list
    all_items = get_inventory_items_list()
    
    # Draw inventory slots
    slot_index = 0
    for row in range(INVENTORY_ROWS):
        for col in range(INVENTORY_COLS):
            slot_x = inv_start_x + col * (INVENTORY_SLOT_SIZE + 5)
            slot_y = inv_start_y + row * (INVENTORY_SLOT_SIZE + 5)
            slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
            
            # Background
            pygame.draw.rect(surface, (60, 60, 60), slot_rect)
            pygame.draw.rect(surface, (100, 100, 100), slot_rect, 2)
            
            # Draw item if exists
            if slot_index < len(all_items):
                item = all_items[slot_index]
                item_surface = get_item_surface(item["type"], INVENTORY_SLOT_SIZE - 6)
                surface.blit(item_surface, (slot_x + 3, slot_y + 3))
                
                # Draw count
                count_font = pygame.font.Font(None, 16)
                count_text = count_font.render(str(item["count"]), True, (255, 255, 255))
                count_rect = count_text.get_rect(bottomright=(slot_rect.right - 4, slot_rect.bottom - 4))
                surface.blit(count_text, count_rect)
            
            slot_index += 1
    
    # Crafting area
    active_rows, active_cols = get_active_crafting_size()
    craft_start_x = inv_start_x + (INVENTORY_COLS + 1) * (INVENTORY_SLOT_SIZE + 5)
    craft_start_y = inv_start_y
    
    craft_mode_name = "3x3 Crafting Table" if using_crafting_table else "2x2 Inventory Crafting"
    craft_title = inv_font.render(craft_mode_name, True, (200, 200, 200))
    surface.blit(craft_title, (craft_start_x, craft_start_y - 30))
    
    # Draw crafting grid
    for row in range(active_rows):
        for col in range(active_cols):
            slot_x = craft_start_x + col * (INVENTORY_SLOT_SIZE + 5)
            slot_y = craft_start_y + row * (INVENTORY_SLOT_SIZE + 5)
            slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
            
            pygame.draw.rect(surface, (60, 60, 60), slot_rect)
            pygame.draw.rect(surface, (100, 100, 100), slot_rect, 2)
            
            # Draw item in crafting slot
            if crafting_grid[row][col]:
                slot_item = crafting_grid[row][col]
                if isinstance(slot_item, dict):
                    item_type = slot_item.get("type")
                    item_count = int(slot_item.get("count", 1))
                else:
                    item_type = slot_item
                    item_count = 1
                item_surface = get_item_surface(item_type, INVENTORY_SLOT_SIZE - 6)
                surface.blit(item_surface, (slot_x + 3, slot_y + 3))
                count_font = pygame.font.Font(None, 16)
                count_text = count_font.render(str(item_count), True, (255, 255, 255))
                count_rect = count_text.get_rect(bottomright=(slot_rect.right - 4, slot_rect.bottom - 4))
                surface.blit(count_text, count_rect)
    
    # Result slot
    result_x = craft_start_x + active_cols * (INVENTORY_SLOT_SIZE + 5) + 15
    result_y = craft_start_y + INVENTORY_SLOT_SIZE // 2
    result_rect = pygame.Rect(result_x, result_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
    pygame.draw.rect(surface, (60, 60, 60), result_rect)
    pygame.draw.rect(surface, (150, 150, 100), result_rect, 2)
    
    # Check for recipe match
    recipe_name, recipe_output, consume_plan = get_crafting_recipe()
    if recipe_output:
        # Show result
        for item_type, count in recipe_output.items():
            item_surface = get_item_surface(item_type, INVENTORY_SLOT_SIZE - 6)
            surface.blit(item_surface, (result_x + 3, result_y + 3))
            
            # Draw count
            count_font = pygame.font.Font(None, 14)
            count_text = count_font.render(f"x{count}", True, (255, 255, 255))
            count_rect = count_text.get_rect(bottomright=(result_rect.right - 3, result_rect.bottom - 3))
            surface.blit(count_text, count_rect)
    
    # Show recipe status
    status_font = pygame.font.Font(None, 20)
    
    if recipe_output:
        status_text = status_font.render(f"Craft: {recipe_name}", True, (100, 255, 100))
    else:
        # Check if there are items in grid but no recipe
        has_items = any(crafting_grid[r][c] for r in range(CRAFTING_ROWS) for c in range(CRAFTING_COLS))
        if has_items:
            status_text = status_font.render("Invalid recipe", True, (255, 100, 100))
        else:
            status_text = status_font.render("Add items to craft", True, (150, 150, 150))
    
    surface.blit(status_text, (craft_start_x, craft_start_y - 50))
    
    # Instructions
    inst_font = pygame.font.Font(None, 16)
    inst_text = inst_font.render("Drag items to crafting area. Click result to craft.", True, (180, 180, 180))
    surface.blit(inst_text, (inv_start_x, craft_start_y + active_rows * (INVENTORY_SLOT_SIZE + 5) + 20))
    
    # Close hint
    close_font = pygame.font.Font(None, 18)
    close_text = close_font.render("Press I to close", True, (150, 150, 150))
    close_rect = close_text.get_rect(center=(WIDTH // 2, HEIGHT - 20))
    surface.blit(close_text, close_rect)
    
    # Draw dragging item
    if drag_item:
        mouse_pos = pygame.mouse.get_pos()
        item_surface = get_item_surface(drag_item["type"], 32)
        surface.blit(item_surface, (mouse_pos[0] - 16, mouse_pos[1] - 16))
        count_font = pygame.font.Font(None, 16)
        count_text = count_font.render(str(drag_item["count"]), True, (255, 255, 255))
        surface.blit(count_text, (mouse_pos[0] + 10, mouse_pos[1] + 8))


def draw_forge(surface, forge):
    """Draw forge smelting UI."""
    surface.fill((80, 80, 80))
    
    # Title
    title_font = pygame.font.Font(None, 40)
    title = title_font.render("Forge", True, (255, 200, 100))
    title_rect = title.get_rect(center=(WIDTH // 2, 15))
    surface.blit(title, title_rect)
    
    # Fire indicator
    fire_font = pygame.font.Font(None, 24)
    fuel_bar_width = 200
    fuel_bar_height = 20
    fuel_x = WIDTH // 2 - fuel_bar_width // 2
    fuel_y = 70
    
    # Fuel bar
    fuel_text = fire_font.render("Fuel:", True, (255, 200, 100))
    surface.blit(fuel_text, (fuel_x - 60, fuel_y))
    pygame.draw.rect(surface, (50, 50, 50), (fuel_x, fuel_y, fuel_bar_width, fuel_bar_height))
    if forge.fuel_remaining_ms > 0:
        fuel_percent = min(1.0, forge.fuel_remaining_ms / 30000)  # Assume max 30 seconds
        pygame.draw.rect(surface, (255, 100, 0), (fuel_x, fuel_y, fuel_bar_width * fuel_percent, fuel_bar_height))
    pygame.draw.rect(surface, (255, 150, 0), (fuel_x, fuel_y, fuel_bar_width, fuel_bar_height), 2)
    
    # Input slot
    input_x = WIDTH // 2 - 150
    input_y = 150
    input_rect = pygame.Rect(input_x, input_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
    pygame.draw.rect(surface, (60, 60, 60), input_rect)
    pygame.draw.rect(surface, (100, 100, 100), input_rect, 2)
    
    input_label = fire_font.render("Input", True, (200, 200, 200))
    surface.blit(input_label, (input_x, input_y - 30))
    
    if forge.input_item:
        item_surface = get_item_surface(forge.input_item["type"], INVENTORY_SLOT_SIZE - 6)
        surface.blit(item_surface, (input_x + 3, input_y + 3))
        count_text = fire_font.render(str(forge.input_item["count"]), True, (255, 255, 255))
        surface.blit(count_text, (input_x + 35, input_y + 35))
    
    # Progress bar
    progress_x = WIDTH // 2 - 50
    progress_y = 150 + INVENTORY_SLOT_SIZE + 30
    progress_width = 100
    progress_height = 20
    
    progress = forge.get_smelting_progress()
    pygame.draw.rect(surface, (50, 50, 50), (progress_x, progress_y, progress_width, progress_height))
    if progress > 0:
        pygame.draw.rect(surface, (100, 150, 255), (progress_x, progress_y, progress_width * progress, progress_height))
    pygame.draw.rect(surface, (150, 150, 150), (progress_x, progress_y, progress_width, progress_height), 2)
    
    progress_text = fire_font.render(f"{int(progress * 100)}%", True, (200, 200, 200))
    surface.blit(progress_text, (progress_x - 70, progress_y))
    
    # Output slot
    output_x = WIDTH // 2 + 50
    output_y = 150
    output_rect = pygame.Rect(output_x, output_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
    pygame.draw.rect(surface, (60, 60, 60), output_rect)
    pygame.draw.rect(surface, (100, 200, 100), output_rect, 2)
    
    output_label = fire_font.render("Output", True, (200, 200, 200))
    surface.blit(output_label, (output_x, output_y - 30))
    
    if forge.output_items:
        output_types = list(forge.output_items.keys())
        first_output = output_types[0]
        output_count = forge.output_items[first_output]
        item_surface = get_item_surface(first_output, INVENTORY_SLOT_SIZE - 6)
        surface.blit(item_surface, (output_x + 3, output_y + 3))
        count_text = fire_font.render(str(output_count), True, (255, 255, 255))
        surface.blit(count_text, (output_x + 35, output_y + 35))
    
    # Fuel slot
    fuel_slot_x = WIDTH // 2 - 150
    fuel_slot_y = 250
    fuel_slot_rect = pygame.Rect(fuel_slot_x, fuel_slot_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
    pygame.draw.rect(surface, (60, 60, 60), fuel_slot_rect)
    pygame.draw.rect(surface, (200, 100, 0), fuel_slot_rect, 2)
    
    fuel_slot_label = fire_font.render("Fuel", True, (200, 200, 200))
    surface.blit(fuel_slot_label, (fuel_slot_x, fuel_slot_y - 30))
    
    if forge.fuel_item:
        item_surface = get_item_surface(forge.fuel_item["type"], INVENTORY_SLOT_SIZE - 6)
        surface.blit(item_surface, (fuel_slot_x + 3, fuel_slot_y + 3))
        count_text = fire_font.render(str(forge.fuel_item["count"]), True, (255, 255, 255))
        surface.blit(count_text, (fuel_slot_x + 35, fuel_slot_y + 35))
    
    # Instructions
    inst_font = pygame.font.Font(None, 16)
    inst_text = inst_font.render("Click input to add items, fuel to add fuel, output to collect smelted items.", True, (180, 180, 180))
    surface.blit(inst_text, (50, 400))
    
    close_font = pygame.font.Font(None, 18)
    close_text = close_font.render("Press E or click outside to close", True, (150, 150, 150))
    surface.blit(close_text, (WIDTH // 2 - close_text.get_width() // 2, HEIGHT - 30))


def craft_item(recipe_name, output_items, consume_plan):
    if not recipe_name or not output_items or not consume_plan:
        return False

    # Consume input items from crafting grid according to the matched recipe plan.
    for row, col, amount in consume_plan:
        slot_item = crafting_grid[row][col]
        if not slot_item:
            continue
        if isinstance(slot_item, dict):
            slot_item["count"] -= amount
            if slot_item["count"] <= 0:
                crafting_grid[row][col] = None
        else:
            crafting_grid[row][col] = None
    
    # Add output items
    for item, count in output_items.items():
        inventory[item] = inventory.get(item, 0) + count
    
    return True


last_frame_time = pygame.time.get_ticks()
running = True
while running:
    frame_time = pygame.time.get_ticks()
    delta_ms = max(1, frame_time - last_frame_time)
    last_frame_time = frame_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_state == GAME_STATE_MENU:
                if event.key == pygame.K_SPACE:
                    start_from_menu()
            elif current_state == GAME_STATE_PLAYING:
                if event.key == pygame.K_F9:
                    show_info = not show_info
                elif event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                elif event.key == pygame.K_i:
                    set_crafting_mode(False)
                    current_state = GAME_STATE_INVENTORY
                elif event.key == pygame.K_ESCAPE:
                    current_state = GAME_STATE_MENU
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                                   pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    # Map keys to hotbar slots
                    key_map = {
                        pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3, pygame.K_5: 4,
                        pygame.K_6: 5, pygame.K_7: 6, pygame.K_8: 7, pygame.K_9: 8
                    }
                    if event.key in key_map:
                        hotbar_selected = key_map[event.key]
                        # Ensure hotbar_selected stays within valid bounds
                        hotbar_selected = max(0, min(hotbar_selected, hotbar_slots - 1))
            elif current_state == GAME_STATE_INVENTORY:
                if event.key == pygame.K_i:
                    # Return all crafting items to inventory when closing inventory
                    for row in crafting_grid:
                        for item in row:
                            if item:
                                if isinstance(item, dict):
                                    item_type = item.get("type")
                                    item_count = int(item.get("count", 0))
                                else:
                                    item_type = item
                                    item_count = 1
                                if item_type and item_count > 0:
                                    inventory[item_type] = inventory.get(item_type, 0) + item_count

                    # Also return dragged stack if player is holding one
                    if drag_item:
                        inventory[drag_item["type"]] = inventory.get(drag_item["type"], 0) + drag_item["count"]
                        drag_item = None
                        drag_source = None

                    # Clear crafting grid
                    for row in crafting_grid:
                        for i in range(len(row)):
                            row[i] = None

                    set_crafting_mode(False)
                    current_state = GAME_STATE_PLAYING
            elif current_state == GAME_STATE_FORGE:
                if event.key in (pygame.K_e, pygame.K_ESCAPE):
                    opened_forge = None
                    current_state = GAME_STATE_PLAYING

        elif event.type == pygame.MOUSEBUTTONDOWN and current_state == GAME_STATE_MENU:
            if event.button == 1:
                if menu_new_button_rect.collidepoint(event.pos):
                    start_from_menu()
                elif menu_save_button_rect.collidepoint(event.pos):
                    try:
                        safe_save_game(menu_selected_slot)
                        menu_status_text = f"Saved to slot {menu_selected_slot}"
                    except OSError:
                        menu_status_text = "Save failed"
                    menu_status_until = pygame.time.get_ticks() + 1800
                else:
                    for i, rect in enumerate(menu_slot_rects, start=1):
                        if rect.collidepoint(event.pos):
                            menu_selected_slot = i
                            loaded = safe_load_game(i)
                            if loaded:
                                menu_status_text = f"Loaded slot {i}"
                                menu_status_until = pygame.time.get_ticks() + 1200
                                current_state = GAME_STATE_PLAYING
                            else:
                                menu_status_text = f"Slot {i} is empty"
                                menu_status_until = pygame.time.get_ticks() + 1200
                            break
        
        elif event.type == pygame.MOUSEBUTTONDOWN and current_state == GAME_STATE_INVENTORY:
            inv_start_x = 50
            inv_start_y = 80
            active_rows, active_cols = get_active_crafting_size()
            craft_start_x = inv_start_x + (INVENTORY_COLS + 1) * (INVENTORY_SLOT_SIZE + 5)
            craft_start_y = inv_start_y
            result_x = craft_start_x + active_cols * (INVENTORY_SLOT_SIZE + 5) + 15
            result_y = craft_start_y + INVENTORY_SLOT_SIZE // 2
            result_rect = pygame.Rect(result_x, result_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
            
            if event.button == 1:
                # Click result to craft
                if result_rect.collidepoint(event.pos) and not drag_item:
                    recipe_name, recipe_output, consume_plan = get_crafting_recipe()
                    if recipe_output:
                        craft_item(recipe_name, recipe_output, consume_plan)
                elif not drag_item:
                    # Pick up full stack from crafting slot first
                    found = False
                    for row in range(active_rows):
                        for col in range(active_cols):
                            slot_x = craft_start_x + col * (INVENTORY_SLOT_SIZE + 5)
                            slot_y = craft_start_y + row * (INVENTORY_SLOT_SIZE + 5)
                            slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)

                            if slot_rect.collidepoint(event.pos) and crafting_grid[row][col] is not None:
                                slot_item = crafting_grid[row][col]
                                if isinstance(slot_item, dict):
                                    drag_item = {"type": slot_item["type"], "count": int(slot_item["count"])}
                                else:
                                    drag_item = {"type": slot_item, "count": 1}
                                drag_source = ("crafting", (row, col))
                                crafting_grid[row][col] = None
                                found = True
                                break
                        if found:
                            break

                    # Otherwise pick up full stack from inventory
                    if not found:
                        all_items = get_inventory_items_list()
                        slot_index = 0
                        for row in range(INVENTORY_ROWS):
                            for col in range(INVENTORY_COLS):
                                slot_x = inv_start_x + col * (INVENTORY_SLOT_SIZE + 5)
                                slot_y = inv_start_y + row * (INVENTORY_SLOT_SIZE + 5)
                                slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)

                                if slot_rect.collidepoint(event.pos) and slot_index < len(all_items):
                                    item_type = all_items[slot_index]["type"]
                                    item_count = inventory.get(item_type, 0)
                                    if item_count > 0:
                                        drag_item = {"type": item_type, "count": item_count}
                                        drag_source = ("inventory", slot_index)
                                        inventory[item_type] = 0
                                    found = True
                                    break
                                slot_index += 1
                            if found:
                                break

            elif event.button == 3 and drag_item:
                # Right-click drops one item at a time
                dropped_one = False

                # Try crafting grid first
                for row in range(active_rows):
                    for col in range(active_cols):
                        slot_x = craft_start_x + col * (INVENTORY_SLOT_SIZE + 5)
                        slot_y = craft_start_y + row * (INVENTORY_SLOT_SIZE + 5)
                        slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
                        if slot_rect.collidepoint(event.pos):
                            slot_item = crafting_grid[row][col]
                            if slot_item is None:
                                crafting_grid[row][col] = {"type": drag_item["type"], "count": 1}
                                dropped_one = True
                            elif slot_item.get("type") == drag_item["type"]:
                                slot_item["count"] += 1
                                dropped_one = True
                            break
                    if dropped_one:
                        break

                # Or drop back to inventory as single item
                if not dropped_one:
                    slot_index = 0
                    all_items = get_inventory_items_list()
                    for row in range(INVENTORY_ROWS):
                        for col in range(INVENTORY_COLS):
                            slot_x = inv_start_x + col * (INVENTORY_SLOT_SIZE + 5)
                            slot_y = inv_start_y + row * (INVENTORY_SLOT_SIZE + 5)
                            slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
                            if slot_rect.collidepoint(event.pos):
                                inventory[drag_item["type"]] = inventory.get(drag_item["type"], 0) + 1
                                dropped_one = True
                                break
                            slot_index += 1
                        if dropped_one:
                            break

                if dropped_one:
                    drag_item["count"] -= 1
                    if drag_item["count"] <= 0:
                        drag_item = None
                        drag_source = None
        
        elif event.type == pygame.MOUSEBUTTONUP and current_state == GAME_STATE_INVENTORY:
            if drag_item and event.button == 1:
                inv_start_x = 50
                inv_start_y = 80
                active_rows, active_cols = get_active_crafting_size()
                craft_start_x = inv_start_x + (INVENTORY_COLS + 1) * (INVENTORY_SLOT_SIZE + 5)
                craft_start_y = inv_start_y
                
                placed = False
                
                # Check if dropped on crafting grid
                for row in range(active_rows):
                    for col in range(active_cols):
                        slot_x = craft_start_x + col * (INVENTORY_SLOT_SIZE + 5)
                        slot_y = craft_start_y + row * (INVENTORY_SLOT_SIZE + 5)
                        slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
                        
                        if slot_rect.collidepoint(event.pos):
                            slot_item = crafting_grid[row][col]
                            if slot_item is None:
                                crafting_grid[row][col] = {"type": drag_item["type"], "count": drag_item["count"]}
                                placed = True
                            elif slot_item.get("type") == drag_item["type"]:
                                slot_item["count"] += drag_item["count"]
                                placed = True
                            else:
                                # Different type in slot, keep holding item
                                placed = False
                            break
                    if placed:
                        break
                
                # Check if dropped on inventory grid
                if not placed:
                    for row in range(INVENTORY_ROWS):
                        for col in range(INVENTORY_COLS):
                            slot_x = inv_start_x + col * (INVENTORY_SLOT_SIZE + 5)
                            slot_y = inv_start_y + row * (INVENTORY_SLOT_SIZE + 5)
                            slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
                            
                            if slot_rect.collidepoint(event.pos):
                                inventory[drag_item["type"]] = inventory.get(drag_item["type"], 0) + drag_item["count"]
                                placed = True
                                break
                        if placed:
                            break
                
                # If not placed anywhere, return to source
                if not placed:
                    if drag_source and drag_source[0] == "crafting":
                        row, col = drag_source[1]
                        if crafting_grid[row][col] is None:
                            crafting_grid[row][col] = {"type": drag_item["type"], "count": drag_item["count"]}
                        elif crafting_grid[row][col].get("type") == drag_item["type"]:
                            crafting_grid[row][col]["count"] += drag_item["count"]
                        else:
                            inventory[drag_item["type"]] = inventory.get(drag_item["type"], 0) + drag_item["count"]
                    else:
                        inventory[drag_item["type"]] = inventory.get(drag_item["type"], 0) + drag_item["count"]
                
                drag_item = None
                drag_source = None
        
        elif event.type == pygame.MOUSEBUTTONDOWN and current_state == GAME_STATE_PLAYING:
            if fullscreen_button_rect.collidepoint(event.pos):
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
            elif event.button == 3:  # Right-click for placing / interacting
                camera_x = player_world_x - WIDTH // 2
                camera_y = player_rect.centery - HEIGHT // 2
                world_x = event.pos[0] + camera_x
                world_y = event.pos[1] + camera_y

                # Snap click to world grid for interaction with placed blocks
                grid_x = int(world_x // TILE_SIZE) * TILE_SIZE
                grid_y = int(world_y // TILE_SIZE) * TILE_SIZE

                clicked_forge = get_forge_at(world_x, world_y)
                if clicked_forge and abs(player_world_x - clicked_forge.x) <= 180:
                    opened_forge = clicked_forge
                    current_state = GAME_STATE_FORGE
                else:
                    # Use crafting table by right-clicking the placed block
                    clicked_table = next(
                        (
                            b
                            for b in placed_blocks
                            if b["type"] == "crafting_table" and get_block_world_rect(b).collidepoint(world_x, world_y)
                        ),
                        None,
                    )
                    if clicked_table and abs(player_world_x - clicked_table["x"]) <= 180:
                        set_crafting_mode(True)
                        current_state = GAME_STATE_INVENTORY
                    else:
                        hotbar_slot = hotbar_items[hotbar_selected]
                        placing_item = hotbar_slot["type"] if hotbar_slot else None
                        if placing_item in PLACEABLE_ITEMS and inventory.get(placing_item, 0) > 0:
                            place_width, place_height = get_block_dimensions(placing_item)
                            placement_rect = pygame.Rect(grid_x, grid_y, place_width, place_height)
                            block_exists = any(
                                r.colliderect(placement_rect)
                                for r in get_nearby_occupied_rects(
                                    placement_rect.centerx,
                                    placement_rect.centery,
                                    half_w_tiles=8,
                                    up_tiles=8,
                                    down_tiles=10,
                                )
                            )
                            inside_player = placement_rect.colliderect(get_player_world_rect())

                            if not block_exists and not inside_player:
                                if placing_item == "forge":
                                    placed_forges.append(Forge(grid_x, grid_y))
                                elif placing_item == "water":
                                    placed_blocks.append({"x": grid_x, "y": grid_y, "type": "water"})
                                else:
                                    placed_blocks.append({"x": grid_x, "y": grid_y, "type": placing_item})
                                inventory[placing_item] -= 1
            else:  # Left-click for tree punching / block breaking
                camera_x = player_world_x - WIDTH // 2
                camera_y = player_rect.centery - HEIGHT // 2
                world_x = event.pos[0] + camera_x
                world_y = event.pos[1] + camera_y
                click_time = pygame.time.get_ticks()

                # Check placed forge breaking first
                block_hit = False
                for forge in placed_forges[:]:
                    forge_rect = pygame.Rect(forge.rect.x - camera_x, forge.rect.y - camera_y, forge.rect.width, forge.rect.height)
                    if forge_rect.collidepoint(event.pos):
                        if abs(player_world_x - forge.x) < 150:
                            inventory["forge"] = inventory.get("forge", 0) + 1
                            placed_forges.remove(forge)
                        block_hit = True
                        break
                if not block_hit:
                    for block in placed_blocks[:]:
                        world_block_rect = get_block_world_rect(block)
                        block_rect = pygame.Rect(world_block_rect.x - camera_x, world_block_rect.y - camera_y, world_block_rect.width, world_block_rect.height)
                        if block_rect.collidepoint(event.pos):
                            # Prevent breaking water blocks
                            if block["type"] == "water":
                                block_hit = True
                                break
                            if abs(player_world_x - block["x"]) < 150:
                                inventory[block["type"]] = inventory.get(block["type"], 0) + 1
                                placed_blocks.remove(block)
                            block_hit = True
                            break

                # Punch crabs if no placed block was hit
                if not block_hit:
                    for crab in crabs[:]:
                        crab_rect = crab.get_world_rect()
                        screen_rect = pygame.Rect(crab_rect.x - camera_x, crab_rect.y - camera_y, crab_rect.width, crab_rect.height)
                        if screen_rect.collidepoint(event.pos):
                            if abs(player_world_x - crab.x) < 150:
                                crab.health -= 1
                                crab.flee_until = click_time + 2500
                                crab.direction = -1 if player_world_x > crab.x else 1
                                crab.jump_on_hit()
                                if crab.health <= 0:
                                    crabs.remove(crab)
                            block_hit = True
                            break

                # Break terrain if no placed block was hit
                if not block_hit:
                    terrain_tile_x = int(world_x // TILE_SIZE) * TILE_SIZE
                    terrain_tile_y = int(world_y // TILE_SIZE) * TILE_SIZE
                    terrain_distance = abs(player_world_x - (terrain_tile_x + TILE_SIZE // 2))
                    if terrain_distance < 150 and break_terrain_at(world_x, world_y):
                        block_hit = True

                # Check for tree punching if no block was hit
                if not block_hit:
                    for tree in trees[:]:
                        tree.sync_to_surface()
                        tree_screen_x = tree.x - camera_x
                        tree_screen_y = tree.y - camera_y
                        tree_rect = pygame.Rect(tree_screen_x, tree_screen_y, tree.width, tree.height)
                        if tree_rect.collidepoint(event.pos):
                            distance = abs(player_world_x - tree.x)
                            if distance < 150:
                                broken_type = tree.break_block_at(world_x, world_y)
                                if broken_type:
                                    inventory[broken_type] = inventory.get(broken_type, 0) + 1
                                    if tree.is_fully_broken():
                                        pending_trees.append({
                                            "x": tree.x, "y": tree.y,
                                            "leaves_type": tree.leaves_type,
                                            "wood_type": tree.wood_type,
                                            "regrow_at": pygame.time.get_ticks() + TREE_REGROW_TIME,
                                        })
                                        trees.remove(tree)
                            break

        elif event.type == pygame.MOUSEBUTTONDOWN and current_state == GAME_STATE_FORGE:
            if event.button == 1 and opened_forge:
                input_x = WIDTH // 2 - 150
                input_y = 150
                input_rect = pygame.Rect(input_x, input_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
                output_x = WIDTH // 2 + 50
                output_y = 150
                output_rect = pygame.Rect(output_x, output_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
                fuel_slot_x = WIDTH // 2 - 150
                fuel_slot_y = 250
                fuel_slot_rect = pygame.Rect(fuel_slot_x, fuel_slot_y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)

                if input_rect.collidepoint(event.pos):
                    hotbar_slot = hotbar_items[hotbar_selected]
                    placing_item = hotbar_slot["type"] if hotbar_slot else None
                    if placing_item and inventory.get(placing_item, 0) > 0 and opened_forge.add_input(placing_item):
                        inventory[placing_item] -= 1
                elif fuel_slot_rect.collidepoint(event.pos):
                    hotbar_slot = hotbar_items[hotbar_selected]
                    placing_item = hotbar_slot["type"] if hotbar_slot else None
                    if placing_item and inventory.get(placing_item, 0) > 0 and opened_forge.add_fuel(placing_item):
                        inventory[placing_item] -= 1
                elif output_rect.collidepoint(event.pos):
                    collected = opened_forge.collect_output()
                    for item_type, count in collected.items():
                        inventory[item_type] = inventory.get(item_type, 0) + count
                else:
                    opened_forge = None
                    current_state = GAME_STATE_PLAYING
            else:
                opened_forge = None
                current_state = GAME_STATE_PLAYING
                current_state = GAME_STATE_PLAYING
    
    if current_state == GAME_STATE_MENU:
        draw_menu(screen)
    elif current_state == GAME_STATE_INVENTORY:
        draw_inventory(screen)
    elif current_state == GAME_STATE_FORGE:
        draw_forge(screen, opened_forge)
    elif current_state == GAME_STATE_PLAYING:
        # --- INPUT ---
        keys = pygame.key.get_pressed()

        move_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_x += 1

        # --- WATER CHECK ---
        in_water = is_player_in_water(player_world_x, player_rect)

        # --- HORIZONTAL MOVEMENT ---
        if in_water:
            move_speed = PLAYER_SPEED * 0.5  # slow in water
        else:
            move_speed = PLAYER_SPEED

        # Apply movement with collision detection
        pw = player_rect.width
        ph = player_rect.height
        new_x = player_world_x + move_x * move_speed
        
        # Check collision at new position
        test_rect = pygame.Rect(new_x - pw // 2, player_rect.y, pw, ph)
        collision = False
        
        # Check terrain collisions (always check, regardless of water)
        for tile_x in range(int(new_x // TILE_SIZE) - 1, int(new_x // TILE_SIZE) + 2):
            for tile_y in range(int(player_rect.y // TILE_SIZE), int((player_rect.y + ph) // TILE_SIZE) + 1):
                if get_terrain_tile(tile_x, tile_y):
                    tile_rect = pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if test_rect.colliderect(tile_rect):
                        collision = True
                        break
            if collision:
                break
        
        # Check block collisions (always check, regardless of water) - get all non-water blocks
        if not collision:
            for block in placed_blocks:
                if block.get("type") == "water":  # Skip water blocks
                    continue
                block_rect = get_block_world_rect(block)
                if test_rect.colliderect(block_rect):
                    collision = True
                    break
            
            # Also check forges
            if not collision:
                for forge in placed_forges:
                    if test_rect.colliderect(forge.rect):
                        collision = True
                        break
        
        # Only move if no collision
        if not collision:
            player_world_x = new_x
        
        # Update direction for animation
        if move_x < 0:
            player_direction = "left"
            player_moving = True
        elif move_x > 0:
            player_direction = "right"
            player_moving = True
        else:
            player_moving = False

        # --- VERTICAL PHYSICS ---
        if in_water:
            # buoyancy (slow sinking)
            player_vel_y += GRAVITY * 0.15

            # cap fall speed
            if player_vel_y > 3:
                player_vel_y = 3

            # swim upward
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player_vel_y = -3
            # swim downward
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player_vel_y = 3
            # float upward slightly when not actively swimming
            else:
                player_vel_y -= 0.2

            # smooth movement
            player_vel_y *= 0.9

        else:
            # normal gravity
            player_vel_y += GRAVITY
            if player_vel_y > MAX_FALL_SPEED:
                player_vel_y = MAX_FALL_SPEED

            # jump
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                # only allow jump if on ground
                player_rect.y += 2
                on_ground = False
                for tile_x in range(int(player_world_x // TILE_SIZE) - 1, int(player_world_x // TILE_SIZE) + 2):
                    tile_y = int((player_rect.bottom) // TILE_SIZE)
                    if get_terrain_tile(tile_x, tile_y):
                        on_ground = True
                        break
                player_rect.y -= 2

                if on_ground:
                    player_vel_y = JUMP_SPEED

        # --- APPLY VERTICAL MOVEMENT ---
        player_rect.y += player_vel_y

        # --- CEILING COLLISION (when moving upward) ---
        if player_vel_y < 0:  # Moving upward
            pw = player_rect.width
            ph = player_rect.height
            test_head = pygame.Rect(player_world_x - pw // 2, player_rect.top, pw, 4)
            
            # Check if actively swimming up
            actively_swimming_up = in_water and (keys[pygame.K_w] or keys[pygame.K_UP])
            
            # Check terrain collision
            for tile_x in range(int(player_world_x // TILE_SIZE) - 1, int(player_world_x // TILE_SIZE) + 2):
                tile_y = int((player_rect.top) // TILE_SIZE)
                if get_terrain_tile(tile_x, tile_y):
                    tile_rect = pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if test_head.colliderect(tile_rect):
                        player_rect.top = tile_rect.bottom
                        if not actively_swimming_up:  # Only stop movement when not actively swimming up
                            player_vel_y = 0
                        break
            
            # Check block collision
            for block in placed_blocks:
                if block.get("type") == "water":  # Skip water blocks
                    continue
                block_rect = get_block_world_rect(block)
                if test_head.colliderect(block_rect):
                    player_rect.top = block_rect.bottom
                    if not actively_swimming_up:  # Only stop movement when not actively swimming up
                        player_vel_y = 0
                    break
            
            # Check forges
            for forge in placed_forges:
                if test_head.colliderect(forge.rect):
                    player_rect.top = forge.rect.bottom
                    if not actively_swimming_up:  # Only stop movement when not actively swimming up
                        player_vel_y = 0
                    break

        # --- GROUND COLLISION (terrain and blocks, NOT water) ---
        pw = player_rect.width
        ph = player_rect.height
        player_on_ground = False
        
        # Only apply ground collision when not actively swimming down
        actively_swimming_down = in_water and (keys[pygame.K_s] or keys[pygame.K_DOWN])
        
        if not actively_swimming_down:
            # Check terrain collision
            for tile_x in range(int(player_world_x // TILE_SIZE) - 1, int(player_world_x // TILE_SIZE) + 2):
                tile_y = int((player_rect.bottom) // TILE_SIZE)
                if get_terrain_tile(tile_x, tile_y):
                    ground_y = tile_y * TILE_SIZE
                    if player_rect.bottom >= ground_y:
                        player_rect.bottom = ground_y
                        if not in_water:  # Only stop vertical movement when not in water
                            player_vel_y = 0
                        player_on_ground = True
                        break
            
            # Check block collision if not on ground yet
            if not player_on_ground:
                test_feet = pygame.Rect(player_world_x - pw // 2, player_rect.bottom - 2, pw, 4)
                for block in placed_blocks:
                    if block.get("type") == "water":  # Skip water blocks
                        continue
                    block_rect = get_block_world_rect(block)
                    if test_feet.colliderect(block_rect):
                        player_rect.bottom = block_rect.top
                        if not in_water:  # Only stop vertical movement when not in water
                            player_vel_y = 0
                        player_on_ground = True
                        break
                
                # Also check forges
                if not player_on_ground:
                    for forge in placed_forges:
                        if test_feet.colliderect(forge.rect):
                            player_rect.bottom = forge.rect.top
                            if not in_water:  # Only stop vertical movement when not in water
                                player_vel_y = 0
                            player_on_ground = True
                            break
        
        # Fall damage tracking
        landed_this_frame = False
        if player_vel_y > 0:  # Only when falling
            # Check if hit ground after falling
            for tile_x in range(int(player_world_x // TILE_SIZE) - 1, int(player_world_x // TILE_SIZE) + 2):
                tile_y = int((player_rect.bottom) // TILE_SIZE)
                if get_terrain_tile(tile_x, tile_y):
                    if player_fall_start_bottom is not None and not in_water:
                        apply_fall_damage(player_rect.bottom - player_fall_start_bottom)
                    player_fall_start_bottom = None
                    landed_this_frame = True
                    break
        
        if not landed_this_frame:
            if not in_water and player_vel_y > 0:  # Falling
                if player_fall_start_bottom is None:
                    player_fall_start_bottom = player_rect.bottom
            else:
                player_fall_start_bottom = None

        current_time = pygame.time.get_ticks()
        
        # Spread water every 500ms like Minecraft fluid ticks
        if current_time - last_water_spread_time > 500:
            spread_water()
            last_water_spread_time = current_time
        
        state = "jump" if not player_on_ground else ("walk" if player_moving else "stand")
        sprite_key = f"{state}_{player_direction}"
        frames = player_sprites.get(sprite_key, player_sprites["stand_right"])

        if state == "walk" and player_moving and player_on_ground:
            if current_time - player_last_frame_time >= ANIMATION_INTERVAL:
                player_frame = (player_frame + 1) % len(frames)
                player_last_frame_time = current_time
        else:
            player_frame = 0

        player_sprite = frames[player_frame] if frames else player_sprites["stand_right"][0]

        # Generate chunks ahead of the player
        _player_chunk = int(player_world_x // CHUNK_WIDTH)
        for _ci in range(_player_chunk - 3, _player_chunk + 4):
            generate_chunk(_ci)
            generate_crabs_for_chunk(_ci)

        unload_distant_chunks(_player_chunk)

        update_dropped_items_and_pickup(current_time)
        for forge in placed_forges:
            forge.update(delta_ms)

        update_crabs_efficiently(current_time, player_world_x)

        # Regrow cut trees
        regrown = [t for t in pending_trees if t["regrow_at"] <= current_time]
        for t in regrown:
            trees.append(Tree(t["x"], t["y"], t["leaves_type"], t["wood_type"]))
            pending_trees.remove(t)

        camera_x = player_world_x - WIDTH // 2
        camera_y = player_rect.centery - HEIGHT // 2
        if current_time < player_damage_shake_until:
            shake_x = random.randint(-PLAYER_DAMAGE_SHAKE_PX, PLAYER_DAMAGE_SHAKE_PX)
            shake_y = random.randint(-PLAYER_DAMAGE_SHAKE_PX, PLAYER_DAMAGE_SHAKE_PX)
            camera_x += shake_x
            camera_y += shake_y
        bic = int(player_world_x // WIDTH) % len(BIOMES)
        player_screen_x = player_world_x - camera_x
        player_screen_y = player_rect.y - camera_y

        draw_sky(screen, camera_x, camera_y)
        for cloud in clouds:
            cloud.draw(screen, camera_x, camera_y)
        if show_info:
            draw_grid(screen, camera_x, camera_y)
        draw_ground(screen, camera_x, camera_y)
        draw_mountains(screen, camera_x, camera_y)
        for tree in trees:
            tree.draw(screen, camera_x, camera_y)
        for crab in crabs:
            crab.draw(screen, camera_x, camera_y)
        draw_dropped_items(screen, camera_x, camera_y, current_time)
        draw_placed_blocks(screen, camera_x, camera_y)
        screen.blit(player_sprite, (player_screen_x - pw // 2, player_screen_y))
        draw_item_in_hand(screen, player_screen_x - pw // 2, player_screen_y, player_direction)

        # Draw fullscreen button
        mouse_pos = pygame.mouse.get_pos()
        button_color = fullscreen_button_hover_color if fullscreen_button_rect.collidepoint(mouse_pos) else fullscreen_button_color
        pygame.draw.rect(screen, button_color, fullscreen_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), fullscreen_button_rect, 2)
        button_text = button_font.render("Fullscreen", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=fullscreen_button_rect.center)
        screen.blit(button_text, text_rect)

        # Draw health HUD
        pygame.draw.rect(screen, (25, 25, 25), (10, 10, 164, 18))
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, 164, 18), 1)
        fill_w = int((player_health / PLAYER_MAX_HEALTH) * 160)
        pygame.draw.rect(screen, (210, 40, 40), (12, 12, fill_w, 14))
        hp_text = info_font.render(f"HP {player_health}/{PLAYER_MAX_HEALTH}", True, (255, 255, 255))
        screen.blit(hp_text, (12, 31))

        # Damage effect: brief red pulse over the screen when the player takes damage.
        if current_time < player_damage_flash_until:
            remaining = player_damage_flash_until - current_time
            alpha = max(0, min(140, int(140 * (remaining / PLAYER_DAMAGE_FLASH_MS))))
            damage_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            damage_overlay.fill((200, 20, 20, alpha))
            screen.blit(damage_overlay, (0, 0))

        if current_time < player_death_message_until:
            death_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            death_overlay.fill((12, 0, 0, 180))
            screen.blit(death_overlay, (0, 0))

            panel_rect = pygame.Rect(WIDTH // 2 - 220, HEIGHT // 2 - 90, 440, 180)
            pygame.draw.rect(screen, (20, 0, 0), panel_rect)
            pygame.draw.rect(screen, (170, 20, 20), panel_rect, 3)
            pygame.draw.line(screen, (110, 10, 10), (panel_rect.left, panel_rect.centery), (panel_rect.right, panel_rect.centery), 1)

            death_title_font = pygame.font.Font(None, 84)
            death_title = death_title_font.render("YOU DIED", True, (255, 70, 70))
            death_title_rect = death_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 26))
            screen.blit(death_title, death_title_rect)

            death_sub_font = pygame.font.Font(None, 28)
            death_sub = death_sub_font.render("Respawning...", True, (230, 180, 180))
            death_sub_rect = death_sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 34))
            screen.blit(death_sub, death_sub_rect)

        # Draw hotbar
        hotbar_start_x = (WIDTH - hotbar_slots * HOTBAR_SLOT_SIZE) // 2
        for i in range(hotbar_slots):
            slot_x = hotbar_start_x + i * HOTBAR_SLOT_SIZE
            slot_rect = pygame.Rect(slot_x, HOTBAR_Y, HOTBAR_SLOT_SIZE, HOTBAR_SLOT_SIZE)
            
            # Highlight selected slot
            if i == hotbar_selected:
                pygame.draw.rect(screen, (255, 200, 0), slot_rect, 3)
            else:
                pygame.draw.rect(screen, (100, 100, 100), slot_rect)
            pygame.draw.rect(screen, (255, 255, 255), slot_rect, 1)
            
            # Draw item texture and count
            if hotbar_items[i]:
                item = hotbar_items[i]
                item_count = inventory.get(item["type"], 0)
                item_surface = get_item_surface(item["type"], HOTBAR_SLOT_SIZE - 6)
                screen.blit(item_surface, (slot_x + 3, HOTBAR_Y + 3))
                
                # Draw count
                small_font = pygame.font.Font(None, 12)
                count_text = small_font.render(str(item_count), True, (255, 255, 255))
                count_rect = count_text.get_rect(bottomright=(slot_rect.right - 2, slot_rect.bottom - 2))
                screen.blit(count_text, count_rect)

        if show_info:
            fps_text = info_font.render(f"FPS: {int(clock.get_fps())}", True, (255,255,255))
            coord_text = info_font.render(f"X: {int(player_world_x)}, Y: {int(player_rect.y)}", True, (255,255,255))
            biome_text = info_font.render(f"Biome: {BIOME_NAMES[bic]}", True, (255,255,255))
            screen.blit(fps_text, (10, 10))
            screen.blit(coord_text, (10, 30))
            screen.blit(biome_text, (10, 50))
        
        # Block placement preview from hotbar selection
        hotbar_slot = hotbar_items[hotbar_selected]
        placing_item = hotbar_slot["type"] if hotbar_slot else None
        if placing_item in PLACEABLE_ITEMS and inventory.get(placing_item, 0) > 0:
            placement_text = info_font.render(f"Placing: {placing_item.upper()} (slot {hotbar_selected+1}) - Right-click to place", True, (100, 255, 100))
            screen.blit(placement_text, (10, 70))
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_mouse_x = mouse_x + camera_x
            world_mouse_y = mouse_y + camera_y
            grid_world_x = int(world_mouse_x // TILE_SIZE) * TILE_SIZE
            grid_world_y = int(world_mouse_y // TILE_SIZE) * TILE_SIZE
            grid_screen_x = grid_world_x - camera_x
            grid_screen_y = grid_world_y - camera_y
            preview_width, preview_height = get_block_dimensions(placing_item)
            preview_rect = pygame.Rect(grid_world_x, grid_world_y, preview_width, preview_height)
            collides_existing = any(
                r.colliderect(preview_rect)
                for r in get_nearby_occupied_rects(
                    preview_rect.centerx,
                    preview_rect.centery,
                    half_w_tiles=8,
                    up_tiles=8,
                    down_tiles=10,
                )
            )
            can_place_here = not preview_rect.colliderect(get_player_world_rect()) and not collides_existing
            
            if can_place_here:
                preview_surf = get_item_surface(placing_item, max(preview_width, preview_height)).copy()
                if preview_surf.get_width() != preview_width or preview_surf.get_height() != preview_height:
                    preview_surf = pygame.transform.scale(preview_surf, (preview_width, preview_height))
                preview_surf.set_alpha(160)
                screen.blit(preview_surf, (grid_screen_x, grid_screen_y))
                pygame.draw.rect(screen, (255, 255, 255), (grid_screen_x, grid_screen_y, preview_width, preview_height), 1)

    # Update hotbar items based on current inventory
    hotbar_items: list[None] = get_hotbar_items()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
