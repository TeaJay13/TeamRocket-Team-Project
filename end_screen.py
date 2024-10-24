import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 750, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ending Screen")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define fonts
font = pygame.font.SysFont(None, 48)

# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.clicked = False  # Prevents multiple clicks being registered

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Draw hover effect
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
            if click[0] == 1 and not self.clicked and self.action:
                self.action()
                self.clicked = True  # Lock click to avoid multiple triggers
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        if not click[0]:
            self.clicked = False  # Reset click state

        # Render text
        text_surface = font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                  self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

# Define button actions
def play_again():
    print("Play Again")  # Replace this with logic to restart the game

def go_to_start_menu():
    print("Go to Start Menu")  # Replace this with logic to return to the start menu

# Create buttons and center them horizontally
button_width = 350
button_height = 50
button_spacing = 70  # Space between buttons

buttons = [
    Button("Play Again", (WIDTH - button_width) // 2, 150, button_width, button_height, BLUE, GREEN, play_again),
    Button("Go to Start Menu", (WIDTH - button_width) // 2, 150 + button_spacing, button_width, button_height, BLUE, GREEN, go_to_start_menu),
]

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display a message at the top (optional)
    text_surface = font.render("Game Over", True, BLACK)
    screen.blit(text_surface, ((WIDTH - text_surface.get_width()) // 2, 50))

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
