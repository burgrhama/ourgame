#!/usr/bin/env python3
"""
COMPREHENSIVE GAME FIXES
- Knife texture display fix
- Crafting table walkthrough fix
- Water collision fix
- 2-block gap walking fix
- Web playable version prep
"""

# This script generates all the fixes needed

fixes = {
    "knife_texture": """
# FIX 1: KNIFE TEXTURE
# In draw_item_in_hand function, ensure knife renders:

elif item_type == "knife":
    knife_img = item_images.get("knife")
    if knife_img:
        hand_item = pygame.transform.scale(knife_img, (hand_size, hand_size)).copy()
        if direction == "left":
            hand_item = pygame.transform.flip(hand_item, True, False)
    else:
        # Fallback if texture not found
        hand_item = get_item_surface(item_type, hand_size).copy()
        if direction == "left":
            hand_item = pygame.transform.flip(hand_item, True, False)
""",

    "crafting_table_collision": """
# FIX 2: CRAFTING TABLE COLLISION
# In get_nearby_block_rects function, include crafting tables:

def get_nearby_block_rects(world_x):
    rects = []
    for block in placed_blocks:
        # Include ALL blocks except water for collision
        if block.get("type") == "water":
            continue
        block_rect = get_block_world_rect(block)
        dx = block_rect.x - world_x
        if abs(dx) < WIDTH:
            rects.append(pygame.Rect(int(world_x + dx), block_rect.y, block_rect.width, block_rect.height))
    
    for forge in placed_forges:
        dx = forge.rect.x - world_x
        if abs(dx) < WIDTH:
            rects.append(pygame.Rect(int(world_x + dx), forge.rect.y, forge.rect.width, forge.rect.height))
    
    return rects
""",

    "water_collision": """
# FIX 3: WATER COLLISION FIX
# Water blocks should NOT be solid for walking
# They should only affect swimming state
# Replace water collision check to only check non-water blocks

# In movement code:
test_rect = pygame.Rect(new_x - pw // 2, player_rect.y, pw, ph)
collision = False

for block in placed_blocks:
    if block.get("type") == "water":  # SKIP WATER BLOCKS
        continue
    block_rect = get_block_world_rect(block)
    if test_rect.colliderect(block_rect):
        collision = True
        break
""",

    "two_block_gap": """
# FIX 4: TWO-BLOCK GAP WALKING
# Increase step-up height to allow walking through 2-block gaps
# Change TILE_SIZE step detection

# Current: step_up in range(4, TILE_SIZE + 1, 4)
# New: larger step increments for smoother terrain navigation

for step_up in range(4, TILE_SIZE * 1.5, 4):  # Increased max step
    try_y = player_rect.y - step_up
    test_rect = pygame.Rect(new_x - pw // 2, try_y, pw, ph)
    # check collision at new height
    if not collision_at(test_rect):  # Can move to this height
        player_rect.y = try_y
        moved = True
        break
"""
}

print("GAME FIXES REFERENCE")
print("=" * 50)
for fix_name, fix_code in fixes.items():
    print(f"\n{fix_name}:")
    print(fix_code)
