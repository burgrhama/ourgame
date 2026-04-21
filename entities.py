# entities.py - Game entity classes (Player, Tree, Crab, Forge)
import pygame
import random
from constants import *


class Tree:
    """Minecraft-style tree with destructible blocks."""
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

    def sync_to_surface(self, get_surface_world_y_func):
        """Align tree to terrain surface."""
        trunk_x = self.x + self.width // 2
        self.y = get_surface_world_y_func(trunk_x) - self.height
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface, camera_x, camera_y, get_item_surface_func):
        """Draw tree with broken blocks visible."""
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        if draw_x < -150 or draw_x > WIDTH + 150 or draw_y < -220 or draw_y > HEIGHT + 80:
            return
        
        draw_order = ["wood", "leaves"]
        for layer_type in draw_order:
            for idx, (block_type, off_x, off_y) in enumerate(self.BLOCK_LAYOUT):
                if block_type != layer_type or idx in self.broken_blocks:
                    continue
                tile = get_item_surface_func(block_type, TILE_SIZE)
                surface.blit(tile, (draw_x + off_x, draw_y + off_y))

    def break_block_at(self, world_x, world_y, inventory, hotbar_items, hotbar_selected, use_tool_func):
        """Break a tree block at world coordinates."""
        self.sync_to_surface(lambda x: 0)  # Placeholder
        for idx, (block_type, off_x, off_y) in enumerate(self.BLOCK_LAYOUT):
            if idx in self.broken_blocks:
                continue
            rect = pygame.Rect(int(self.x + off_x), int(self.y + off_y), TILE_SIZE, TILE_SIZE)
            if rect.collidepoint(world_x, world_y):
                hits = self.block_damage.get(idx, 0) + 1
                self.block_damage[idx] = hits
                
                selected_item = hotbar_items[hotbar_selected] if hotbar_selected < len(hotbar_items) else None
                has_axe = selected_item and selected_item.get("type") == "axe" and inventory.get("axe", 0) > 0
                needed_hits = WOOD_BLOCK_HITS_AXE if block_type == "wood" and has_axe else TREE_BLOCK_HITS
                
                if hits < needed_hits:
                    return None
                
                self.block_damage.pop(idx, None)
                self.broken_blocks.add(idx)
                self.health = float(self.max_health - len(self.broken_blocks))
                
                if has_axe:
                    use_tool_func("axe")
                
                return block_type
        return None

    def is_fully_broken(self):
        """Check if all blocks are broken."""
        return len(self.broken_blocks) >= len(self.BLOCK_LAYOUT)

    def to_dict(self):
        """Serialize tree to dictionary."""
        return {
            "x": int(self.x),
            "y": int(self.y),
            "leaves_type": self.leaves_type,
            "wood_type": self.wood_type,
            "health": float(self.health),
            "max_health": float(self.max_health),
            "broken_blocks": sorted(list(self.broken_blocks)),
            "block_damage": {str(idx): int(hits) for idx, hits in self.block_damage.items()},
        }

    @staticmethod
    def from_dict(data):
        """Deserialize tree from dictionary."""
        tree = Tree(
            int(data.get("x", 0)),
            int(data.get("y", 0)),
            data.get("leaves_type", "leaves1"),
            data.get("wood_type", "wood"),
        )
        broken = data.get("broken_blocks", [])
        tree.broken_blocks = {int(idx) for idx in broken if isinstance(idx, (int, float)) and 0 <= int(idx) < len(Tree.BLOCK_LAYOUT)}
        saved_damage = data.get("block_damage", {})
        tree.block_damage = {int(idx): int(hits) for idx, hits in saved_damage.items() if str(idx).isdigit()}
        tree.max_health = float(len(Tree.BLOCK_LAYOUT))
        tree.health = float(tree.max_health - len(tree.broken_blocks))
        return tree


