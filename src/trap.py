"""
Trap class - represents hazards that damage the player on contact
"""

import pygame
from src.sprite_renderer import SpriteRenderer


class Trap:
    """A trap that damages the player on contact"""
    
    def __init__(self, x, y, width, height, damage=10, trap_type="spike"):
        """Initialize a trap
        
        Args:
            x: X position in pixels
            y: Y position in pixels
            width: Width in pixels
            height: Height in pixels
            damage: Damage dealt to player on contact
            trap_type: Type of trap ("spike", "fire", "acid", etc.)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.damage = damage
        self.trap_type = trap_type
        
        # Create rect for collision detection
        self.rect = pygame.Rect(x, y, width, height)

        # Create detailed trap sprite
        self.image = SpriteRenderer.create_trap_sprite(width, height, trap_type)
    
    def draw(self, surface, camera):
        """Draw the trap to the screen with camera offset
        
        Args:
            surface: Pygame surface to draw to
            camera: Camera object for viewport offset
        """
        screen_x, screen_y = camera.apply_point(self.x, self.y)
        
        # Only draw if visible on screen
        if -self.width < screen_x < camera.width and \
           -self.height < screen_y < camera.height:
            surface.blit(self.image, (screen_x, screen_y))

