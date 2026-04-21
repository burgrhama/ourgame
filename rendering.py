# rendering.py - All UI and drawing functions
import pygame
import math
from constants import *
from assets import get_item_surface


def draw_sky(surface, camera_x, camera_y, sky_images):
    """Draw sky background."""
    if sky_images.get("sky"):
        sky_img = pygame.transform.scale(sky_images["sky"], (TILE_SIZE, TILE_SIZE))
        start_x = int(-(camera_x % TILE_SIZE) - TILE_SIZE)
        start_y = int(-(camera_y % TILE_SIZE) - TILE_SIZE)
        for y in range(start_y, HEIGHT + TILE_SIZE, TILE_SIZE):
            for x in range(start_x, WIDTH + TILE_SIZE, TILE_SIZE):
                surface.blit(sky_img, (x, y))


def draw_grid(surface, camera_x, camera_y, cell_size=32, color=(50, 50, 50)):
    """Draw debug grid."""
    start_x = int(-(camera_x % cell_size))
    start_y = int(-(camera_y % cell_size))
    for x in range(start_x, WIDTH + cell_size, cell_size):
        pygame.draw.line(surface, color, (x, 0), (x, HEIGHT))
    for y in range(start_y, HEIGHT + cell_size, cell_size):
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))


def draw_ground(surface, camera_x, camera_y, tile_images, get_terrain_tile_func):
    """Draw all terrain tiles."""
    start_tile_x = int(camera_x // TILE_SIZE) - 1
    end_tile_x = int((camera_x + WIDTH) // TILE_SIZE) + 1
    start_tile_y = int(camera_y // TILE_SIZE) - 1
    end_tile_y = int((camera_y + HEIGHT) // TILE_SIZE) + 1
    
    for tile_x in range(start_tile_x, end_tile_x + 1):
        for tile_y in range(start_tile_y, end_tile_y + 1):
            tile_key = get_terrain_tile_func(tile_x, tile_y)
            if not tile_key:
                continue
            draw_x = tile_x * TILE_SIZE - camera_x
            draw_y = tile_y * TILE_SIZE - camera_y
            surface.blit(tile_images[tile_key], (draw_x, draw_y))


def draw_placed_blocks(surface, camera_x, camera_y, placed_blocks, placed_forges, forge_images, get_item_surface_func, get_block_dimensions_func, get_block_world_rect_func):
    """Draw all placed blocks and forges."""
    # Draw crafting tables first
    for block in placed_blocks:
        if block.get("type") != "crafting_table":
            continue
        block_rect = get_block_world_rect_func(block)
        draw_x = block_rect.x - camera_x
        draw_y = block_rect.y - camera_y + CRAFTING_TABLE_GROUND_SINK_PX
        if draw_x < -block_rect.width or draw_x > WIDTH or draw_y < -block_rect.height or draw_y > HEIGHT:
            continue
        item_surface = get_item_surface_func(block["type"], max(block_rect.width, block_rect.height))
        if item_surface.get_width() != block_rect.width or item_surface.get_height() != block_rect.height:
            item_surface = pygame.transform.scale(item_surface, (block_rect.width, block_rect.height))
        surface.blit(item_surface, (draw_x, draw_y))
    
    # Draw other blocks
    for block in placed_blocks:
        if block.get("type") == "crafting_table":
            continue
        block_rect = get_block_world_rect_func(block)
        draw_x = block_rect.x - camera_x
        draw_y = block_rect.y - camera_y
        if draw_x < -block_rect.width or draw_x > WIDTH or draw_y < -block_rect.height or draw_y > HEIGHT:
            continue
        
        if block["type"] == "water":
            has_water_above = any(b["type"] == "water" and b["x"] == block["x"] and b["y"] == block["y"] - TILE_SIZE for b in placed_blocks)
            water_type = "water_top" if not has_water_above else "water_bottom"
            item_surface = get_item_surface_func(water_type, max(block_rect.width, block_rect.height))
        else:
            item_surface = get_item_surface_func(block["type"], max(block_rect.width, block_rect.height))
        
        if item_surface.get_width() != block_rect.width or item_surface.get_height() != block_rect.height:
            item_surface = pygame.transform.scale(item_surface, (block_rect.width, block_rect.height))
        surface.blit(item_surface, (draw_x, draw_y))
    
    # Draw forges
    for forge in placed_forges:
        draw_x = forge.rect.x - camera_x
        draw_y = forge.rect.y - camera_y + CRAFTING_TABLE_GROUND_SINK_PX
        if draw_x < -forge.rect.width or draw_x > WIDTH or draw_y < -forge.rect.height or draw_y > HEIGHT:
            continue
        
        if forge.is_smelting and forge.fuel_remaining_ms > 0:
            frame_key = "fire_bobing" if (pygame.time.get_ticks() // 300) % 2 else "fire"
            forge_img = forge_images.get(frame_key)
        else:
            frame_key = "idle_bobing" if (pygame.time.get_ticks() // 500) % 2 else "idle"
            forge_img = forge_images.get(frame_key)
        
        if forge_img:
            scaled_img = pygame.transform.scale(forge_img, (forge.rect.width, forge.rect.height))
            surface.blit(scaled_img, (draw_x, draw_y))


def draw_item_in_hand(surface, player_x, player_y, direction, hotbar_selected, hotbar_items, inventory, item_images, get_item_surface_func):
    """Draw item held in player's hand."""
    if hotbar_selected < 0 or hotbar_selected >= len(hotbar_items):
        return
    
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
            hand_item = get_item_surface_func(item_type, hand_size).copy()
            if direction == "left":
                hand_item = pygame.transform.flip(hand_item, True, False)
    elif item_type == "knife":
        knife_img = item_images.get("knife")
        if knife_img:
            hand_item = pygame.transform.scale(knife_img, (hand_size, hand_size)).copy()
            if direction == "left":
                hand_item = pygame.transform.flip(hand_item, True, False)
        else:
            hand_item = get_item_surface_func(item_type, hand_size).copy()
            if direction == "left":
                hand_item = pygame.transform.flip(hand_item, True, False)
    else:
        hand_item = get_item_surface_func(item_type, hand_size).copy()
        if direction == "left":
            hand_item = pygame.transform.flip(hand_item, True, False)
    
    hand_x = player_x - 6 if direction == "left" else player_x + 34
    hand_y = player_y + 20
    surface.blit(hand_item, (hand_x, hand_y))


def draw_hotbar(surface, hotbar_items, inventory, get_item_surface_func, hotbar_selected):
    """Draw hotbar at bottom of screen."""
    hotbar_start_x = (WIDTH - HOTBAR_SLOTS * HOTBAR_SLOT_SIZE) // 2
    for i in range(HOTBAR_SLOTS):
        slot_x = hotbar_start_x + i * HOTBAR_SLOT_SIZE
        slot_rect = pygame.Rect(slot_x, HOTBAR_Y, HOTBAR_SLOT_SIZE, HOTBAR_SLOT_SIZE)
        
        if i == hotbar_selected:
            pygame.draw.rect(surface, (255, 200, 0), slot_rect, 3)
        else:
            pygame.draw.rect(surface, (100, 100, 100), slot_rect)
        pygame.draw.rect(surface, (255, 255, 255), slot_rect, 1)
        
        if hotbar_items[i]:
            item = hotbar_items[i]
            item_count = inventory.get(item["type"], 0)
            item_surface = get_item_surface_func(item["type"], HOTBAR_SLOT_SIZE - 6)
            surface.blit(item_surface, (slot_x + 3, HOTBAR_Y + 3))
            
            small_font = pygame.font.Font(None, 12)
            count_text = small_font.render(str(item_count), True, (255, 255, 255))
            count_rect = count_text.get_rect(bottomright=(slot_rect.right - 2, slot_rect.bottom - 2))
            surface.blit(count_text, count_rect)


def draw_health_hud(surface, player_health):
    """Draw health bar."""
    pygame.draw.rect(surface, (25, 25, 25), (10, 10, 164, 18))
    pygame.draw.rect(surface, (255, 255, 255), (10, 10, 164, 18), 1)
    fill_w = int((player_health / PLAYER_MAX_HEALTH) * 160)
    pygame.draw.rect(surface, (210, 40, 40), (12, 12, fill_w, 14))
    info_font = pygame.font.Font(None, 20)
    hp_text = info_font.render(f"HP {player_health}/{PLAYER_MAX_HEALTH}", True, (255, 255, 255))
    surface.blit(hp_text, (12, 31))


def draw_damage_effect(surface, current_time, player_damage_flash_until):
    """Draw red damage flash overlay."""
    if current_time < player_damage_flash_until:
        remaining = player_damage_flash_until - current_time
        alpha = max(0, min(140, int(140 * (remaining / PLAYER_DAMAGE_FLASH_MS))))
        damage_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        damage_overlay.fill((200, 20, 20, alpha))
        surface.blit(damage_overlay, (0, 0))


def draw_death_screen(surface, current_time, player_death_message_until):
    """Draw death message."""
    if current_time < player_death_message_until:
        death_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        death_overlay.fill((12, 0, 0, 180))
        surface.blit(death_overlay, (0, 0))
        
        panel_rect = pygame.Rect(WIDTH // 2 - 220, HEIGHT // 2 - 90, 440, 180)
        pygame.draw.rect(surface, (20, 0, 0), panel_rect)
        pygame.draw.rect(surface, (170, 20, 20), panel_rect, 3)
        pygame.draw.line(surface, (110, 10, 10), (panel_rect.left, panel_rect.centery), (panel_rect.right, panel_rect.centery), 1)
        
        death_title_font = pygame.font.Font(None, 84)
        death_title = death_title_font.render("YOU DIED", True, (255, 70, 70))
        death_title_rect = death_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 26))
        surface.blit(death_title, death_title_rect)
        
        death_sub_font = pygame.font.Font(None, 28)
        death_sub = death_sub_font.render("Respawning...", True, (230, 180, 180))
        death_sub_rect = death_sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 34))
        surface.blit(death_sub, death_sub_rect)


def draw_placement_preview(surface, camera_x, camera_y, hotbar_items, hotbar_selected, inventory, placing_item_in_world, mouse_x, mouse_y, get_item_surface_func, get_block_dimensions_func, get_player_world_rect_func, get_nearby_occupied_rects_func):
    """Draw block placement preview."""
    if not placing_item_in_world:
        return
    
    info_font = pygame.font.Font(None, 20)
    placement_text = info_font.render(f"Placing: {placing_item_in_world.upper()} (right-click) - Left-click to remove", True, (100, 255, 100))
    surface.blit(placement_text, (10, 70))
    
    world_mouse_x = mouse_x + camera_x
    world_mouse_y = mouse_y + camera_y
    grid_world_x = int(world_mouse_x // TILE_SIZE) * TILE_SIZE
    grid_world_y = int(world_mouse_y // TILE_SIZE) * TILE_SIZE
    grid_screen_x = grid_world_x - camera_x
    grid_screen_y = grid_world_y - camera_y
    preview_width, preview_height = get_block_dimensions_func(placing_item_in_world)
    preview_rect = pygame.Rect(grid_world_x, grid_world_y, preview_width, preview_height)
    
    collides_existing = any(
        r.colliderect(preview_rect)
        for r in get_nearby_occupied_rects_func(preview_rect.centerx, preview_rect.centery, 8, 8, 10)
    )
    can_place_here = not preview_rect.colliderect(get_player_world_rect_func()) and not collides_existing
    
    if can_place_here:
        preview_surf = get_item_surface_func(placing_item_in_world, max(preview_width, preview_height)).copy()
        if preview_surf.get_width() != preview_width or preview_surf.get_height() != preview_height:
            preview_surf = pygame.transform.scale(preview_surf, (preview_width, preview_height))
        preview_surf.set_alpha(160)
        surface.blit(preview_surf, (grid_screen_x, grid_screen_y))
        pygame.draw.rect(surface, (255, 255, 255), (grid_screen_x, grid_screen_y, preview_width, preview_height), 1)


def draw_debug_info(surface, show_info, fps, player_world_x, player_rect_y, biome_name):
    """Draw debug information."""
    if show_info:
        info_font = pygame.font.Font(None, 20)
        fps_text = info_font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
        coord_text = info_font.render(f"X: {int(player_world_x)}, Y: {int(player_rect_y)}", True, (255, 255, 255))
        biome_text = info_font.render(f"Biome: {biome_name}", True, (255, 255, 255))
        surface.blit(fps_text, (10, 10))
        surface.blit(coord_text, (10, 30))
        surface.blit(biome_text, (10, 50))


def draw_dropped_items(surface, dropped_items, camera_x, camera_y, current_time, get_item_surface_func):
    """Draw dropped items in world."""
    for drop in dropped_items:
        draw_x = int(drop["x"] - camera_x)
        bob_y = int(math.sin((current_time + int(drop["x"])) * 0.008) * 2)
        draw_y = int(drop["y"] - camera_y + bob_y)
        if draw_x < -20 or draw_x > WIDTH + 20 or draw_y < -20 or draw_y > HEIGHT + 20:
            continue
        icon = get_item_surface_func(drop["type"], 18)
        surface.blit(icon, (draw_x - 9, draw_y - 9))
        
        count_text = pygame.font.Font(None, 14).render(str(drop["count"]), True, (255, 255, 255))
        surface.blit(count_text, (draw_x + 4, draw_y + 2))
