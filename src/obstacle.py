"""
Obstacle class - represents static obstacles in the world
"""

import pygame


class Obstacle:
    """A static obstacle that blocks movement"""

    def __init__(self, x, y, width, height, color=(128, 128, 128)):
        """Initialize an obstacle

        Args:
            x: X position in pixels
            y: Y position in pixels
            width: Width in pixels
            height: Height in pixels
            color: RGB tuple for obstacle color (default: grey)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Create rect for collision detection
        self.rect = pygame.Rect(x, y, width, height)

        # Create image for rendering
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

    def draw(self, surface):
        """Draw the obstacle to the screen"""
        surface.blit(self.image, self.rect)