class Crab:
    """Simple crab enemy that walks and flees."""
    def __init__(self, x):
        self.x = float(x)
        self.width = 42
        self.height = 30
        self.direction = random.choice([-1, 1])
        self.speed = 0.55
        self.y = 0  # Will be set by caller
        self.move_until = pygame.time.get_ticks() + random.randint(900, 2200)
        self.pause_until = 0
        self.frame_toggle = False
        self.health = CRAB_HITS_HAND
        self.flee_until = 0
        self.vy = 0.0
        self.airborne = False

    def update(self, current_time, player_x, get_surface_world_y_func, get_local_solid_rects_func, crab_position_valid_func):
        """Update crab position and state."""
        distance_to_player = player_x - self.x
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
            if move_speed > 0:
                test_x = self.x + self.direction * move_speed * 0.7
                body_rect = pygame.Rect(int(test_x), int(self.y), self.width, self.height)
                if not any(body_rect.colliderect(r) for r in get_local_solid_rects_func(body_rect.centerx, body_rect.centery)):
                    self.x = test_x
            settle_y = get_surface_world_y_func(self.x) - self.height
            if settle_y is not None and self.vy >= 0 and self.y >= settle_y:
                self.y = settle_y
                self.vy = 0.0
                self.airborne = False
        elif move_speed > 0:
            next_x = self.x + self.direction * move_speed
            moved = False
            if crab_position_valid_func(next_x, self.y, self.width, self.height):
                self.x = next_x
                moved = True
            else:
                for step_up in range(4, TILE_SIZE + 1, 4):
                    try_y = self.y - step_up
                    if crab_position_valid_func(next_x, try_y, self.width, self.height):
                        self.x = next_x
                        self.y = try_y
                        moved = True
                        break
            if not moved:
                self.direction *= -1
            settle_y = get_surface_world_y_func(self.x) - self.height
            if settle_y is not None:
                self.y = settle_y
        else:
            settle_y = get_surface_world_y_func(self.x) - self.height
            if settle_y is not None:
                self.y = settle_y
        
        self.frame_toggle = (current_time // 280) % 2 == 1 and move_speed == 0

    def jump_on_hit(self):
        """Make crab jump when hit."""
        self.airborne = True
        self.vy = CRAB_JUMP_IMPULSE

    def get_world_rect(self):
        """Get crab's world collision rect."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface, camera_x, camera_y, crab_sprites):
        """Draw crab sprite."""
        draw_x = int(self.x - camera_x)
        draw_y = int(self.y - camera_y + CRAB_GROUND_SINK_PX)
        if draw_x < -self.width or draw_x > WIDTH + self.width or draw_y < -self.height or draw_y > HEIGHT + self.height:
            return
        sprite_key = "bob" if self.frame_toggle else "stand"
        sprite = crab_sprites[sprite_key].copy()
        if self.direction < 0:
            sprite = pygame.transform.flip(sprite, True, False)
        surface.blit(sprite, (draw_x, draw_y))


class Forge:
    """Minecraft-style furnace for smelting items."""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.width = TILE_SIZE * 3
        self.height = TILE_SIZE * 2
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.input_item = None
        self.fuel_item = None
        self.output_items = {}
        self.fuel_remaining_ms = 0
        self.smelt_progress_ms = 0
        self.is_smelting = False

    def try_start_smelt(self):
        """Start smelting if conditions are met."""
        if self.is_smelting or not self.input_item or self.fuel_remaining_ms <= 0:
            return
        self.is_smelting = True
        self.smelt_progress_ms = 0

    def update(self, delta_ms, get_smelt_recipe_func):
        """Update smelting progress."""
        if self.fuel_remaining_ms > 0:
            self.fuel_remaining_ms = max(0, self.fuel_remaining_ms - delta_ms)
        
        if self.is_smelting:
            self.smelt_progress_ms += delta_ms
            item_type = self.input_item["type"] if self.input_item else None
            recipe = get_smelt_recipe_func(item_type) if item_type else None
            
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

    def add_fuel(self, item_type, get_fuel_recipe_func):
        """Add fuel to forge."""
        fuel_recipe = get_fuel_recipe_func(item_type)
        if not fuel_recipe:
            return False
        if self.fuel_item and self.fuel_item["type"] != item_type:
            return False
        self.fuel_item = self.fuel_item or {"type": item_type, "count": 0}
        self.fuel_item["count"] += 1
        self.fuel_remaining_ms += fuel_recipe.get("burn_time", 10000)
        return True

    def add_input(self, item_type, get_smelt_recipe_func):
        """Add item to be smelted."""
        recipe = get_smelt_recipe_func(item_type)
        if not recipe:
            return False
        if self.input_item and self.input_item["type"] != item_type:
            return False
        self.input_item = self.input_item or {"type": item_type, "count": 0}
        self.input_item["count"] += 1
        self.try_start_smelt()
        return True

    def collect_output(self):
        """Collect smelted items."""
        collected = dict(self.output_items)
        self.output_items.clear()
        return collected

    def get_smelting_progress(self):
        """Get smelting progress 0-1."""
        if not self.is_smelting or not self.input_item:
            return 0.0
        recipe_time = SMELT_RECIPES.get(self.input_item["type"], {}).get("smelt_time", 10000)
        return min(1.0, self.smelt_progress_ms / recipe_time)

    def to_dict(self):
        """Serialize forge."""
        return {
            "x": int(self.x),
            "y": int(self.y),
            "input_item": dict(self.input_item) if self.input_item else None,
            "fuel_item": dict(self.fuel_item) if self.fuel_item else None,
            "output_items": dict(self.output_items),
            "fuel_remaining_ms": int(self.fuel_remaining_ms),
            "smelt_progress_ms": int(self.smelt_progress_ms),
            "is_smelting": bool(self.is_smelting),
        }

    @staticmethod
    def from_dict(data):
        """Deserialize forge."""
        forge = Forge(int(data.get("x", 0)), int(data.get("y", 0)))
        input_item = data.get("input_item")
        if isinstance(input_item, dict) and isinstance(input_item.get("type"), str):
            forge.input_item = {"type": input_item["type"], "count": max(1, int(input_item.get("count", 0)))}
        fuel_item = data.get("fuel_item")
        if isinstance(fuel_item, dict) and isinstance(fuel_item.get("type"), str):
            forge.fuel_item = {"type": fuel_item["type"], "count": max(1, int(fuel_item.get("count", 0)))}
        output_items = data.get("output_items", {})
        forge.output_items = {str(k): int(v) for k, v in output_items.items() if isinstance(v, (int, float)) and int(v) > 0}
        forge.fuel_remaining_ms = max(0, int(data.get("fuel_remaining_ms", 0)))
        forge.smelt_progress_ms = max(0, int(data.get("smelt_progress_ms", 0)))
        forge.is_smelting = bool(data.get("is_smelting", False))
        return forge


class Cloud:
    """Decorative cloud in sky."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface, camera_x, camera_y, sky_images):
        """Draw cloud."""
        if sky_images.get("cloud"):
            cloud = pygame.transform.scale(sky_images["cloud"], (80, 40))
            draw_x = self.x - camera_x
            draw_y = self.y - camera_y
            surface.blit(cloud, (draw_x, draw_y))
