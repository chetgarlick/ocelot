"""
Coin class - represents a collectible currency item
"""

import pygame
from src.sprite_renderer import SpriteRenderer


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

        # Create detailed coin sprite
        self.image = SpriteRenderer.create_coin_sprite(self.width, self.height)

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

