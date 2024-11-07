import pygame
import sys
import Start_home

WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Block Game')
        self.screen = pygame.display.set_mode((1000, 700))
        self.display = pygame.Surface((840, 240))

        self.clock = pygame.time.Clock()

        self.world_width = 1000  # Width of the game world in pixels
        self.world_height = 300  # Height adjusted to match screen height

        self.scroll = [0, 0]

        # Set the initial player position closer to the center
        self.player_x = 400
        self.player_y = 150
        self.player_width = 20
        self.player_height = 20
        self.player_gravity = 0
        self.is_jumping = False  # To track if the rectangle is in a jump

        # Create platforms as instances of Platform class
        self.platforms = [
            Platform(200, 600, 500, 5),
            Platform(200, 450, 500, 5),
            Platform(200, 300, 500, 5)
        ]

    def game_loop(self):
        running = True
        while running:
            # Calculate the scroll based on the player position
            center_x = self.display.get_width() / 2
            center_y = self.display.get_height() / 2

            # Calculate scroll to keep the player centered
            self.scroll[0] += (self.player_x - center_x - self.scroll[0]) / 10
            self.scroll[1] += (self.player_y - center_y - self.scroll[1]) / 10

            # Constrain the scroll within the boundaries of the game world
            self.scroll[0] = max(0, min(self.scroll[0], self.world_width - self.display.get_width()))
            self.scroll[1] = max(0, min(self.scroll[1], self.world_height - self.display.get_height()))

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            # Create the player rectangle (using the scroll offset for rendering)
            player = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)

            # Move the player left and right
            if keys[pygame.K_a]:
                self.player_x -= 5
                player.x = self.player_x

            if keys[pygame.K_d]:
                self.player_x += 5
                player.x = self.player_x

            # Handle jumping
            if keys[pygame.K_SPACE] and not self.is_jumping:
                self.player_gravity = -20
                self.is_jumping = True

            self.player_gravity += 1  # Apply gravity
            self.player_y += self.player_gravity
            player.y = self.player_y

            # Check for platform collision from above
            on_ground = False
            for platform in self.platforms:
                if player.colliderect(platform.get_rect()) and self.player_gravity > 0:
                    self.player_y = platform.y - self.player_height
                    self.player_gravity = 0
                    self.is_jumping = False
                    on_ground = True
            
            # Prevent falling off screen
            screen_height = self.screen.get_height()
            if self.player_y >= screen_height - self.player_height:
                self.player_y = screen_height - self.player_height
                self.player_gravity = 0
                self.is_jumping = False

            # Fill the screen, applying scroll offset when rendering
            self.screen.fill((0, 0, 0))

            # Draw player
            pygame.draw.rect(self.screen, WHITE, player.move(-render_scroll[0], -render_scroll[1]))

            # Draw platforms
            for platform in self.platforms:
                pygame.draw.rect(self.screen, WHITE, platform.get_rect().move(-render_scroll[0], -render_scroll[1]))

            # Update the display and limit the frame rate
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

class Platform:
    def __init__(self, x, y, length, height):
        self.x = x
        self.y = y
        self.length = length
        self.height = height
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.length, self.height)

# Run the start page and then the game
Start_home.start_page()
if Start_home.game_active:
    Game().game_loop()
