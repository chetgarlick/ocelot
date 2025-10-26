"""
Projectile class - represents a projectile fired by the player
"""

import pygame
import math
from src.sprite_renderer import SpriteRenderer


class Projectile:
    """A projectile that travels in a direction and can hit enemies"""

    def __init__(self, x, y, target_x, target_y, speed=8, knockback_power=5):
        """Initialize a projectile

        Args:
            x: Starting x position
            y: Starting y position
            target_x: Target x position (cursor position)
            target_y: Target y position (cursor position)
            speed: Speed of projectile in pixels per frame
            knockback_power: How much knockback this projectile applies
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 5
        self.color = (255, 200, 0)  # Orange/gold color
        self.knockback_power = knockback_power
        
        # Calculate direction to target
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Normalize direction vector
        if distance > 0:
            self.vx = (dx / distance) * speed
            self.vy = (dy / distance) * speed
        else:
            self.vx = 0
            self.vy = 0
        
        # Create rect for collision detection
        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                               self.radius * 2, self.radius * 2)

        # Lifetime in frames (projectile disappears after this many frames)
        self.lifetime = 300  # 5 seconds at 60 FPS
        self.age = 0

        # Damage dealt by this projectile (can be overridden)
        self.damage = 5  # Default damage

    def update(self):
        """Update projectile position"""
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        
        # Update rect position
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def is_alive(self):
        """Check if projectile is still active
        
        Returns:
            True if projectile hasn't exceeded lifetime
        """
        return self.age < self.lifetime

    def draw(self, surface, camera=None):
        """Draw the projectile to the screen

        Args:
            surface: Pygame surface to draw to
            camera: Camera object for offset (optional)
        """
        if camera:
            # Apply camera offset
            screen_x = self.x - camera.x
            screen_y = self.y - camera.y
        else:
            screen_x = self.x
            screen_y = self.y

        # Only draw if on screen
        if -10 < screen_x < surface.get_width() + 10 and \
           -10 < screen_y < surface.get_height() + 10:
            # Create and draw detailed projectile sprite
            sprite = SpriteRenderer.create_projectile_sprite(self.radius, self.color)
            surface.blit(sprite, (int(screen_x - self.radius), int(screen_y - self.radius)))

