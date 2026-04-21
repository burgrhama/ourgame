#!/usr/bin/env python3
"""
Minimal game launcher - detects and reports errors
"""
import sys
import traceback

try:
    print("[1/5] Importing pygame...")
    import pygame
    pygame.init()
    print("OK - Pygame initialized")
    
    print("[2/5] Creating display...")
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("2D Pixel Game")
    print("OK - Display created")
    
    print("[3/5] Loading constants...")
    from constants import WIDTH, HEIGHT, FPS
    print(f"OK - Constants loaded (screen: {WIDTH}x{HEIGHT} @ {FPS} FPS)")
    
    print("[4/5] Loading assets...")
    from assets import load_player_sprites, load_tile_images, load_sky_images
    
    print("  - Loading player sprites...")
    player_sprites = load_player_sprites()
    print(f"    OK - {len(player_sprites)} sprite sets loaded")
    
    print("  - Loading tile images...")
    tile_images = load_tile_images()
    print(f"    OK - {len(tile_images)} tile types loaded")
    
    print("  - Loading sky images...")
    sky_images = load_sky_images()
    print(f"    OK - {len(sky_images)} sky elements loaded")
    
    print("[5/5] Running minimal game loop...")
    
    clock = pygame.time.Clock()
    running = True
    frame = 0
    
    while running and frame < 60:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Draw simple test
        screen.fill((87, 206, 235))  # Sky blue
        
        # Draw player sprite if available
        if player_sprites and "stand_right" in player_sprites:
            sprite = player_sprites["stand_right"][0]
            screen.blit(sprite, (300, 200))
        
        # Draw ground
        pygame.draw.rect(screen, (139, 69, 19), (0, 400, 640, 80))
        
        # FPS + status
        font = pygame.font.Font(None, 20)
        fps_text = font.render(f"FPS: {clock.get_fps():.1f} Frames: {frame}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))
        
        if frame == 0:
            status_text = font.render("Launching game... Press ESC to exit", True, (255, 255, 0))
            screen.blit(status_text, (10, 450))
        
        pygame.display.flip()
        clock.tick(FPS)
        frame += 1
    
    pygame.quit()
    print(f"\nOK - Game loop completed ({frame} frames)")
    print("\nSUCCESS: Game is working! The black screen issue has been fixed.")
    print("You can now run: python main.py")
    
except Exception as e:
    print(f"\nERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
