# inventory.py - Inventory, crafting, and item management
from constants import *


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
        "pattern": ["P", "P"],
        "key": {"P": "planks"},
        "output": {"sticks": 4},
        "mirror": False,
    },
    {
        "name": "crafting_table",
        "type": "shaped",
        "pattern": ["PP", "PP"],
        "key": {"P": "planks"},
        "output": {"crafting_table": 1},
        "mirror": False,
    },
    {
        "name": "forge",
        "type": "shaped",
        "pattern": [" P ", "P P", "P P"],
        "key": {"P": "stone"},
        "output": {"forge": 1},
        "mirror": False,
    },
    {
        "name": "axe",
        "type": "shaped",
        "pattern": ["PP ", "PS ", " S "],
        "key": {"P": "planks", "S": "sticks"},
        "output": {"axe": 1},
        "mirror": True,
    },
    {
        "name": "knife",
        "type": "shaped",
        "pattern": ["P", "P", "S"],
        "key": {"P": "planks", "S": "sticks"},
        "output": {"knife": 1},
        "mirror": False,
    },
    {
        "name": "pickaxe",
        "type": "shaped",
        "pattern": ["PPP", " S ", " S "],
        "key": {"P": "planks", "S": "sticks"},
        "output": {"pickaxe": 1},
        "mirror": False,
    },
]

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

PLACEABLE_ITEMS = {
    "wood", "leaves", "planks", "crafting_table", "forge", "stone",
    "jord", "grass", "sand", "limestone", "copper_ore", "iron_ore",
    "gold_ore", "ruby", "bedrock",
}


def create_inventory():
    """Create new inventory."""
    return {
        "wood": 0, "leaves": 0, "planks": 0, "sticks": 0, "axe": 0,
        "crafting_table": 0, "forge": 0, "grass": 0, "jord": 0, "stone": 0,
        "sand": 0, "limestone": 0, "copper_ore": 0, "iron_ore": 0,
        "gold_ore": 0, "ruby": 0, "knife": 0, "pickaxe": 0,
    }


def get_hotbar_items(inventory):
    """Generate hotbar items based on inventory."""
    hotbar_items = [None] * HOTBAR_SLOTS
    slot_index = 0
    for item in AVAILABLE_HOTBAR_ITEMS:
        if inventory.get(item["type"], 0) > 0 and slot_index < HOTBAR_SLOTS:
            hotbar_items[slot_index] = item
            slot_index += 1
    return hotbar_items


def use_tool(tool_type, tool_durability, inventory):
    """Use tool and reduce durability."""
    if tool_type not in TOOL_DURABILITY:
        return True
    durability = tool_durability.get(tool_type, TOOL_DURABILITY[tool_type])
    durability -= 1
    if durability <= 0:
        inventory[tool_type] = max(0, inventory.get(tool_type, 0) - 1)
        if tool_type in tool_durability:
            del tool_durability[tool_type]
        return False
    tool_durability[tool_type] = durability
    return True


def get_smelt_recipe(item_type):
    """Get smelting recipe for item."""
    return SMELT_RECIPES.get(item_type)


def get_fuel_recipe(item_type):
    """Get fuel recipe for item."""
    return FUEL_RECIPES.get(item_type)


def get_slot_item_data(slot_item):
    """Extract item type and count from slot."""
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


def build_crafting_grid_data(crafting_grid):
    """Build types and counts from crafting grid."""
    grid_types = [[None for _ in range(CRAFTING_LARGE_COLS)] for _ in range(CRAFTING_LARGE_ROWS)]
    grid_counts = [[0 for _ in range(CRAFTING_LARGE_COLS)] for _ in range(CRAFTING_LARGE_ROWS)]
    for r in range(CRAFTING_LARGE_ROWS):
        for c in range(CRAFTING_LARGE_COLS):
            item_type, item_count = get_slot_item_data(crafting_grid[r][c])
            grid_types[r][c] = item_type
            grid_counts[r][c] = item_count
    return grid_types, grid_counts


def match_shapeless_recipe(recipe, grid_types, grid_counts, active_rows, active_cols):
    """Match shapeless recipe."""
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


def match_shaped_recipe(recipe, grid_types, grid_counts, active_rows, active_cols):
    """Match shaped recipe."""
    patterns = [recipe["pattern"]]
    if recipe.get("mirror"):
        mirrored = [row[::-1] for row in recipe["pattern"]]
        if mirrored != recipe["pattern"]:
            patterns.append(mirrored)
    
    for pattern in patterns:
        pat_rows = len(pattern)
        pat_cols = len(pattern[0]) if pat_rows else 0
        if pat_rows == 0 or pat_cols == 0 or pat_rows > active_rows or pat_cols > active_cols:
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


def get_crafting_recipe(crafting_grid, active_rows, active_cols):
    """Find matching recipe in crafting grid."""
    grid_types, grid_counts = build_crafting_grid_data(crafting_grid)
    
    for recipe in CRAFTING_RECIPES:
        if recipe["type"] == "shapeless":
            result = match_shapeless_recipe(recipe, grid_types, grid_counts, active_rows, active_cols)
        else:
            result = match_shaped_recipe(recipe, grid_types, grid_counts, active_rows, active_cols)
        if result:
            return result
    
    return None, None, None


def craft_item(crafting_grid, recipe_name, output_items, consume_plan, inventory):
    """Perform crafting."""
    if not recipe_name or not output_items or not consume_plan:
        return False
    
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
    
    for item, count in output_items.items():
        inventory[item] = inventory.get(item, 0) + count
    
    return True


def get_inventory_items_list(inventory):
    """Get list of items in inventory."""
    all_items = []
    for item_type in inventory.keys():
        if inventory[item_type] > 0:
            all_items.append({"type": item_type, "count": inventory[item_type]})
    return all_items


def set_crafting_mode(crafting_grid, use_table, inventory):
    """Switch crafting grid size."""
    active_rows = CRAFTING_LARGE_ROWS if use_table else CRAFTING_SMALL_ROWS
    active_cols = CRAFTING_LARGE_COLS if use_table else CRAFTING_SMALL_COLS
    
    for row in range(CRAFTING_LARGE_ROWS):
        for col in range(CRAFTING_LARGE_COLS):
            if row < active_rows and col < active_cols:
                continue
            item = crafting_grid[row][col]
            if not item:
                continue
            item_type, item_count = get_slot_item_data(item)
            if item_type and item_count > 0:
                inventory[item_type] = inventory.get(item_type, 0) + item_count
            crafting_grid[row][col] = None
