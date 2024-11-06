import pygame
import sys
import Start_home

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

background = pygame.image.load("textures/bacground.png")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

player_x = 100
player_y = 150
player_width = 20
player_height = 20
player_gravity = 0
is_jumping = False  # To track if the rectangle is in a jump

clock = pygame.time.Clock()

# Confirmation box function
def confirmation_screen():
    font = pygame.font.Font(None, 36)
    message = font.render("Are you sure you want to go back to home? (Y/N)", True, WHITE)
    rect = message.get_rect(center=(screen_width // 2, screen_height // 2))

    while True:
        screen.fill(BLACK)
        screen.blit(message, rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # If "Y" is pressed, go back to home
                    Start_home.start_page()  # Call the start page function
                    if Start_home.game_active:
                        game_loop()
                elif event.key == pygame.K_n:  # If "N" is pressed, return to game
                    return

# Main game loop
def game_loop():
    global player_x, player_y, player_gravity, is_jumping

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Escape key event to trigger confirmation screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    confirmation_screen()

        keys = pygame.key.get_pressed()

        # Create the rectangles
        player = pygame.Rect(player_x, player_y, player_width, player_height)
        platform = pygame.Rect(200, 450, 500, 5)

        # Move the rectangle
        if keys[pygame.K_LEFT]:
            player_x -= 5
            player.x = player_x
            if player.colliderect(platform):
                player_x += 5

        if keys[pygame.K_RIGHT]:
            player_x += 5
            player.x = player_x
            if player.colliderect(platform):
                player_x -= 5

        if keys[pygame.K_SPACE] and not is_jumping:  # Jump only when not already jumping
            player_gravity = -20  # Negative gravity for upward jump
            is_jumping = True

        player_gravity += 1  # Simulate gravity (increases over time)
        player_y += player_gravity
        player.y = player_y

        # Check for collisions with platform (coming from above)
        if player.colliderect(platform) and player_gravity > 0:
            player_y = platform.y - player_height  # Position the rectangle on top of the platform
            player_gravity = 0  # Stop gravity
            is_jumping = False  # Allow jumping again

        # Prevent the rectangle from falling off the bottom of the screen
        if player_y >= screen_height - player_height:
            player_y = screen_height - player_height
            player_gravity = 0
            is_jumping = False

        # Draw the background image
        screen.blit(background, (0, 0))  # Position background at the top-left corner

        # Draw the player and platform
        pygame.draw.rect(screen, WHITE, player)
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
