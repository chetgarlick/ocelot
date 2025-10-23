"""
World class - manages the game world and tilemap
"""

import pygame
import random
from src.config import Config
from src.obstacle import Obstacle
from src.coin import Coin
from src.enemy import Enemy, TankyEnemy, RangedEnemy, FastEnemy


class World:
    """Game world"""

    def __init__(self):
        """Initialize the world"""
        self.config = Config()
        self.tile_size = 32

        # Create a large tilemap (0 = grass, 1 = water)
        self.width = self.config.WORLD_WIDTH // self.tile_size
        self.height = self.config.WORLD_HEIGHT // self.tile_size
        self.world_width = self.config.WORLD_WIDTH
        self.world_height = self.config.WORLD_HEIGHT
        self.tiles = self._generate_tilemap()

        # List of obstacles
        self.obstacles = []
        self._generate_obstacles()

        # List of collectible coins
        self.coins = []
        self._generate_coins()

        # List of enemies
        self.enemies = []
        self._generate_enemies()

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
        # Create world boundaries (invisible walls at edges)
        boundary_thickness = 50

        # Top boundary
        self.obstacles.append(Obstacle(0, -boundary_thickness, self.world_width, boundary_thickness))

        # Bottom boundary
        self.obstacles.append(Obstacle(0, self.world_height, self.world_width, boundary_thickness))

        # Left boundary
        self.obstacles.append(Obstacle(-boundary_thickness, 0, boundary_thickness, self.world_height))

        # Right boundary
        self.obstacles.append(Obstacle(self.world_width, 0, boundary_thickness, self.world_height))

        # Create obstacles scattered throughout the larger world

        # Top-left area
        self.obstacles.append(Obstacle(100, 50, 300, 20))
        self.obstacles.append(Obstacle(600, 100, 20, 250))

        # Top-right area
        self.obstacles.append(Obstacle(1500, 100, 400, 30))
        self.obstacles.append(Obstacle(2000, 200, 100, 150))

        # Middle area
        self.obstacles.append(Obstacle(150, 500, 300, 20))
        self.obstacles.append(Obstacle(350, 250, 100, 100))
        self.obstacles.append(Obstacle(1000, 600, 200, 50))
        self.obstacles.append(Obstacle(1200, 400, 50, 200))

        # Bottom-left area
        self.obstacles.append(Obstacle(200, 1400, 250, 30))
        self.obstacles.append(Obstacle(100, 1200, 30, 300))

        # Bottom-right area
        self.obstacles.append(Obstacle(1800, 1500, 300, 40))
        self.obstacles.append(Obstacle(2100, 1200, 100, 200))

        # Center-right area
        self.obstacles.append(Obstacle(1600, 800, 150, 150))

    def _generate_coins(self):
        """Generate coins scattered throughout the world"""
        # Create coins in various locations
        coin_positions = [
            (200, 200), (400, 150), (700, 300), (900, 250),
            (300, 700), (800, 900), (1200, 700), (1400, 600),
            (500, 1200), (1000, 1400), (1600, 1300), (1900, 1100),
            (2100, 400), (1800, 800), (600, 1600), (1300, 1600),
            (400, 900), (1100, 300), (1700, 500), (2200, 1400),
        ]

        for x, y in coin_positions:
            self.coins.append(Coin(x, y))

    def _generate_enemies(self):
        """Generate enemies scattered throughout the world"""
        # Create enemies in various locations with patrol areas
        # Format: (x, y, patrol_radius, enemy_type)
        enemy_positions = [
            (400, 400, 150, "normal"),      # Normal red enemy
            (1200, 300, 150, "tanky"),      # Tanky blue enemy
            (1600, 1000, 150, "ranged"),    # Ranged purple enemy
            (800, 1400, 150, "fast"),       # Fast green enemy
            (2000, 600, 150, "normal"),     # Another normal enemy
        ]

        for x, y, patrol_radius, enemy_type in enemy_positions:
            if enemy_type == "tanky":
                self.enemies.append(TankyEnemy(x, y, patrol_radius))
            elif enemy_type == "ranged":
                self.enemies.append(RangedEnemy(x, y, patrol_radius))
            elif enemy_type == "fast":
                self.enemies.append(FastEnemy(x, y, patrol_radius))
            else:  # normal
                self.enemies.append(Enemy(x, y, patrol_radius))

    def draw(self, surface, camera):
        """Draw the world to the screen with camera offset

        Args:
            surface: Pygame surface to draw to
            camera: Camera object for viewport offset
        """
        # Draw tiles
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                world_x = x * self.tile_size
                world_y = y * self.tile_size
                screen_x, screen_y = camera.apply_point(world_x, world_y)

                rect = pygame.Rect(screen_x, screen_y,
                                   self.tile_size, self.tile_size)

                # Only draw tiles that are visible on screen
                if -self.tile_size < screen_x < camera.width and \
                   -self.tile_size < screen_y < camera.height:
                    if tile == 0:  # Grass
                        pygame.draw.rect(surface, (34, 139, 34), rect)
                    elif tile == 1:  # Water
                        pygame.draw.rect(surface, (0, 100, 200), rect)

                    # Draw grid lines for visibility
                    pygame.draw.rect(surface, (50, 150, 50), rect, 1)

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(
                camera.apply_point(obstacle.x, obstacle.y),
                (obstacle.width, obstacle.height)
            )
            # Only draw if visible on screen
            if -obstacle.width < obstacle_rect.x < camera.width and \
               -obstacle.height < obstacle_rect.y < camera.height:
                surface.blit(obstacle.image, obstacle_rect)

        # Draw coins
        for coin in self.coins:
            coin.draw(surface, camera)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(surface, camera)

