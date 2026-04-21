# terrain.py - Terrain generation and utilities
import random
import pygame
import math
from collections import deque
from constants import *


def get_surface_tile_y(tile_x):
    """Calculate surface tile Y based on procedural height."""
    broad_hills = math.sin(tile_x * 0.075) * 1.4
    small_hills = math.sin(tile_x * 0.21 + 1.4) * 0.9
    mountain_band = (max(0.0, math.sin(tile_x * 0.032 - 0.8)) ** 3) * 7.5
    ridge_band = (max(0.0, math.sin(tile_x * 0.017 + 2.1)) ** 4) * 9.0
    surface_offset = broad_hills + small_hills - mountain_band - ridge_band
    return max(5, min(SURFACE_TILE_Y + 2, SURFACE_TILE_Y + int(round(surface_offset))))


def get_surface_world_y(world_x):
    """Get world Y coordinate of surface at world X."""
    tile_x = int(world_x // TILE_SIZE)
    return get_surface_tile_y(tile_x) * TILE_SIZE


def carve_ellipse(tile_map, center_x, center_y, radius_x, radius_y):
    """Carve elliptical cave into tilemap."""
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
    """Flood fill water from starting point."""
    queue = deque([(start_tile_x, start_tile_y)])
    visited = set()
    max_iterations = 10000
    iterations = 0
    while queue and iterations < max_iterations:
        x, y = queue.popleft()
        iterations += 1
        if (x, y) in visited or (x, y) in chunk_tiles:
            continue
        visited.add((x, y))
        water_chunk.add((x, y))
        start_tile_x_chunk = chunk_idx * CHUNK_TILES
        end_tile_x_chunk = start_tile_x_chunk + CHUNK_TILES
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if start_tile_x_chunk <= nx < end_tile_x_chunk:
                if (nx, ny) not in visited and (nx, ny) not in chunk_tiles:
                    queue.append((nx, ny))


BIOMES = [
    [("leaves1", "wood"), ("leaves2", "wood"), ("leaves1", "wood"), ("red_leaves", "wood")],
    [("red_leaves", "wood"), ("red_leaves", "wood_hole"), ("red_leaves", "wood"), ("red_leaves", "wood")],
    [("leaves2", "wood"), ("leaves1", "wood"), ("leaves2", "wood_hole"), ("leaves1", "wood")],
    [("leaves1", "wood_hole"), ("red_leaves", "wood"), ("leaves2", "wood"), ("red_leaves", "wood_hole")],
    [],
    [],
]

BIOME_TYPES = ["forest", "forest", "forest", "forest", "desert", "ocean"]


def generate_terrain_chunk(chunk_idx, terrain_chunks, removed_terrain_tiles, placed_blocks, water_chunks):
    """Procedurally generate terrain for a chunk."""
    if chunk_idx in terrain_chunks:
        return
    
    rng = random.Random((chunk_idx * 92821) ^ (SEED >> 4))
    chunk_tiles = {}
    start_tile_x = chunk_idx * CHUNK_TILES
    
    biome_index = abs(chunk_idx) % len(BIOMES)
    biome_type = BIOME_TYPES[biome_index]
    
    # Generate base terrain
    for tile_x in range(start_tile_x, start_tile_x + CHUNK_TILES):
        surface_tile_y = get_surface_tile_y(tile_x)
        for tile_y in range(surface_tile_y, surface_tile_y + TERRAIN_DEPTH_ROWS):
            if tile_y == surface_tile_y:
                chunk_tiles[(tile_x, tile_y)] = "sand" if biome_type in ["desert", "ocean"] else "grass"
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
    
    # Carve caves
    carved_positions = set()
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
    
    # Carve chambers
    chamber_count = rng.randint(2, 4)
    for _ in range(chamber_count):
        center_x = rng.uniform(start_tile_x + 2, start_tile_x + CHUNK_TILES - 2)
        local_surface = get_surface_tile_y(int(center_x))
        center_y = rng.uniform(local_surface + 6, local_surface + TERRAIN_DEPTH_ROWS - 4)
        radius_x = rng.uniform(2.0, 4.2)
        radius_y = rng.uniform(1.8, 3.4)
        carved_positions.update(carve_ellipse(chunk_tiles, center_x, center_y, radius_x, radius_y))
    
    # Remove already-broken tiles
    for pos in list(chunk_tiles.keys()):
        if pos in removed_terrain_tiles:
            chunk_tiles.pop(pos, None)
    
    terrain_chunks[chunk_idx] = chunk_tiles
    
    # Generate water blocks for ocean biomes
    if biome_type == "ocean":
        for tile_x in range(start_tile_x, start_tile_x + CHUNK_TILES):
            surface_tile_y = get_surface_tile_y(tile_x)
            water_start_y = surface_tile_y - 1
            if water_start_y >= 0:
                world_x = tile_x * TILE_SIZE
                world_y = water_start_y * TILE_SIZE
                block_exists = any(b["x"] == world_x and b["y"] == world_y and b["type"] == "water" for b in placed_blocks)
                if not block_exists:
                    placed_blocks.append({"x": world_x, "y": world_y, "type": "water"})
        
        # Water spreading
        new_water_blocks = []
        for block in placed_blocks:
            if block["type"] != "water":
                continue
            block_x = int(block["x"] // TILE_SIZE)
            block_y = int(block["y"] // TILE_SIZE)
            
            below_y = block_y + 1
            below_world_x = block_x * TILE_SIZE
            below_world_y = below_y * TILE_SIZE
            below_exists = any(b["x"] == below_world_x and b["y"] == below_world_y and b["type"] == "water" for b in placed_blocks)
            if not below_exists and below_y < get_surface_tile_y(block_x) + 5:
                new_water_blocks.append({"x": below_world_x, "y": below_world_y, "type": "water"})
            
            for dx in [-1, 1]:
                spread_x = block_x + dx
                side_world_x = spread_x * TILE_SIZE
                side_world_y = block_y * TILE_SIZE
                side_exists = any(b["x"] == side_world_x and b["y"] == side_world_y and b["type"] == "water" for b in placed_blocks)
                if not side_exists and abs(spread_x - chunk_idx * CHUNK_TILES) < 5:
                    new_water_blocks.append({"x": side_world_x, "y": side_world_y, "type": "water"})
        
        for new_block in new_water_blocks:
            block_exists = any(b["x"] == new_block["x"] and b["y"] == new_block["y"] and b["type"] == "water" for b in placed_blocks)
            if not block_exists:
                placed_blocks.append(new_block)


def get_terrain_tile(tile_x, tile_y, terrain_chunks, removed_terrain_tiles):
    """Get terrain tile type at position."""
    surface_tile_y = get_surface_tile_y(tile_x)
    if tile_y < surface_tile_y:
        return None
    if (tile_x, tile_y) in removed_terrain_tiles:
        return None
    if tile_y >= surface_tile_y + TERRAIN_DEPTH_ROWS + 5:
        return "bedrock"
    
    chunk_idx = int((tile_x * TILE_SIZE) // CHUNK_WIDTH)
    if chunk_idx not in terrain_chunks:
        generate_terrain_chunk(chunk_idx, terrain_chunks, removed_terrain_tiles, [], {})
    
    if tile_y >= surface_tile_y + TERRAIN_DEPTH_ROWS:
        return "stone"
    
    return terrain_chunks.get(chunk_idx, {}).get((tile_x, tile_y))


def unload_distant_chunks(player_chunk_idx, terrain_chunks, water_chunks):
    """Unload chunks far from player."""
    chunks_to_unload = []
    for chunk_idx in list(terrain_chunks.keys()):
        if abs(chunk_idx - player_chunk_idx) > UNLOAD_DISTANCE_CHUNKS:
            chunks_to_unload.append(chunk_idx)
    
    for chunk_idx in chunks_to_unload:
        if chunk_idx in terrain_chunks:
            del terrain_chunks[chunk_idx]
        if chunk_idx in water_chunks:
            del water_chunks[chunk_idx]
