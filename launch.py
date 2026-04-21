#!/usr/bin/env python3
"""
Quick launcher to debug the game issue
"""
import sys
import os

# Add current dir to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    import pygame
    pygame.init()
    print("Pygame initialized")
    
    # Try importing main
    import main
    print("Main imported successfully")
    
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
