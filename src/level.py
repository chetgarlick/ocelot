"""
Level class - base class for game levels/areas
"""

import pygame
from src.config import Config
from src.obstacle import Obstacle


class ExitZone:
    """An exit zone that transitions to another level"""
    
    def __init__(self, x, y, width, height, target_level, spawn_x, spawn_y):
        """Initialize an exit zone
        
        Args:
            x: X position of the exit zone
            y: Y position of the exit zone
            width: Width of the exit zone
            height: Height of the exit zone
            target_level: The level ID to transition to
            spawn_x: X position where player spawns in target level
            spawn_y: Y position where player spawns in target level
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.target_level = target_level
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y


class Level:
    """Base class for game levels"""
    
    def __init__(self, level_id, world_width=2400, world_height=1800):
        """Initialize a level
        
        Args:
            level_id: Unique identifier for this level
            world_width: Width of the level world
            world_height: Height of the level world
        """
        self.config = Config()
        self.level_id = level_id
        self.tile_size = 32
        
        # World dimensions
        self.world_width = world_width
        self.world_height = world_height
        self.width = world_width // self.tile_size
        self.height = world_height // self.tile_size
        
        # Tilemap
        self.tiles = self._generate_tilemap()
        
        # Game objects
        self.obstacles = []  # Collision obstacles
        self.visual_obstacles = []  # Visual-only obstacles (no collision)
        self.coins = []
        self.enemies = []
        self.traps = []  # Hazards that damage the player
        self.boss = None  # Optional boss for this level
        self.exit_zones = []
        
        # Generate level content
        self._generate_obstacles()
        self._generate_coins()
        self._generate_enemies()
        self._generate_traps()
        self._generate_boss()
        self._generate_exits()
    
    def _generate_tilemap(self):
        """Generate the tilemap for this level - override in subclasses"""
        tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(0)  # 0 = grass
            tiles.append(row)
        return tiles
    
    def _generate_obstacles(self):
        """Generate obstacles for this level - override in subclasses"""
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
    
    def _generate_coins(self):
        """Generate coins for this level - override in subclasses"""
        pass
    
    def _generate_enemies(self):
        """Generate enemies for this level - override in subclasses"""
        pass

    def _generate_traps(self):
        """Generate traps for this level - override in subclasses"""
        pass

    def _generate_boss(self):
        """Generate boss for this level - override in subclasses"""
        pass

    def _generate_exits(self):
        """Generate exit zones for this level - override in subclasses"""
        pass
    
    def update(self, player, explosions, loot_items):
        """Update level logic
        
        Args:
            player: Player object
            explosions: List of explosions
            loot_items: List of loot items
            
        Returns:
            Tuple of (target_level_id, spawn_x, spawn_y) if player exited, else None
        """
        # Check if player is in any exit zone
        for exit_zone in self.exit_zones:
            if player.rect.colliderect(exit_zone.rect):
                return (exit_zone.target_level, exit_zone.spawn_x, exit_zone.spawn_y)
        
        return None
    
    def draw(self, surface, camera):
        """Draw the level to the screen
        
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
        
        # Draw visual obstacles (no collision)
        for obstacle in self.visual_obstacles:
            obstacle_rect = pygame.Rect(
                camera.apply_point(obstacle.x, obstacle.y),
                (obstacle.width, obstacle.height)
            )
            # Only draw if visible on screen
            if -obstacle.width < obstacle_rect.x < camera.width and \
               -obstacle.height < obstacle_rect.y < camera.height:
                surface.blit(obstacle.image, obstacle_rect)

        # Draw collision obstacles
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

        # Draw traps
        for trap in self.traps:
            trap.draw(surface, camera)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(surface, camera)

        # Draw boss
        if self.boss:
            self.boss.draw(surface, camera)

        # Draw exit zones (debug - can be removed later)
        for exit_zone in self.exit_zones:
            exit_rect = pygame.Rect(
                camera.apply_point(exit_zone.rect.x, exit_zone.rect.y),
                (exit_zone.rect.width, exit_zone.rect.height)
            )
            if -exit_zone.rect.width < exit_rect.x < camera.width and \
               -exit_zone.rect.height < exit_rect.y < camera.height:
                # Draw semi-transparent exit zone
                surface_copy = surface.copy()
                pygame.draw.rect(surface_copy, (255, 200, 0, 100), exit_rect)
                surface.blit(surface_copy, (0, 0))

