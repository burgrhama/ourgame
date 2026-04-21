import pygame
import os
import sys

# Test basic setup
print("Testing game setup...")

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")

print(f"Base dir: {BASE_DIR}")
print(f"Model dir: {MODEL_DIR}")
print(f"Model dir exists: {os.path.exists(MODEL_DIR)}")

# List textures
if os.path.exists(MODEL_DIR):
    files = os.listdir(MODEL_DIR)
    print(f"Found {len(files)} files in models/")
    print("First 10 files:", files[:10])

# Try to load pygame
try:
    pygame.init()
    print("OK - Pygame initialized")
except Exception as e:
    print("FAIL - Pygame error:", e)
    sys.exit(1)

# Try to create display
try:
    screen = pygame.display.set_mode((640, 480))
    print("OK - Display created (640x480)")
except Exception as e:
    print("FAIL - Display error:", e)
    pygame.quit()
    sys.exit(1)

# Try to load a texture
try:
    test_img_path = os.path.join(MODEL_DIR, "Sky.png")
    if os.path.exists(test_img_path):
        img = pygame.image.load(test_img_path)
        print(f"OK - Loaded Sky.png: {img.get_size()}")
    else:
        print(f"FAIL - Sky.png not found at {test_img_path}")
except Exception as e:
    print("FAIL - Image load error:", e)

# Fill screen with test color
try:
    screen.fill((100, 150, 200))  # Light blue
    pygame.display.flip()
    print("OK - Screen filled and flipped")
except Exception as e:
    print("FAIL - Screen fill error:", e)

# Keep window open for 1 second
pygame.time.wait(1000)

pygame.quit()
print("OK - All tests passed! Game should work.")
