import pygame

class Tilemap:
    def __init__(self, render_scroll, display):
        self.render_scroll = render_scroll
        self.display = display
        
        self.platform_texture = pygame.image.load("graphics/platform00.png")
        self.long_platform_texture = pygame.image.load("graphics/long_platform_01.png")

        self.WHITE = (255, 255, 255)

        # Define the platforms
        self.white_platforms = [
            pygame.Rect(300, 340, 400, 10),
            pygame.Rect(300, 436, 400, 10),
            pygame.Rect(400, 250, 200, 10)
        ]
        self.grass_platforms = [
            pygame.Rect(100, 500, 100, 20),
            pygame.Rect(100, 400, 100, 20),
            pygame.Rect(100, 300, 100, 20),
            pygame.Rect(800, 500, 100, 20),
            pygame.Rect(800, 300, 100, 20),
            pygame.Rect(800, 400, 100, 20)
        ]

    def render(self):
        # Render the white platforms (with their texture or color)
        for platform in self.white_platforms:
            platform_rect = platform.move(-self.render_scroll[0], -self.render_scroll[1])

            # Scale the texture to match the platform width and height
            scaled_texture = pygame.transform.scale(self.long_platform_texture, (platform_rect.width, platform_rect.height))

            # Blit the scaled texture onto the display at its position
            self.display.blit(scaled_texture, platform_rect)

        # Render the grass platforms (with their texture)
        for platform in self.grass_platforms:
            platform_rect = platform.move(-self.render_scroll[0], -self.render_scroll[1])

            # Scale the texture to match the platform width and height
            scaled_platform = pygame.transform.scale(self.platform_texture, (platform_rect.width, platform_rect.height))

            # Blit the scaled texture onto the display at the platform's position
            self.display.blit(scaled_platform, platform_rect)
