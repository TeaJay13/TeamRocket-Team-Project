# Start_home.py

import pygame
import sys
import time

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
BLUE = (0, 0, 255)
BRIGHT_BLUE = (0, 0, 200)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Start Page")

# Fonts
font_large = pygame.font.SysFont(None, 75)
font_small = pygame.font.SysFont(None, 50)

# Background state (default to the first background)
background_state = 0  # 0 for background.png, 1 for background2.png

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



def choose_background(state):
    global background_state, game_active, background_chosen
    background_state = state
    game_active = True  # Start the game after background selection
    background_chosen = True

# Quit game function
def quit_game():
    pygame.quit()
    sys.exit()

# Function to show the background selection page
# def background_selection_page():
#     global choose_background, game_active, background_chosen
#     background_chosen = False
#     pygame.time.wait(900) 

#     while not background_chosen:
#         screen.fill(WHITE)
        
        
#     # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 quit_game()


#         # Title
#         render_text("Choose Your Background", font_large, BLACK, (150, 100))

#         # Draw buttons for background choices
#         draw_button("Forest", 300, 250, 200, 50, GREEN, BRIGHT_GREEN, lambda: choose_background(0))
#         draw_button("Swamp", 300, 350, 200, 50, BLUE, BRIGHT_BLUE, lambda: choose_background(1))

#         pygame.display.update()



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

        # Draw buttons for background choices
        draw_button("Prairie", 300, 250, 200, 50, GREEN, BRIGHT_GREEN, lambda: choose_background(0))
        draw_button("Swamp", 300, 350, 200, 50, BLUE, BRIGHT_BLUE, lambda: choose_background(1))


        # draw_button("Start", 300, 250, 200, 50, GREEN, BRIGHT_GREEN, background_selection_page)
        draw_button("Quit", 300, 450, 200, 50, RED, BRIGHT_RED, quit_game)



        pygame.display.update()

        # Exit the loop if a background is chosen to start the game
        if game_active:
            background_chosen = True