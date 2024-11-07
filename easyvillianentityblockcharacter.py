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
bullet_speed = 20
bullets = []

# Triangle properties
triangle_speed = 5
triangles = []

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
    
    # Spawn triangles
    spawn_timer -= 1
    if spawn_timer <= 0:
        spawn_timer = 30
        # Add a triangle from the left or right side
        side = random.choice(["left", "right"])
        if side == "left":
            triangles.append([0, random.randint(0, HEIGHT), triangle_speed, 0])
        else:
            triangles.append([WIDTH, random.randint(0, HEIGHT), -triangle_speed, 0])
    
    # Update triangles
    for triangle in triangles[:]:
        triangle[0] += triangle[2]
        if (triangle[2] > 0 and triangle[0] > WIDTH) or (triangle[2] < 0 and triangle[0] < 0):
            triangles.remove(triangle)
    
    # Check for collisions
    for bullet in bullets[:]:
        for triangle in triangles[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
            triangle_rect = pygame.Rect(triangle[0], triangle[1], 20, 20)
            if bullet_rect.colliderect(triangle_rect):
                bullets.remove(bullet)
                triangles.remove(triangle)
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
    
    # Update display
    pygame.display.flip()

# Quit the game
pygame.quit()