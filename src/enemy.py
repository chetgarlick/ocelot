"""
Enemy class - represents an enemy that patrols and chases the player
"""

import pygame
import math
import random
from enum import Enum
from src.config import Config
from src.entity import Entity
from src.loot import HealthPotion, CoinDrop


class EnemyType(Enum):
    """Enum for different enemy types"""
    NORMAL = "normal"
    TANKY = "tanky"
    RANGED = "ranged"
    FAST = "fast"


class Enemy(Entity):
    """An enemy that patrols an area and chases the player when nearby"""

    def __init__(self, x, y, patrol_radius=150):
        """Initialize an enemy

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            patrol_radius: Radius of the patrol area around the starting position
        """
        self.config = Config()

        # Initialize parent Entity class
        super().__init__(
            x, y,
            24, 24,  # width, height
            max_hp=30,
            knockback_resistance=0.3
        )

        self.start_x = x  # Starting position for patrol
        self.start_y = y
        self.speed = 2
        self.patrol_radius = patrol_radius
        self.chase_radius = 200  # Distance at which enemy starts chasing player

        # Experience reward
        self.xp_reward = 10  # Base XP for defeating this enemy

        # State
        self.is_chasing = False
        self.patrol_direction = 1  # 1 for right, -1 for left
        self.patrol_timer = 0
        self.patrol_change_interval = 60  # Frames before changing direction

        # Create a simple colored rectangle for the enemy (red)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))  # Red color

    def update(self, player, obstacles):
        """Update enemy position based on patrol or chase behavior

        Args:
            player: Player object to chase or detect
            obstacles: List of obstacles to check collision against
        """
        # Apply knockback velocity with friction
        if self.knockback_velocity[0] != 0 or self.knockback_velocity[1] != 0:
            self._try_move(self.knockback_velocity[0], self.knockback_velocity[1], obstacles)
            self.apply_knockback_friction()

        # Calculate distance to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance_to_player = math.sqrt(dx**2 + dy**2)

        # Check if should chase
        if distance_to_player < self.chase_radius:
            self.is_chasing = True
        elif distance_to_player > self.chase_radius + 100:  # Hysteresis to prevent flickering
            self.is_chasing = False

        if self.is_chasing:
            self._chase_player(player, obstacles, dx, dy, distance_to_player)
        else:
            self._patrol(obstacles)

        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y

    def _patrol(self, obstacles):
        """Patrol back and forth in the patrol area
        
        Args:
            obstacles: List of obstacles to check collision against
        """
        self.patrol_timer += 1
        
        # Change direction periodically or at patrol boundaries
        if self.patrol_timer >= self.patrol_change_interval:
            self.patrol_timer = 0
            self.patrol_direction *= -1
        
        # Move in patrol direction
        dx = self.patrol_direction * self.speed
        self._try_move(dx, 0, obstacles)

    def _chase_player(self, player, obstacles, dx, dy, distance):
        """Chase the player
        
        Args:
            player: Player object to chase
            obstacles: List of obstacles to check collision against
            dx: X distance to player
            dy: Y distance to player
            distance: Total distance to player
        """
        # Normalize direction
        if distance > 0:
            dir_x = dx / distance
            dir_y = dy / distance
        else:
            dir_x = 0
            dir_y = 0
        
        # Move towards player
        move_x = dir_x * self.speed
        move_y = dir_y * self.speed
        
        # Try to move (with simple pathfinding - try x and y separately)
        self._try_move(move_x, 0, obstacles)
        self._try_move(0, move_y, obstacles)

    def _try_move(self, dx, dy, obstacles):
        """Try to move the enemy, checking for collisions

        Args:
            dx: Change in x
            dy: Change in y
            obstacles: List of obstacles to check against
        """
        # Calculate new position
        new_x = self.x + dx
        new_y = self.y + dy

        # Create a test rect at the new position
        test_rect = pygame.Rect(new_x, new_y, self.width, self.height)

        # Check collision with obstacles
        for obstacle in obstacles:
            if test_rect.colliderect(obstacle.rect):
                # Collision detected, don't move
                return

        # No collision, update position
        self.x = new_x
        self.y = new_y

    def generate_loot(self):
        """Generate loot drops when enemy dies

        Returns:
            List of loot items dropped by this enemy
        """
        loot_drops = []

        # 40% chance to drop a health potion
        if random.random() < 0.4:
            loot_drops.append(HealthPotion(
                self.x + self.width // 2,
                self.y + self.height // 2,
                heal_amount=25
            ))

        # 60% chance to drop a coin
        if random.random() < 0.6:
            loot_drops.append(CoinDrop(
                self.x + self.width // 2,
                self.y + self.height // 2,
                coin_value=1
            ))

        return loot_drops

    def draw(self, surface, camera):
        """Draw the enemy to the screen with camera offset
        
        Args:
            surface: Pygame surface to draw to
            camera: Camera object for viewport offset
        """
        screen_x, screen_y = camera.apply_point(self.x, self.y)
        
        # Only draw if visible on screen
        if -self.width < screen_x < camera.width and \
           -self.height < screen_y < camera.height:
            surface.blit(self.image, (screen_x, screen_y))
            
            # Draw a circle around the enemy when chasing (for visibility)
            if self.is_chasing:
                pygame.draw.circle(
                    surface,
                    (255, 100, 100),  # Light red
                    (int(screen_x + self.width // 2), int(screen_y + self.height // 2)),
                    self.chase_radius,
                    1  # Outline only
                )


class TankyEnemy(Enemy):
    """A tanky enemy with high HP, slow speed, and high knockback resistance"""

    def __init__(self, x, y, patrol_radius=150):
        """Initialize a tanky enemy

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            patrol_radius: Radius of the patrol area around the starting position
        """
        super().__init__(x, y, patrol_radius)

        # Override stats for tanky behavior
        self.max_hp = 60  # Double the normal HP
        self.current_hp = self.max_hp
        self.speed = 1  # Half the normal speed
        self.knockback_resistance = 0.6  # Much more resistant to knockback
        self.width = 32  # Larger size
        self.height = 32

        # Recreate image with larger size and different color (blue)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 100, 255))  # Blue color

        # Update rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Higher XP reward for tanky enemies
        self.xp_reward = 25


class RangedEnemy(Enemy):
    """A ranged enemy that shoots projectiles at the player"""

    def __init__(self, x, y, patrol_radius=150):
        """Initialize a ranged enemy

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            patrol_radius: Radius of the patrol area around the starting position
        """
        super().__init__(x, y, patrol_radius)

        # Override stats for ranged behavior
        self.max_hp = 20  # Lower HP than normal
        self.current_hp = self.max_hp
        self.speed = 1.5  # Slightly slower
        self.knockback_resistance = 0.2  # Less resistant to knockback

        # Ranged-specific properties
        self.projectiles = []
        self.attack_cooldown = 0
        self.attack_cooldown_max = 120  # Fire every 2 seconds
        self.attack_range = 250  # Range at which to start attacking

        # Recreate image with different color (purple)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((200, 0, 200))  # Purple color

        # Higher XP reward for ranged enemies
        self.xp_reward = 20

    def update(self, player, obstacles):
        """Update ranged enemy with attack behavior

        Args:
            player: Player object to chase or attack
            obstacles: List of obstacles to check collision against
        """
        # Call parent update for movement
        super().update(player, obstacles)

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Check if player is in attack range
        dx = player.x - self.x
        dy = player.y - self.y
        distance_to_player = math.sqrt(dx**2 + dy**2)

        if distance_to_player < self.attack_range and self.attack_cooldown == 0:
            self._fire_at_player(player)
            self.attack_cooldown = self.attack_cooldown_max

    def _fire_at_player(self, player):
        """Fire a projectile at the player

        Args:
            player: Player object to target
        """
        from src.projectile import Projectile

        # Calculate direction to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            # Normalize direction
            target_x = self.x + (dx / distance) * 500  # Fire in direction of player
            target_y = self.y + (dy / distance) * 500
        else:
            target_x = self.x + 500
            target_y = self.y

        # Create projectile (orange color for enemy projectiles)
        projectile = Projectile(
            self.x + self.width // 2,
            self.y + self.height // 2,
            target_x,
            target_y,
            speed=6,
            knockback_power=3
        )
        self.projectiles.append(projectile)


class FastEnemy(Enemy):
    """A fast enemy with low HP and aggressive behavior"""

    def __init__(self, x, y, patrol_radius=150):
        """Initialize a fast enemy

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            patrol_radius: Radius of the patrol area around the starting position
        """
        super().__init__(x, y, patrol_radius)

        # Override stats for fast behavior
        self.max_hp = 15  # Lower HP than normal
        self.current_hp = self.max_hp
        self.speed = 4  # Double the normal speed
        self.knockback_resistance = 0.1  # Very susceptible to knockback
        self.chase_radius = 300  # Chases from farther away

        # Smaller size
        self.width = 16
        self.height = 16

        # Recreate image with smaller size and different color (green)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 255, 0))  # Green color

        # Update rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Lower XP reward for fast enemies (easier to defeat)
        self.xp_reward = 15

