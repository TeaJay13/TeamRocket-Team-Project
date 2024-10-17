import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

WHITE = (255, 255, 255)

rect_x = 100
rect_y = 150
rect_width = 50
rect_height = 50
rect_gravity = 0
is_jumping = False  # To track if the rectangle is in a jump

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Create the rectangles
    rectangle = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
    platform = pygame.Rect(200, 300, 500, 20)

    # Move the rectangle
    if keys[pygame.K_LEFT]:
        rect_x -= 3
        rectangle.x = rect_x
        if rectangle.colliderect(platform):
            rect_x += 3

    if keys[pygame.K_RIGHT]:
        rect_x += 2
        rectangle.x = rect_x
        if rectangle.colliderect(platform):
            rect_x -= 3

    if keys[pygame.K_SPACE] and not is_jumping:  # Jump only when not already jumping
        rect_gravity = -30  # Negative gravity for upward jump
        is_jumping = True

    rect_gravity += 1  # Simulate gravity (increases over time)
    rect_y += rect_gravity
    rectangle.y = rect_y

    # Check for collisions with platform (coming from above)
    if rectangle.colliderect(platform) and rect_gravity > 0:
        rect_y = platform.y - rect_height  # Position the rectangle on top of the platform
        rect_gravity = 0  # Stop gravity
        is_jumping = False  # Allow jumping again

    # Prevent the rectangle from falling off the bottom of the screen
    if rect_y >= screen_height - rect_height:
        rect_y = screen_height - rect_height
        rect_gravity = 0
        is_jumping = False

    # Fill the screen and draw the rectangles
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, rectangle)
    pygame.draw.rect(screen, WHITE, platform)
    
    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
