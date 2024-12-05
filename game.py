import pygame
import sys
import Start_home
import math
import scoring
import database
from tilemap import Tilemap

class Square:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.hit_count = 2  # Set hit count for squares to 2

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Block Game')
        self.screen_width = 1000
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Font initialization
        self.font = pygame.font.Font(None, 36)  # Default Pygame font, size 36

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
        self.player_x = 425
        self.player_y = 150
        self.player_width = 40
        self.player_height = 76
        self.player_gravity = 0
        self.is_jumping = False

        # Define the ground (as a Rect object)
        self.ground = pygame.Rect(-100, 600, 1200, 10)  # Ground positioned at y=550

        self.sprite_sheet_idle = pygame.image.load("graphics/player_char_idle.png").convert_alpha()
        self.sprite_sheet_moving = pygame.image.load("graphics/player_char_moving.png").convert_alpha()

        self.idle_frames = self.load_frames(self.sprite_sheet_idle, 0, 4, 64, 85)
        self.walk_frames = self.load_frames(self.sprite_sheet_moving, 0, 6, 64, 85)

        self.current_frames = self.idle_frames
        self.current_frame_index = 0
        self.animation_timer = 0

        self.bullets = []  # Bullets list

    def load_frames(self, sprite_sheet, start_index, count, width, height):
        frames = []
        for i in range(start_index, start_index + count):
            x = i * width  # Горизонтальная позиция кадра
            y = 0  # Так как все кадры находятся в одной строке, вертикальная позиция всегда 0

            # Проверяем, не выходит ли кадр за пределы изображения
            if x + width > sprite_sheet.get_width() or y + height > sprite_sheet.get_height():
                raise ValueError(f"Frame {i} out of bounds: x={x}, y={y}, width={width}, height={height}, "
                                 f"sheet_width={sprite_sheet.get_width()}, sheet_height={sprite_sheet.get_height()}")
        
            frame = sprite_sheet.subsurface(pygame.Rect(x, y, width, height))
            frames.append(frame)
    
        return frames


    def update_animation(self, keys):
        # Determine the current frame set based on player movement
        if keys[pygame.K_a] or keys[pygame.K_d]:
            if self.current_frames != self.walk_frames:
                self.current_frames = self.walk_frames
                self.current_frame_index = 0  # Reset frame index
        else:
            if self.current_frames != self.idle_frames:
                self.current_frames = self.idle_frames
                self.current_frame_index = 0  # Reset frame index

        # Increment the animation timer
        self.animation_timer += 1
        if self.animation_timer >= 10:  # Change frame every 10 ticks
            self.animation_timer = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.current_frames)


        

    def game_loop(self):
        # Start the timer and initialize the database**
        scoring.start_timer()
        database.initialize_db()

        # Load initial background
        global background_state, game_active, background_chosen
        background_forest = pygame.image.load("graphics/BG1.svg") #draw a bottom on those and rename them
        background_swamp = pygame.image.load("graphics/BG2.svg")

        background1_scaled = pygame.transform.scale(background_forest, (self.screen_width, self.screen_height))
        background2_scaled = pygame.transform.scale(background_swamp, (self.screen_width, self.screen_height))

        if Start_home.background_state == 0:
            background = background1_scaled
        if Start_home.background_state == 1:
            background = background2_scaled




        running = True
        while running:
            # Calculate the scroll offset to center player
            center_x = self.display.get_width() / 2
            center_y = self.display.get_height() / 2

            self.scroll[0] += (self.player_x - center_x - self.scroll[0])  / 10
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

            # Define player rectangle
            player = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)

            # Constrain player position horizontally to stay within the bounds (0 to 1000 pixels)
            if self.player_x < -20:
                self.player_x = -20
            elif self.player_x > 960:
                self.player_x = 960


            # Platform collision (grass and white platforms)
            for platform in self.tilemap.grass_platforms:
                if player.colliderect(platform) and self.player_gravity > 0:
                    self.player_y = platform.top - self.player_height
                    self.player_gravity = 0
                    self.is_jumping = False

            for platform in self.tilemap.white_platforms:
                if player.colliderect(platform):
                    # Check if the player is falling onto the platform
                    if self.player_gravity > 0 and player.bottom - 10 <= platform.top + self.player_gravity:
                        self.player_y = platform.top - self.player_height
                        self.player_gravity = 0
                        self.is_jumping = False
                    # Check if the player is jumping up and hits the platform from below
                    elif self.player_gravity < 0 and player.top >= platform.bottom - abs(self.player_gravity):
                        self.player_y = platform.bottom
                        self.player_gravity = 0


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

            self.update_animation(keys)

            # Draw everything
            self.display.fill((0, 0, 0))
            self.display.blit(background, (-render_scroll[0], -render_scroll[1]))

            if self.current_frame_index < 0 or self.current_frame_index >= len(self.current_frames):
                raise IndexError(f"Invalid frame index: {self.current_frame_index}. Available frames: {len(self.current_frames)}")
            else:
                 current_frame = self.current_frames[self.current_frame_index]
            self.display.blit(current_frame, (self.player_x - render_scroll[0], self.player_y - render_scroll[1]))


            # # Draw player with scroll offset
            # pygame.draw.rect(
            #     self.display, (255, 255, 255),
            #     player.move(-render_scroll[0], -render_scroll[1])
            # )

            # Draw bullets and update their positions
            for bullet in self.bullets[:]:
                bullet[0] += bullet[2]
                bullet[1] += bullet[3]
                if bullet[0] < 0 or bullet[0] > self.world_width or bullet[1] < 0 or bullet[1] > self.world_height:
                    self.bullets.remove(bullet)
                else:
                    pygame.draw.circle(
                        self.display, (255, 165, 20),
                        (int(bullet[0] - render_scroll[0]), int(bullet[1] - render_scroll[1])), 5
                    )

            # Render platforms
            self.tilemap.render()

            self.screen.blit(
                pygame.transform.scale(self.display, (self.screen_width, self.screen_height)), (0, 0)
            )

            # Update and display score and timer
            scoring.update_timer()
            scoring.display_timer_and_score(self.screen, self.font)


            pygame.display.flip()  # Update the display
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


# Run the start page and then the game
Start_home.start_page()
if Start_home.game_active:
    Game().game_loop()
