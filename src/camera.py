"""
Camera class - handles the viewport that follows the player
"""

import pygame


class Camera:
    """Camera that follows the player and defines the viewport"""

    def __init__(self, width, height, world_width, world_height):
        """Initialize the camera
        
        Args:
            width: Camera/screen width in pixels
            height: Camera/screen height in pixels
            world_width: Total world width in pixels
            world_height: Total world height in pixels
        """
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        
        # Camera position (top-left corner)
        self.x = 0
        self.y = 0

    def update(self, target):
        """Update camera position to follow target (player)
        
        Args:
            target: Object with x, y, width, height attributes (the player)
        """
        # Center camera on target
        self.x = target.x + target.width // 2 - self.width // 2
        self.y = target.y + target.height // 2 - self.height // 2
        
        # Clamp camera to world bounds
        self.x = max(0, min(self.x, self.world_width - self.width))
        self.y = max(0, min(self.y, self.world_height - self.height))

    def apply(self, entity):
        """Apply camera offset to an entity's rect
        
        Args:
            entity: Object with a rect attribute
            
        Returns:
            A new rect with camera offset applied
        """
        return entity.rect.move(-self.x, -self.y)

    def apply_point(self, x, y):
        """Apply camera offset to a point
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Tuple of (x - camera.x, y - camera.y)
        """
        return (x - self.x, y - self.y)

