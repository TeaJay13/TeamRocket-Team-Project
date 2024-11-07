import pygame
import sys
# import Start_home  # Import start page
# import game  # Import main game

# Initialize Pygame
pygame.init()

# Constants for screen size and colors
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Over")

# Fonts
font_large = pygame.font.SysFont(None, 75)
font_small = pygame.font.SysFont(None, 50)

# Button function
def draw_button(msg, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))
    
    text_surface = font_small.render(msg, True, WHITE)
    screen.blit(text_surface, (x + (w - text_surface.get_width()) // 2, y + (h - text_surface.get_height()) // 2))

# Actions for buttons
def play_again():
    print("Play Again clicked")  # Placeholder action for testing
    # game.game_loop()  # Restart the main game loop

def go_to_start_menu():
    print("Go to Start Menu clicked")  # Placeholder action for testing
    # Start_home.start_page()  # Go back to start page

# Main loop for end screen
def end_screen():
    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Display "Game Over" message
        text_surface = font_large.render("Game Over", True, BLACK)
        screen.blit(text_surface, ((WIDTH - text_surface.get_width()) // 2, 100))

        # Draw buttons
        draw_button("Play Again", 225, 300, 350, 50, GREEN, BRIGHT_GREEN, play_again)
        draw_button("Go to Start Menu", 225, 400, 350, 50, RED, BRIGHT_RED, go_to_start_menu)

        pygame.display.flip()

# Run end screen if this file is executed directly
if __name__ == "__main__":
    end_screen()