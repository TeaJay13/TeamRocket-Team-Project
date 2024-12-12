import pygame
import sys
import sqlite3
from scoring import get_final_score

class EndScreen:
    def __init__(self, db_path="game_scores.db", width=1000, height=700):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game Over")

        # Colors
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "blue": (0, 0, 255),
            "green": (0, 200, 0),
            "bright_green": (0, 255, 0),
            "red": (200, 0, 0),
            "bright_red": (255, 0, 0)
        }

        # Fonts
        self.font_large = pygame.font.SysFont(None, 75)
        self.font_small = pygame.font.SysFont(None, 50)

        # Database setup
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                name TEXT,
                score INTEGER
            )
        """)
        self.conn.commit()

        self.restart_game = False

    def save_score(self, name, score):
        self.cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
        self.conn.commit()

    def draw_button(self, msg, x, y, w, h, inactive_color, active_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        color = active_color if x + w > mouse[0] > x and y + h > mouse[1] > y else inactive_color
        pygame.draw.rect(self.screen, color, (x, y, w, h))

        text_surface = self.font_small.render(msg, True, self.colors["white"])
        self.screen.blit(text_surface, (x + (w - text_surface.get_width()) // 2, y + (h - text_surface.get_height()) // 2))

        if click[0] == 1 and action is not None:
            action()

    def input_name_screen(self, score):
        name = ""
        cursor_visible = True
        cursor_timer = 0
        cursor_blink_speed = 500  # Blinking speed in milliseconds
        clock = pygame.time.Clock()

        while True:
            self.screen.fill(self.colors["white"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name:
                        self.save_score(name, score)
                        return  # Return after saving score
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 15:  # Limit the name length
                        name += event.unicode

            # Cursor blinking
            cursor_timer += clock.get_time()
            if cursor_timer >= cursor_blink_speed:
                cursor_visible = not cursor_visible
                cursor_timer = 0

            # Display input prompt
            prompt_surface = self.font_large.render("Enter Your Name:", True, self.colors["black"])
            self.screen.blit(prompt_surface, ((self.width - prompt_surface.get_width()) // 2, 150))

            # Input box
            input_box = pygame.Rect((self.width - 400) // 2, 250, 400, 50)
            pygame.draw.rect(self.screen, self.colors["black"], input_box, 2)

            name_surface = self.font_large.render(name, True, self.colors["black"])
            self.screen.blit(name_surface, (input_box.x + 10, input_box.y + (input_box.height - name_surface.get_height()) // 2))

            # Cursor
            if cursor_visible:
                cursor_x = input_box.x + 10 + name_surface.get_width() + 5
                cursor_y, cursor_height = input_box.y + 10, input_box.height - 20
                pygame.draw.line(self.screen, self.colors["black"], (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

            pygame.display.flip()
            clock.tick(60)

    def display_top_scores(self):
        self.cursor.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 6")
        scores = self.cursor.fetchall()

        y_offset = 200
        for idx, (name, score) in enumerate(scores):
            score_text = f"{idx + 1}. {name}: {score}"
            score_surface = self.font_small.render(score_text, True, self.colors["black"])
            self.screen.blit(score_surface, (self.width // 2 - 200, y_offset))
            y_offset += 40

    def end_screen(self, final_score):
        self.restart_game = False  # Ensure it's reset each time
        self.input_name_screen(final_score)  # Wait for name input and save score

        def play_again():
            self.restart_game = True

        def quit_game():
            pygame.quit()
            sys.exit()

        while True:
            self.screen.fill(self.colors["white"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

            # Game Over
            text_surface = self.font_large.render("Game Over", True, self.colors["black"])
            self.screen.blit(text_surface, ((self.width - text_surface.get_width()) // 2, 50))

            # Final Score
            score_surface = self.font_large.render(f"Your Score: {final_score}", True, self.colors["black"])
            self.screen.blit(score_surface, ((self.width - score_surface.get_width()) // 2, 120))

            # Top Scores
            self.display_top_scores()

            # Buttons
            self.draw_button("Quit", 325, 480, 350, 50, self.colors["red"], self.colors["bright_red"], quit_game)

            pygame.display.flip()

            if self.restart_game:
                # Restart the game or return to the game loop
                return True  # Or implement game restart logic here
