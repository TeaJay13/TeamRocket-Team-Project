import pygame
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Square properties (centered)
SQUARE_SIZE = 30
square_x, square_y = WIDTH // 2, HEIGHT // 2

# Exclude stationary square's y-coordinate range
square_y_range = (square_y - SQUARE_SIZE // 2, square_y + SQUARE_SIZE // 2)

# Define the helper function to ensure valid y-coordinate for spawn
def get_valid_y():
    while True:
        y = random.randint(0, HEIGHT)
        if y < square_y_range[0] or y > square_y_range[1]:
            return y

# Bullet properties
bullet_speed = 70
bullets = []

# Triangle properties
triangle_speed = 5
triangles = []

# Square properties
square_speed = 4
squares = []

# Hexagon properties
hexagon_speed = 2
hexagons = []

# Square class (2 hits required)
class Square:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.hit_count = 2  # Set hit count for squares to 2

class Hexagon:
    def __init__(self, x, y, speed, hit_count):
        self.x = x
        self.y = y
        self.speed = speed
        self.hit_count = hit_count  # Initialize hit count for the hexagon

    def update(self):
        self.x += self.speed  # Move hexagon based on its speed

    def draw(self, screen):
        # Draw hexagon
        pygame.draw.polygon(screen, (0, 255, 0), [
            (self.x, self.y - 30),  # Top
            (self.x + 26, self.y - 15),  # Top-right
            (self.x + 26, self.y + 15),  # Bottom-right
            (self.x, self.y + 30),  # Bottom
            (self.x - 26, self.y + 15),  # Bottom-left
            (self.x - 26, self.y - 15)   # Top-left
        ])
        
        # Display hit count on the hexagon
        font = pygame.font.Font(None, 36)
        hit_text = font.render(str(self.hit_count), True, (255, 255, 255))
        screen.blit(hit_text, (self.x - 10, self.y - 10))  # Display hit count near the hexagon

# Game settings
start_time = pygame.time.get_ticks()  # Get the initial time (in milliseconds)
spawn_timer = 0  # This is for the general spawn interval

# Game loop control
running = True
clock = pygame.time.Clock()

# Timers for each piece type spawn
last_triangle_spawn_time = 0
last_square_spawn_time = 0
last_hexagon_spawn_time = 0

# Spawn interval for each piece type (3 seconds)
spawn_interval = 3000  # 3 seconds (3000 milliseconds)
spawn_count = 1  # Start with 1 piece spawning at a time

# Main game loop
while running:
    clock.tick(30)  # Run the game at 30 FPS
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (square_x - SQUARE_SIZE // 2, square_y - SQUARE_SIZE // 2, SQUARE_SIZE, SQUARE_SIZE))


    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Shoot a bullet
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - square_y, mouse_x - square_x)
                dx = math.cos(angle) * bullet_speed
                dy = math.sin(angle) * bullet_speed
                bullets.append([square_x, square_y, dx, dy])

    # Update bullets
    for bullet in bullets[:]:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
        if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:  # Remove if off-screen
            bullets.remove(bullet)

    # Get the elapsed time since the start of the game
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    # Handle spawning of triangles, squares, and hexagons
    # Spawn triangles every 3 seconds, starting immediately
    if current_time - last_triangle_spawn_time >= spawn_interval:
        last_triangle_spawn_time = current_time  # Update the last spawn time for triangles
        for _ in range(spawn_count):  # Spawn spawn_count number of triangles
            side = random.choice(["left", "right"])
            y = get_valid_y()  # Ensure valid y-coordinate for spawn
            if side == "left":
                triangles.append([0, y, triangle_speed, 0])
            else:
                triangles.append([WIDTH, y, -triangle_speed, 0])

    # Spawn squares after 20 seconds, every 3 seconds
    if elapsed_time >= 20000 and current_time - last_square_spawn_time >= spawn_interval:
        last_square_spawn_time = current_time  # Update the last spawn time for squares
        for _ in range(spawn_count):  # Spawn spawn_count number of squares
            side = random.choice(["left", "right"])
            y = get_valid_y()
            if side == "left":
                squares.append(Square(0, y, square_speed))  # Create a Square object and append it
            else:
                squares.append(Square(WIDTH, y, -square_speed))  # Create a Square object and append it

    # Spawn hexagons after 40 seconds, every 3 seconds
    if elapsed_time >= 40000 and current_time - last_hexagon_spawn_time >= spawn_interval:
        last_hexagon_spawn_time = current_time  # Update the last spawn time for hexagons
        for _ in range(spawn_count):  # Spawn spawn_count number of hexagons
            side = random.choice(["left", "right"])
            y = get_valid_y()
            # Append a new Hexagon object to the hexagons list
            if side == "left":
                hexagons.append(Hexagon(0, y, hexagon_speed, 5))  # Hexagon with 5 hits to destroy
            else:
                hexagons.append(Hexagon(WIDTH, y, -hexagon_speed, 5))  # Hexagon with 5 hits to destroy

    # Gradually increase spawn count every 10 seconds (after 10, 20, 30, etc. seconds)
    if elapsed_time % 10000 == 0 and spawn_count < 10:  # Max spawn count cap (e.g., 10 pieces max)
        spawn_count += 1

    # Update triangles
    for triangle in triangles[:]:
        triangle[0] += triangle[2]  # Update x position
        if (triangle[2] > 0 and triangle[0] > WIDTH) or (triangle[2] < 0 and triangle[0] < 0):
            triangles.remove(triangle)

    # Update squares
    for square in squares[:]:
        square.x += square.speed  # Accessing 'x' attribute of the Square object
        if (square.speed > 0 and square.x > WIDTH) or (square.speed < 0 and square.x < 0):
            squares.remove(square)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), 5)

    # Draw triangles
    for triangle in triangles:
        pygame.draw.polygon(screen, RED, [
            (triangle[0], triangle[1]),
            (triangle[0] - 20, triangle[1] - 20),
            (triangle[0] - 20, triangle[1] + 20)
        ])

    # Collision check with updated logic for squares and hexagons
    for bullet in bullets[:]:
    # Check collision with triangles
        for triangle in triangles[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
            triangle_rect = pygame.Rect(triangle[0] - 10, triangle[1] - 10, 20, 20)  # Adjust triangle's bounding box
            if bullet_rect.colliderect(triangle_rect):
                bullets.remove(bullet)
                triangles.remove(triangle)
                break

        # Check collision with squares
        for square in squares[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
            square_rect = pygame.Rect(square.x - 10, square.y - 10, 20, 20)
            if bullet_rect.colliderect(square_rect):
                bullets.remove(bullet)
                square.hit_count -= 1  # Decrease hit count for the square
                if square.hit_count <= 0:  # If hit count is zero, remove square
                    squares.remove(square)
                break

        # Check collision with hexagons
        for hexagon in hexagons[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
            hexagon_rect = pygame.Rect(hexagon.x - 30, hexagon.y - 30, 60, 60)  # Hexagon's bounding box
            if bullet_rect.colliderect(hexagon_rect):
                bullets.remove(bullet)
                hexagon.hit_count -= 1  # Decrease hit count
                if hexagon.hit_count <= 0:  # Remove hexagon when it reaches 0 hits
                    hexagons.remove(hexagon)
                break

    # Draw squares with hit count
    for square in squares:
        pygame.draw.polygon(screen, (0, 0, 255), [  # Blue color (R, G, B)
            (square.x - 15, square.y - 15),  # Top-left
            (square.x + 15, square.y - 15),  # Top-right
            (square.x + 15, square.y + 15),  # Bottom-right
            (square.x - 15, square.y + 15)   # Bottom-left
        ])
        # Draw the hit count on the square
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(str(square.hit_count), True, (255, 255, 255))
        screen.blit(text, (square.x - 10, square.y - 10))

    # Update hexagons
    for hexagon in hexagons[:]:
        hexagon.update()

        # Remove hexagon if it moves off-screen
        if (hexagon.speed > 0 and hexagon.x > WIDTH) or (hexagon.speed < 0 and hexagon.x < 0):
            hexagons.remove(hexagon)

        # Draw the hexagon and hit count
        hexagon.draw(screen)

    # Update display
    pygame.display.flip()

pygame.quit()
