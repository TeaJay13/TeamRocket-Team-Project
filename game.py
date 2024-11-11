import pygame
import sys
import Start_home

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

background = pygame.image.load("TeamRocket-Team-Project/graphics/bacground.PNG")
platform_texture = pygame.image.load("TeamRocket-Team-Project/graphics/platform00.png")

WHITE = (255, 255, 255)

player_x = 100
player_y = 150
player_width = 20
player_height = 20
player_gravity = 0
is_jumping = False  # To track if the player is in a jump

clock = pygame.time.Clock()

# Invisible platform dimensions (for character to walk on at land level)
land_platform_y = screen_height - 45  # Position 45 pixels from the bottom
land = pygame.Rect(0, land_platform_y, screen_width, 5)

platform_x = 450
platform_y = 430
platform_width = platform_texture.get_width()
platform_height = platform_texture.get_height()

# Main game loop
def game_loop():
    global player_x, player_y, player_gravity, is_jumping

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Create the player rectangle
        player = pygame.Rect(player_x, player_y, player_width, player_height)
        
        # Define platform rectangle for collision
        platform = pygame.Rect(platform_x, platform_y, platform_width, platform_height)

        # Move the player
        if keys[pygame.K_a]:
            player_x -= 5
            player.x = player_x
            if player.colliderect(land):
                player_x += 5

        if keys[pygame.K_d]:
            player_x += 5
            player.x = player_x
            if player.colliderect(land):
                player_x -= 5

        # Jump logic
        if keys[pygame.K_SPACE] and not is_jumping:  # Jump only when not already jumping
            player_gravity = -20  # Negative gravity for upward jump
            is_jumping = True

        player_gravity += 1  # Simulate gravity (increases over time)
        player_y += player_gravity
        player.y = player_y

        # Check for collision with land (invisible ground platform)
        if player.colliderect(land) and player_gravity > 0:
            player_y = land.y - player_height  # Align player's bottom to land's top
            player_gravity = 0  # Stop gravity
            is_jumping = False  # Allow jumping again

        # Check for collision with platform
        if player.colliderect(platform) and player_gravity > 0:
            player_y = platform.y - player_height # Align player's bottom to platform's top
            player_gravity = 0  # Stop gravity
            is_jumping = False  # Allow jumping again

        # Prevent the player from falling off the bottom of the screen
        if player_y >= screen_height - player_height:
            player_y = screen_height - player_height
            player_gravity = 0
            is_jumping = False

        # Draw background, player, and platform
        screen.blit(background, (0, 0))  # Position background at the top-left corner
        pygame.draw.rect(screen, WHITE, player)
        screen.blit(platform_texture, (platform_x, platform_y))

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