import pygame
import sys
import Start_home
from tilemap import Tilemap

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
        
        # Tilemap instance
        self.tilemap = Tilemap(self.scroll, self.display)

        # Player properties
        self.player_x = 400
        self.player_y = 150
        self.player_width = 20
        self.player_height = 20
        self.player_gravity = 0
        self.is_jumping = False

        # Define the ground (as a Rect object)
        self.ground = pygame.Rect(0, 555, 1000, 10)  # Ground positioned at y=550

    def game_loop(self):
        background = pygame.image.load("graphics/background.png")

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
                self.player_gravity = -9
                self.is_jumping = True

            # Gravity effect
            self.player_gravity += 0.4
            self.player_y += self.player_gravity
            player.y = self.player_y

            # Check for collision with grass platforms in Tilemap
            for platform in self.tilemap.grass_platforms:
                if player.colliderect(platform) and self.player_gravity > 0:
                    self.player_y = platform.top - self.player_height
                    self.player_gravity = 0
                    self.is_jumping = False

            # Platform collision (check for white platforms specifically)
            for platform in self.tilemap.white_platforms:  # Access the white platforms from the tilemap
                if player.colliderect(platform):
                    if self.player_gravity > 0:
                        self.player_y = platform.top - self.player_height  # Stop falling by setting player position to platform top
                        self.player_gravity = 0  # Reset gravity so player doesn't keep falling
                        self.is_jumping = False  # The player has landed on the platform, so they're not jumping anymore
                    else:
                        self.player_y = platform.bottom
                        self.player_gravity = 0


            if self.player_x < 0:
                self.player_x = 0
            if self.player_x > 980:
                self.player_x = 980


            # Ground collision (for player landing)
            if player.colliderect(self.ground) and self.player_gravity > 0:
                self.player_y = self.ground.top - self.player_height
                self.player_gravity = 0
                self.is_jumping = False

            # Prevent player from falling off the screen
            if self.player_y >= self.world_height - self.player_height:
                self.player_y = self.world_height - self.player_height
                self.player_gravity = 0
                self.is_jumping = False

            # Draw everything with scroll offsets on the display surface
            self.display.fill((0, 0, 0))

            # Draw background first (so it's behind everything else)
            self.display.blit(background, (-render_scroll[0], -render_scroll[1]))

            # Draw player with scroll offset
            pygame.draw.rect(self.display, (255,255,255), player.move(-render_scroll[0], -render_scroll[1]))

            # Use the tilemap's render function to draw the platforms
            self.tilemap.render()

            # Scale and blit the display surface to the main screen
            self.screen.blit(pygame.transform.scale(self.display, (self.screen_width, self.screen_height)), (0, 0))

            pygame.display.flip()  # Update the display
            self.clock.tick(60)

        pygame.quit()
        sys.exit()



# Run the start page and then the game
Start_home.start_page()
if Start_home.game_active:
    Game().game_loop()
