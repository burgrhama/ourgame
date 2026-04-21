import sys
sys.path.insert(0, '.')

with open('main.py', 'r') as f:
    content = f.read()

# Fix 1: Remove crafting table from collision exclusion
old1 = 'if block.get("type") == "water" or block.get("type") == "crafting_table":'
new1 = 'if block.get("type") == "water":'
content = content.replace(old1, new1)
print(f"Fix 1 - Crafting table collision: {old1 in content} -> Applied")

# Fix 2: Increase step-up height for 2-block gaps
old2 = 'for step_up in range(4, TILE_SIZE + 1, 4):'
new2 = 'for step_up in range(4, int(TILE_SIZE * 1.8), 4):'
if old2 in content:
    content = content.replace(old2, new2)
    print(f"Fix 2 - Step-up height: Applied")
else:
    print(f"Fix 2 - Step-up height: Already fixed or not found")

with open('main.py', 'w') as f:
    f.write(content)

print("\nAll fixes applied!")
print("Ready to play - run: python main.py")
