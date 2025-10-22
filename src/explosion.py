"""
Explosion class - visual effect when enemies die
"""

import pygame


class Explosion:
    """A simple explosion particle effect"""

    def __init__(self, x, y, lifetime=30):
        """Initialize an explosion
        
        Args:
            x: X position
            y: Y position
            lifetime: How long the explosion lasts in frames
        """
        self.x = x
        self.y = y
        self.lifetime = lifetime
        self.age = 0
        self.max_radius = 40

    def update(self):
        """Update explosion"""
        self.age += 1

    def is_alive(self):
        """Check if explosion is still active
        
        Returns:
            True if explosion hasn't finished
        """
        return self.age < self.lifetime

    def draw(self, surface, camera=None):
        """Draw the explosion to the screen
        
        Args:
            surface: Pygame surface to draw to
            camera: Camera object for offset (optional)
        """
        # Calculate progress (0 to 1)
        progress = self.age / self.lifetime
        
        # Radius shrinks over time
        radius = int(self.max_radius * (1 - progress))
        
        # Opacity fades over time
        alpha = int(255 * (1 - progress))
        
        if camera:
            screen_x = self.x - camera.x
            screen_y = self.y - camera.y
        else:
            screen_x = self.x
            screen_y = self.y
        
        # Only draw if on screen
        if -50 < screen_x < surface.get_width() + 50 and \
           -50 < screen_y < surface.get_height() + 50:
            
            if radius > 0:
                # Create a surface for the explosion with alpha
                explosion_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                
                # Draw outer ring (orange/red)
                pygame.draw.circle(explosion_surface, (255, 100, 0, alpha), 
                                 (radius, radius), radius)
                
                # Draw inner ring (yellow)
                inner_radius = int(radius * 0.6)
                if inner_radius > 0:
                    pygame.draw.circle(explosion_surface, (255, 200, 0, alpha), 
                                     (radius, radius), inner_radius)
                
                # Blit to screen
                surface.blit(explosion_surface, 
                           (int(screen_x) - radius, int(screen_y) - radius))

