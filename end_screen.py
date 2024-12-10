import pygame
import sys
import sqlite3
from scoring import get_final_score


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

# Database connection
DB_PATH = "game_scores.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Ensure the scores table exists (does not recreate it unnecessarily)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        name TEXT,
        score INTEGER
    )
""")
conn.commit()

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
    restartGame = True
    sys.exit()  # Exit the end screen to allow the game to restart

def quit_game():
    print("Exiting the game...")
    pygame.quit()
    sys.exit()

def save_score(name, score):
    cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()

# Screen to input name
def input_name_screen(score):
    name = ""
    cursor_visible = True
    cursor_timer = 0
    cursor_blink_speed = 500  # Blinking speed in milliseconds
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    save_score(name, score)
                    end_screen(score)
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 15:  # Limit the name length to 15 characters
                        name += event.unicode

        # Cursor blinking logic
        cursor_timer += clock.get_time()
        if cursor_timer >= cursor_blink_speed:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        # Display input prompt
        prompt_surface = font_large.render("Enter Your Name:", True, BLACK)
        screen.blit(prompt_surface, ((WIDTH - prompt_surface.get_width()) // 2, 150))

        # Draw input box
        input_box_x = (WIDTH - 400) // 2
        input_box_y = 250
        input_box_width = 400
        input_box_height = 50
        pygame.draw.rect(screen, BLACK, (input_box_x, input_box_y, input_box_width, input_box_height), 2)

        # Display entered name inside the input box
        name_surface = font_large.render(name, True, BLACK)
        screen.blit(name_surface, (input_box_x + 10, input_box_y + (input_box_height - name_surface.get_height()) // 2))

        # Draw cursor
        if cursor_visible:
            cursor_x = input_box_x + 10 + name_surface.get_width() + 5
            cursor_y = input_box_y + 10
            cursor_height = input_box_height - 20
            pygame.draw.line(screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

        pygame.display.flip()
        clock.tick(60)

# Display top 10 scores
def display_top_scores():
    cursor.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 10")
    scores = cursor.fetchall()

    y_offset = 200
    for idx, (name, score) in enumerate(scores):
        score_text = f"{idx + 1}. {name}: {score}"
        score_surface = font_small.render(score_text, True, BLACK)
        screen.blit(score_surface, (WIDTH // 2 - 200, y_offset))
        y_offset += 40

# Main loop for end screen
def end_screen(final_score):
    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Display "Game Over" message
        text_surface = font_large.render("Game Over", True, BLACK)
        screen.blit(text_surface, ((WIDTH - text_surface.get_width()) // 2, 50))

        # Display final score
        score_surface = font_large.render(f"Your Score: {final_score}", True, BLACK)
        screen.blit(score_surface, ((WIDTH - score_surface.get_width()) // 2, 120))

        # Display top scores
        display_top_scores()

        # Draw buttons
        draw_button("Play Again", 225, 450, 350, 50, GREEN, BRIGHT_GREEN, play_again)
        draw_button("Quit", 225, 520, 350, 50, RED, BRIGHT_RED, quit_game)

        pygame.display.flip()

# Run the name input screen if this file is executed directly
if __name__ == "__main__":
    final_score = get_final_score()  # Retrieve the final score from scoring.py
    input_name_screen(final_score)
