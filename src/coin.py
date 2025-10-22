"""
Coin class - represents a collectible currency item
"""

import pygame


class Coin:
    """A collectible coin that the player can pick up"""

    def __init__(self, x, y):
        """Initialize a coin
        
        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
        """
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.radius = 8
        
        # Create a yellow circular coin image
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_colorkey((0, 0, 0))  # Make black transparent
        self.image.fill((0, 0, 0))  # Fill with black (will be transparent)
        
        # Draw a yellow circle
        pygame.draw.circle(
            self.image,
            (255, 255, 0),  # Yellow color
            (self.radius, self.radius),
            self.radius
        )
        
        # Create rect for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        """Update coin position (currently static)"""
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface, camera):
        """Draw the coin to the screen with camera offset
        
        Args:
            surface: Pygame surface to draw to
            camera: Camera object for viewport offset
        """
        screen_x, screen_y = camera.apply_point(self.x, self.y)
        
        # Only draw if visible on screen
        if -self.width < screen_x < camera.width and \
           -self.height < screen_y < camera.height:
            surface.blit(self.image, (screen_x, screen_y))

