import pygame
import random
import sys

WIDTH = 1000
HEIGHT = 700

class EnemyManager:
    def __init__(self, screen):
        self.screen = screen

        self.blue_square_image = pygame.image.load("graphics/enemy_o1.PNG").convert_alpha()
        self.red_square_image = pygame.image.load("graphics/enemy_o2.PNG").convert_alpha()

        self.blue_square_image = pygame.transform.scale(self.blue_square_image, (80, 80))
        self.red_square_image = pygame.transform.scale(self.red_square_image, (80, 80))  # Resize to fit your game


        # var to compare tick clock to next time an enemy spawns
        self.next_spawn_time = 0

    # Define the helper function to ensure valid y-coordinate for spawn
    def get_valid_y(self):
        y = random.randint(0, HEIGHT)
        return y

    # Function to check if the current_time is greater than the next spawn time, next_spawn_time increments by a number every time an enemy is spawned
    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time >= self.next_spawn_time:
            enemy_type = random.randint(0, 1)
            if enemy_type == 0:
                wall_side = random.randint(0,1)
                square = BlueSquare(1000*wall_side, random.randint(0, HEIGHT))
                squares.append(square)
            else:
                square = RedSquare(random.randint(0, WIDTH), -20, 2)
                squares.append(square)
            if current_time > 60000:
                self.next_spawn_time = current_time + 300
            elif current_time > 30000:
                self.next_spawn_time = current_time + 600
            elif current_time > 10000:
                self.next_spawn_time = current_time + 900
            else:
                self.next_spawn_time = current_time + 1200

    # Function for drawing enemies as blue squares
    def update_draw_enemies(self, render_scroll, player):
        for square in squares:
            # Adjust enemy position based on the scroll offset
            screen_x = square.x - render_scroll[0]
            screen_y = square.y - render_scroll[1]

            if isinstance(square, BlueSquare):
                if square.x > player.x:
                    square.x = square.x - 1.4
                elif square.x < player.x:
                    square.x = square.x + 1.4

                if square.y > player.y:
                    square.y = square.y - 1.4
                elif square.y < player.y:
                    square.y = square.y + 1.4
            elif isinstance(square, RedSquare):
                if square.x > player.x:
                    square.x = square.x - 1
                elif square.x < player.x:
                    square.x = square.x + 1

                if square.y > player.y:
                    square.y = square.y - 1
                elif square.y < player.y:
                    square.y = square.y + 1

            # Draw the blue square at the adjusted position
            if isinstance(square, BlueSquare):
                self.screen.blit(self.blue_square_image, (screen_x - 10, screen_y - 20))
            else:
                self.screen.blit(self.red_square_image, (screen_x - 10, screen_y - 20))


    def check_bullet_collision(self, bullets):
        # Check collision with squares
        for bullet in bullets[:]:  # Loop through all bullets
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)  # Create the bullet's rectangle
            for square in squares[:]:
                square_rect = pygame.Rect(square.x - 10, square.y - 10, 80, 80)  # Create the square's rectangle
                
                if bullet_rect.colliderect(square_rect):  # Check for collision
                    bullets.remove(bullet)  # Remove the bullet
                    square.hit_count -= 1  # Decrease hit count for the square
                    if square.hit_count <= 0:  # If hit count is zero, remove the square
                        squares.remove(square)
                    break  # Exit loop once the bullet hits a square

    def check_player_collision(self, player):
        player_width = 10
        player_height = 76

        # Define the hitbox as the entire rectangle of the player
        player_rect = pygame.Rect(player.x, player.y, player_width, player_height)
        for square in squares:
            # Assuming square has x, y, width, and height attributes
            square_rect = pygame.Rect(square.x, square.y, 20, 20)
            if square_rect.colliderect(player_rect):
                return True # Return True if player is hit
        return False # Return False if player is not hit

# Enemy List Initialization
squares = []
red_squares = []

# Square class (2 hits required)
class BlueSquare:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit_count = 1  # Set hit count for squares to 2

class RedSquare:
    def __init__(self, x, y, hit_count):
        self.x = x
        self.y = y
        self.hit_count = 2  # Set hit count for squares to 2