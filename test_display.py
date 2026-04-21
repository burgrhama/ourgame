#!/usr/bin/env python3
"""
Test if the game window is showing anything
"""
import pygame
import os
from constants import WIDTH, HEIGHT, TILE_SIZE, FPS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Test - Should show colors")

clock = pygame.time.Clock()
running = True
frame = 0

while running and frame < 120:  # Run for ~2 seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Draw test pattern
    if frame < 30:
        # Blue background
        screen.fill((50, 100, 200))
        text_surf = pygame.font.Font(None, 24).render("GAME STARTING - BLUE", True, (255, 255, 255))
        screen.blit(text_surf, (150, 200))
    elif frame < 60:
        # Green background
        screen.fill((50, 200, 100))
        text_surf = pygame.font.Font(None, 24).render("GAME LOADING - GREEN", True, (255, 255, 255))
        screen.blit(text_surf, (150, 200))
    elif frame < 90:
        # Red background
        screen.fill((200, 50, 50))
        text_surf = pygame.font.Font(None, 24).render("GAME READY - RED", True, (255, 255, 255))
        screen.blit(text_surf, (150, 200))
    else:
        # Yellow background
        screen.fill((200, 200, 50))
        text_surf = pygame.font.Font(None, 24).render("GAME RUNNING - YELLOW", True, (0, 0, 0))
        screen.blit(text_surf, (150, 200))
    
    # FPS text
    fps_text = pygame.font.Font(None, 16).render(f"FPS: {clock.get_fps():.0f} Frame: {frame}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(FPS)
    frame += 1

print(f"Test completed. Ran for {frame} frames.")
pygame.quit()
print("If you saw color changes above, your game can render!")
print("The black screen issue is likely in game initialization.")
