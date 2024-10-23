import pygame
import sys
import Start_home

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)

player_texture = pygame.image.load("TeamRocket-Team-Project/textures/pngegg.png")
player_texture_size = player_texture.get_size()

WHITE = (255, 255, 255)



player_x = 100
player_y = 150
player_width = player_texture_size[0]
player_height = player_texture_size[1]
player_gravity = 0
is_jumping = False  # To track if the rectangle is in a jump

clock = pygame.time.Clock()

# Main game loop
def game_loop():
    global player_x, player_y, player_gravity, is_jumping
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Create the rectangles
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        platform = pygame.Rect(200, 450, 500, 5)

        # Move the texture
        if keys[pygame.K_LEFT]:
            player_x -= 5
            player_rect.x = player_x
            if player_rect.colliderect(platform):
                player_x += 5

        if keys[pygame.K_RIGHT]:
            player_x += 5
            player_rect.x = player_x
            if player_rect.colliderect(platform):
                player_x -= 5

        if keys[pygame.K_SPACE] and not is_jumping:  # Jump only when not already jumping
            player_gravity = -20  # Negative gravity for upward jump
            is_jumping = True

        player_gravity += 1  # Simulate gravity (increases over time)
        player_y += player_gravity
        player_rect.y = player_y

        # Check for collisions with platform (coming from above)
        if player_rect.colliderect(platform) and player_gravity > 0:
            player_y = platform.y - player_height  # Position the texture on top of the platform
            player_gravity = 0  # Stop gravity
            is_jumping = False  # Allow jumping again

        # Prevent the texture from falling off the bottom of the screen
        if player_y >= window_size[1] - player_height:
            player_y = window_size[1] - player_height
            player_gravity = 0
            is_jumping = False

        # Fill the screen and draw the texture and platform
        screen.fill((0, 0, 0))
        screen.blit(player_texture, (player_x, player_y))  # Draw the texture instead of the rectangle
        pygame.draw.rect(screen, WHITE, platform)

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Run the start page and then the game
Start_home.start_page()
if Start_home.game_active:
    game_loop()