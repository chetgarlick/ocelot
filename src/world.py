"""
World class - manages the game world and tilemap
"""

import pygame
from src.config import Config


class World:
    """Game world"""

    def __init__(self):
        """Initialize the world"""
        self.config = Config()
        self.tile_size = 32
        
        # Create a simple tilemap (0 = grass, 1 = water)
        self.width = self.config.SCREEN_WIDTH // self.tile_size
        self.height = self.config.SCREEN_HEIGHT // self.tile_size
        self.tiles = self._generate_tilemap()

    def _generate_tilemap(self):
        """Generate a simple tilemap"""
        # For now, just create a grass world
        tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(0)  # 0 = grass
            tiles.append(row)
        return tiles

    def draw(self, surface):
        """Draw the world to the screen"""
        # Draw tiles
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, 
                                   self.tile_size, self.tile_size)
                if tile == 0:  # Grass
                    pygame.draw.rect(surface, (34, 139, 34), rect)
                elif tile == 1:  # Water
                    pygame.draw.rect(surface, (0, 100, 200), rect)
                
                # Draw grid lines for visibility
                pygame.draw.rect(surface, (50, 150, 50), rect, 1)

