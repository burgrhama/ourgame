# assets.py - Asset loading (sprites, images, textures)
import pygame
import os
from constants import *

# Sprite definitions
PLAYER_SPRITES_DEF = {
    "stand_right": ["MC-stand-still-look-right.png"],
    "stand_left": ["MC-stand-still-look-left.png"],
    "walk_right": ["MC-walk-right-main.png", "MC-walk-right-main-2.png", "MC-walk-right-main-3.png", "MC-walk-right.png"],
    "walk_left": ["MC-walk-left-main.png", "MC-walk-left-main-2.png", "MC-walk-left-main-3.png", "MC-walk-left.png"],
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


def load_sprite(path):
    """Load sprite and scale to 48x48."""
    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (48, 48))
    return None


def create_placeholder(color):
    """Create colored placeholder sprite."""
    sprite = pygame.Surface((48, 48), pygame.SRCALPHA)
    sprite.fill(color)
    pygame.draw.rect(sprite, (0, 0, 0), sprite.get_rect(), 2)
    return sprite


def load_player_sprites():
    """Load all player animation sprites."""
    sprites = {}
    for key, filenames in PLAYER_SPRITES_DEF.items():
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
    """Load all tile textures."""
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
    """Load tree sprite parts."""
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
    """Load sky elements."""
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
    """Load all item textures."""
    items = {}
    for key, filename in ITEM_FILENAMES.items():
        path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(path):
            items[key] = pygame.image.load(path).convert_alpha()
        else:
            items[key] = None
    return items


def load_crab_sprites():
    """Load crab sprites."""
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
    """Load forge animation frames."""
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
    """Load main title image."""
    path = os.path.join(MODEL_DIR, MAIN_NAME_FILENAME)
    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (420, 100))
    return None


def get_item_surface(item_type, size=40, tile_images=None, tree_images=None, item_images=None, forge_images=None):
    """Get pygame surface for item (texture or fallback color)."""
    if not tile_images:
        tile_images = {}
    if not tree_images:
        tree_images = {}
    if not item_images:
        item_images = {}
    if not forge_images:
        forge_images = {}
    
    # Check tile images
    if item_type == "grass" and tile_images.get("grass"):
        img = pygame.transform.scale(tile_images["grass"], (size, size))
        return img.copy()
    elif item_type in {"jord", "stone", "sand", "limestone", "copper_ore", "iron_ore", "gold_ore", "ruby"} and tile_images.get(item_type):
        img = pygame.transform.scale(tile_images[item_type], (size, size))
        return img.copy()
    
    # Check tree images
    elif item_type == "wood" and tree_images.get("wood"):
        img = pygame.transform.scale(tree_images["wood"], (size, size))
        return img.copy()
    elif item_type == "leaves" and tree_images.get("leaves1"):
        img = pygame.transform.scale(tree_images["leaves1"], (size, size))
        return img.copy()
    
    # Check item images
    elif item_type in {"planks", "axe", "knife", "pickaxe"} and item_images.get(item_type):
        img = pygame.transform.scale(item_images[item_type], (size, size))
        return img.copy()
    
    # Check crafting table
    elif item_type == "crafting_table":
        if item_images.get("crafting_table"):
            img = pygame.transform.scale(item_images["crafting_table"], (size, size))
            return img.copy()
        surface = pygame.Surface((size, size))
        surface.fill((120, 75, 35))
        pygame.draw.rect(surface, (85, 50, 25), (0, 0, size, size), 2)
        pygame.draw.line(surface, (90, 55, 30), (0, size // 2), (size, size // 2), 1)
        pygame.draw.line(surface, (90, 55, 30), (size // 2, 0), (size // 2, size), 1)
        return surface
    
    # Check forge
    elif item_type == "forge":
        if forge_images.get("idle"):
            img = pygame.transform.scale(forge_images["idle"], (size, size))
            return img.copy()
        surface = pygame.Surface((size, size))
        surface.fill((100, 100, 100))
        pygame.draw.rect(surface, (60, 60, 60), (0, 0, size, size), 2)
        pygame.draw.rect(surface, (200, 100, 50), (size // 4, size // 4, size // 2, size // 2))
        return surface
    
    # Check water
    elif item_type in {"water_top", "water_bottom", "water"} and item_images.get("water_top"):
        img = pygame.transform.scale(item_images["water_top"], (size, size))
        return img.copy()
    
    # Fallback to color
    else:
        surface = pygame.Surface((size, size))
        color = ITEM_COLORS.get(item_type, (100, 100, 100))
        surface.fill(color)
        return surface
