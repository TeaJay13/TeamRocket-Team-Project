# Start_home.py

import pygame
import sys

# Initialize pygame
pygame.init()

# Constants for screen size and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Start Page")

# Fonts
font_large = pygame.font.SysFont(None, 75)
font_small = pygame.font.SysFont(None, 50)

# Function to render text
def render_text(text, font, color, position):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

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
    
    render_text(msg, font_small, WHITE, (x + 20, y + 10))

# Start game function (this will set the game state to active)
def start_game():
    global game_active
    game_active = True

# Quit game function
def quit_game():
    pygame.quit()
    sys.exit()

# Main loop for start page
def start_page():
    global game_active
    game_active = False  # Reset game state to not active
    
    while not game_active:
        screen.fill(WHITE)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        # Title
        render_text("Welcome to the Game", font_large, BLACK, (150, 100))

        # Draw buttons
        draw_button("Start", 300, 250, 200, 50, GREEN, BRIGHT_GREEN, start_game)
        draw_button("Quit", 300, 350, 200, 50, RED, BRIGHT_RED, quit_game)
        
        pygame.display.update()
