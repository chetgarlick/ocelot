"""
Starfield - generates and renders a space background with stars
"""

import pygame
import random


class Starfield:
    """Generates and manages a starfield background"""

    def __init__(self, width, height, num_stars=200):
        """Initialize the starfield
        
        Args:
            width: Width of the starfield
            height: Height of the starfield
            num_stars: Number of stars to generate
        """
        self.width = width
        self.height = height
        self.num_stars = num_stars
        self.stars = []
        
        # Generate stars
        self._generate_stars()
        
        # Create starfield surface
        self.surface = pygame.Surface((width, height))
        self._draw_starfield()
    
    def _generate_stars(self):
        """Generate random stars across the starfield"""
        for _ in range(self.num_stars):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            # Brightness (0-255, higher = brighter)
            brightness = random.randint(100, 255)
            # Size (1-3 pixels)
            size = random.randint(1, 3)
            
            self.stars.append({
                'x': x,
                'y': y,
                'brightness': brightness,
                'size': size
            })
    
    def _draw_starfield(self):
        """Draw the starfield to the surface"""
        # Fill with black
        self.surface.fill((0, 0, 0))
        
        # Draw each star
        for star in self.stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(
                self.surface,
                color,
                (int(star['x']), int(star['y'])),
                star['size']
            )
    
    def draw(self, screen, camera):
        """Draw the starfield to the screen with camera offset
        
        Args:
            screen: Pygame surface to draw to
            camera: Camera object for viewport offset
        """
        # Draw the starfield surface
        screen.blit(self.surface, (0, 0))

