import pygame
import sys
import Start_home

WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Block Game')
        self.screen_width = 1000
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Smaller display surface to act as the viewport
        self.display = pygame.Surface((1000, 500))  # The size of the "camera" viewport

        self.clock = pygame.time.Clock()

        # World and player properties
        self.world_width = 1000
        self.world_height = 700

        # Scroll offset for the camera
        self.scroll = [0, 0]

        # Player properties
        self.player_x = 400
        self.player_y = 150
        self.player_width = 20
        self.player_height = 20
        self.player_gravity = 0
        self.is_jumping = False

        # Define platforms
        self.platforms = [
            Platform(200, 450, 500, 10),
            Platform(200, 300, 500, 10),
        ]

        # Ground platform for collision
        self.ground = Platform(0, 555, 1000, 10)  # Ground positioned at y=550

        # Load platform texture
        self.platform_texture = pygame.image.load("graphics/platform00.png")

    def game_loop(self):
        background = pygame.image.load("graphics/bacground.PNG")

        running = True
        while running:
            # Calculate the scroll offset to center player
            center_x = self.display.get_width() / 2
            center_y = self.display.get_height() / 2

            self.scroll[0] += (self.player_x - center_x - self.scroll[0]) / 10
            self.scroll[1] += (self.player_y - center_y - self.scroll[1]) / 10

            # Constrain scroll to the world boundaries
            self.scroll[0] = max(0, min(self.scroll[0], self.world_width - self.display.get_width()))
            self.scroll[1] = max(0, min(self.scroll[1], self.world_height - self.display.get_height()))

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            # Define player rectangle
            player = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)

            # Player movement
            if keys[pygame.K_a]:
                self.player_x -= 5
                player.x = self.player_x

            if keys[pygame.K_d]:
                self.player_x += 5
                player.x = self.player_x

            # Jumping logic
            if keys[pygame.K_SPACE] and not self.is_jumping:
                self.player_gravity = -20
                self.is_jumping = True

            # Gravity effect
            self.player_gravity += 1
            self.player_y += self.player_gravity
            player.y = self.player_y

            # Platform collision
            for platform in self.platforms:
                if player.colliderect(platform.get_rect()) and self.player_gravity > 0:
                    self.player_y = platform.y - self.player_height
                    self.player_gravity = 0
                    self.is_jumping = False

            # Ground collision (for player landing)
            if player.colliderect(self.ground.get_rect()) and self.player_gravity > 0:
                self.player_y = self.ground.y - self.player_height
                self.player_gravity = 0
                self.is_jumping = False

            # Prevent player from falling off the screen
            if self.player_y >= self.world_height - self.player_height:
                self.player_y = self.world_height - self.player_height
                self.player_gravity = 0
                self.is_jumping = False

            # Draw everything with scroll offsets on the display surface
            self.display.fill((0, 0, 0))

            # Draw ground (drawn here behind the player but still used for collision)
            pygame.draw.rect(self.display, WHITE, self.ground.get_rect().move(-render_scroll[0], -render_scroll[1]))

            # Draw background first (so it's behind everything else)
            self.display.blit(background, (-render_scroll[0], -render_scroll[1]))  # Scroll background

            # Draw player and platforms with scroll offset
            pygame.draw.rect(self.display, WHITE, player.move(-render_scroll[0], -render_scroll[1]))

            # Blit platforms using the texture (instead of drawing a rectangle)
            # Blit platforms using the texture and scale it to match the platform width
            for platform in self.platforms:
                # Get the platform rectangle
                platform_rect = platform.get_rect().move(-render_scroll[0], -render_scroll[1])
                
                # Scale the texture to match the width and height of the platform
                scaled_platform = pygame.transform.scale(self.platform_texture, (platform_rect.width, platform_rect.height))
                
                # Blit the scaled texture onto the display at the platform's position
                self.display.blit(scaled_platform, platform_rect)


            # Scale and blit the display surface to the main screen
            self.screen.blit(pygame.transform.scale(self.display, (self.screen_width, self.screen_height)), (0, 0))

            # Update the display
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
