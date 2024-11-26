import pygame
import sys
import Start_home
import math
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

        self.bullets = []  # Bullets list

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        bullet_speed = 14

                        # Adjust mouse position to account for scaling and scrolling
                        adjusted_mouse_x = mouse_x / (self.screen_width / self.display.get_width()) + render_scroll[0]
                        adjusted_mouse_y = mouse_y / (self.screen_height / self.display.get_height()) + render_scroll[1]

                        # Calculate the direction of the bullet
                        angle = math.atan2(
                            adjusted_mouse_y - self.player_y,
                            adjusted_mouse_x - self.player_x
                        )
                        dx = math.cos(angle) * bullet_speed
                        dy = math.sin(angle) * bullet_speed

                        # Add the bullet to self.bullets
                        self.bullets.append([self.player_x, self.player_y, dx, dy])


            keys = pygame.key.get_pressed()

            # Define player rectangle
            player = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)

            # Player movement
            if keys[pygame.K_a]:
                self.player_x -= 5

            if keys[pygame.K_d]:
                self.player_x += 5

            # Jumping logic
            if keys[pygame.K_SPACE] and not self.is_jumping:
                self.player_gravity = -9
                self.is_jumping = True

            # Gravity effect
            self.player_gravity += 0.4
            self.player_y += self.player_gravity

            # Platform collision (grass and white platforms)
            for platform in self.tilemap.grass_platforms + self.tilemap.white_platforms:
                if player.colliderect(platform) and self.player_gravity > 0:
                    self.player_y = platform.top - self.player_height
                    self.player_gravity = 0
                    self.is_jumping = False

            # Ground collision
            if player.colliderect(self.ground) and self.player_gravity > 0:
                self.player_y = self.ground.top - self.player_height
                self.player_gravity = 0
                self.is_jumping = False

            # Prevent player from falling off the screen
            if self.player_y >= self.world_height - self.player_height:
                self.player_y = self.world_height - self.player_height
                self.player_gravity = 0
                self.is_jumping = False

            # Draw everything
            self.display.fill((0, 0, 0))
            self.display.blit(background, (-render_scroll[0], -render_scroll[1]))

            # Draw player with scroll offset
            pygame.draw.rect(
                self.display, (255, 255, 255),
                player.move(-render_scroll[0], -render_scroll[1])
            )

            # Draw bullets and update their positions
            for bullet in self.bullets[:]:
                bullet[0] += bullet[2]
                bullet[1] += bullet[3]
                if bullet[0] < 0 or bullet[0] > self.world_width or bullet[1] < 0 or bullet[1] > self.world_height:
                    self.bullets.remove(bullet)
                else:
                    pygame.draw.circle(
                        self.display, (255, 255, 255),
                        (int(bullet[0] - render_scroll[0]), int(bullet[1] - render_scroll[1])), 5
                    )

            # Render platforms
            self.tilemap.render()

            # Scale and blit the display surface to the main screen
            self.screen.blit(
                pygame.transform.scale(self.display, (self.screen_width, self.screen_height)), (0, 0)
            )

            pygame.display.flip()  # Update the display
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


# Run the start page and then the game
Start_home.start_page()
if Start_home.game_active:
    Game().game_loop()
