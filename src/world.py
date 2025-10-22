"""
World class - manages the game world and tilemap
"""

import pygame
from src.config import Config
from src.obstacle import Obstacle


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

        # List of obstacles
        self.obstacles = []
        self._generate_obstacles()

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

    def _generate_obstacles(self):
        """Generate obstacles in the world"""
        # Create some grey obstacles scattered around
        # Top wall
        self.obstacles.append(Obstacle(100, 50, 300, 20))

        # Right wall
        self.obstacles.append(Obstacle(600, 100, 20, 250))

        # Bottom wall
        self.obstacles.append(Obstacle(150, 500, 300, 20))

        # Center obstacle
        self.obstacles.append(Obstacle(350, 250, 100, 100))

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

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(surface)

