"""
Star class - represents a collectible currency item
"""

import pygame


class Star:
    """A collectible star that the player can pick up"""

    def __init__(self, x, y):
        """Initialize a star
        
        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
        """
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        
        # Create a yellow star image
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 255, 0))  # Yellow color
        
        # Draw a simple star shape (filled rectangle for now, can be improved)
        # Create a star by drawing a filled circle-like shape
        pygame.draw.polygon(
            self.image,
            (255, 255, 0),
            [
                (8, 0),    # top point
                (10, 6),   # top-right
                (16, 6),   # right point
                (11, 10),  # bottom-right
                (13, 16),  # bottom point
                (8, 12),   # bottom-left
                (3, 16),   # left point
                (5, 10),   # top-left
                (0, 6),    # left point
                (6, 6),    # top-right
            ]
        )
        
        # Create rect for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        """Update star position (currently static)"""
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface, camera):
        """Draw the star to the screen with camera offset
        
        Args:
            surface: Pygame surface to draw to
            camera: Camera object for viewport offset
        """
        screen_x, screen_y = camera.apply_point(self.x, self.y)
        
        # Only draw if visible on screen
        if -self.width < screen_x < camera.width and \
           -self.height < screen_y < camera.height:
            surface.blit(self.image, (screen_x, screen_y))

