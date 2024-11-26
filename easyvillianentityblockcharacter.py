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
SQUARE_SIZE = 50
square_x, square_y = WIDTH // 2, HEIGHT // 2

# Bullet properties
bullet_speed = 25
bullets = []

# Triangle properties
triangle_speed = 5
triangles = []

# square properties
square_speed = 5
squares = []

# hexagon properties
hexagon_speed = 5
hexagons = []

# Game settings
spawn_timer = 30  # Timer for triangle spawn rate

# Main loop control
running = True
clock = pygame.time.Clock()

# Game loop
while running:
    clock.tick(30)
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Shoot a bullet
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Calculate the direction of the bullet
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
    
    # Spawn triangles, squares, and hexagons
    spawn_timer -= 1
    if spawn_timer <= 0:
        spawn_timer = 30

    # Spawn triangles
    side = random.choice(["left", "right"])
    if side == "left":
        triangles.append([0, random.randint(0, HEIGHT), triangle_speed, 0])  # [x, y, x_speed, y_speed]
    else:
        triangles.append([WIDTH, random.randint(0, HEIGHT), -triangle_speed, 0])

    # Spawn squares
    side = random.choice(["left", "right"])
    if side == "left":
        squares.append([0, random.randint(0, HEIGHT), square_speed, 0])  # [x, y, x_speed, y_speed]
    else:
        squares.append([WIDTH, random.randint(0, HEIGHT), -square_speed, 0])

    # Spawn hexagons
    side = random.choice(["left", "right"])
    if side == "left":
        hexagons.append([0, random.randint(0, HEIGHT), hexagon_speed, 0])  # [x, y, x_speed, y_speed]
    else:
        hexagons.append([WIDTH, random.randint(0, HEIGHT), -hexagon_speed, 0])

    # Update triangles
    for triangle in triangles[:]:
        triangle[0] += triangle[2]  # Update x position
        if (triangle[2] > 0 and triangle[0] > WIDTH) or (triangle[2] < 0 and triangle[0] < 0):
            triangles.remove(triangle)

    # Update squares
    for square in squares[:]:
        square[0] += square[2]  # Update x position
        if (square[2] > 0 and square[0] > WIDTH) or (square[2] < 0 and square[0] < 0):
            squares.remove(square)

    # Update hexagons
    for hexagon in hexagons[:]:
        hexagon[0] += hexagon[2]  # Update x position
        if (hexagon[2] > 0 and hexagon[0] > WIDTH) or (hexagon[2] < 0 and hexagon[0] < 0):
            hexagons.remove(hexagon)

    # Check for collisions
    for bullet in bullets[:]:
        # Check collision with triangles
        for triangle in triangles[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
            triangle_rect = pygame.Rect(triangle[0], triangle[1], 20, 20)
            if bullet_rect.colliderect(triangle_rect):
                bullets.remove(bullet)
                triangles.remove(triangle)
                break

    # Check collision with squares
    for square in squares[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
        square_rect = pygame.Rect(square[0] - 10, square[1] - 10, 20, 20)  # Square's bounding box
        if bullet_rect.colliderect(square_rect):
            bullets.remove(bullet)
            squares.remove(square)
            break

    # Check collision with hexagons
    for hexagon in hexagons[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
        hexagon_rect = pygame.Rect(hexagon[0] - 30, hexagon[1] - 30, 60, 60)  # Hexagon's bounding box
        if bullet_rect.colliderect(hexagon_rect):
            bullets.remove(bullet)
            hexagons.remove(hexagon)
            break

    
    # Draw the square (stationary in center)
    pygame.draw.rect(screen, WHITE, (square_x - SQUARE_SIZE // 2, square_y - SQUARE_SIZE // 2, SQUARE_SIZE, SQUARE_SIZE))
    
    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), 5)
    
    # Draw triangles
    for triangle in triangles:
        pygame.draw.polygon(screen, RED, [
            (triangle[0], triangle[1]),
            (triangle[0] - 20, triangle[1] - 10),
            (triangle[0] - 20, triangle[1] + 10)
        ])

    for square in squares:
        pygame.draw.polygon(screen, (0, 0, 255), [  # Blue color (R, G, B)
        (square[0] - 10, square[1] - 10),  # Top-left
        (square[0] + 10, square[1] - 10),  # Top-right
        (square[0] + 10, square[1] + 10),  # Bottom-right
        (square[0] - 10, square[1] + 10)   # Bottom-left
    ])

    for hexagon in hexagons:
        pygame.draw.polygon(screen, (0, 255, 0), [  # Green color (R, G, B)
            (hexagon[0], hexagon[1] - 30),  # Top
            (hexagon[0] + 26, hexagon[1] - 15),  # Top-right
            (hexagon[0] + 26, hexagon[1] + 15),  # Bottom-right
            (hexagon[0], hexagon[1] + 30),  # Bottom
            (hexagon[0] - 26, hexagon[1] + 15),  # Bottom-left
            (hexagon[0] - 26, hexagon[1] - 15)   # Top-left
        ])
    
    # Update display
    pygame.display.flip()

# Quit the game
pygame.quit()