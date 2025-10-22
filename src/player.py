"""
Player class - represents the player character
"""

import pygame
import math
from src.config import Config
from src.entity import Entity
from src.projectile import Projectile


class Player(Entity):
    """Player character"""

    def __init__(self, x, y):
        """Initialize the player"""
        self.config = Config()

        # Initialize parent Entity class
        super().__init__(
            x, y,
            self.config.PLAYER_SIZE,
            self.config.PLAYER_SIZE,
            max_hp=100,
            knockback_resistance=0.7
        )

        self.speed = self.config.PLAYER_SPEED

        # Create a simple colored rectangle for the player
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((100, 149, 237))  # Blue color (cornflower blue)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Coin collection
        self.coins_collected = 0

        # Combat
        self.projectiles = []
        self.attack_cooldown = 0  # Frames until next attack is allowed

        # Dash mechanics
        self.is_dashing = False
        self.dash_duration = 15  # Frames the dash lasts
        self.dash_timer = 0  # Current dash frame
        self.dash_speed = 12  # Speed during dash (pixels per frame)
        self.dash_cooldown = 0  # Frames until next dash is allowed
        self.dash_max_cooldown = 60  # 1 second cooldown at 60 FPS
        self.dash_direction = (0, 0)  # Direction of dash (normalized)
        self.invincibility_timer = 0  # Frames of invincibility after dash starts
        self.invincibility_duration = 20  # 0.33 seconds of invincibility

    def update(self, keys, obstacles=None):
        """Update player position based on input

        Args:
            keys: Pygame key states
            obstacles: List of obstacles to check collision against
        """
        if obstacles is None:
            obstacles = []

        # Update cooldowns
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        # Apply knockback velocity with friction
        if self.knockback_velocity[0] != 0 or self.knockback_velocity[1] != 0:
            self._try_move(self.knockback_velocity[0], self.knockback_velocity[1], obstacles)
            self.apply_knockback_friction()

        # Handle dash movement
        if self.is_dashing:
            self.dash_timer += 1
            # Move in dash direction
            dx = self.dash_direction[0] * self.dash_speed
            dy = self.dash_direction[1] * self.dash_speed
            self._try_move(dx, dy, obstacles)

            # End dash when duration is over
            if self.dash_timer >= self.dash_duration:
                self.is_dashing = False
                self.dash_timer = 0
        else:
            # Handle normal movement with collision detection
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self._try_move(0, -self.speed, obstacles)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self._try_move(0, self.speed, obstacles)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self._try_move(-self.speed, 0, obstacles)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self._try_move(self.speed, 0, obstacles)

        # Update rect position
        self.rect.topleft = (self.x, self.y)

    def _try_move(self, dx, dy, obstacles):
        """Try to move the player, checking for collisions

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

    def collect_coin(self):
        """Collect a coin and increment the counter"""
        self.coins_collected += 1

    def start_dash(self, direction_x, direction_y):
        """Start a dash in the given direction

        Args:
            direction_x: X component of direction (-1, 0, or 1)
            direction_y: Y component of direction (-1, 0, or 1)
        """
        if self.dash_cooldown <= 0 and not self.is_dashing:
            self.is_dashing = True
            self.dash_timer = 0
            self.invincibility_timer = self.invincibility_duration
            self.dash_cooldown = self.dash_max_cooldown

            # Normalize direction
            magnitude = math.sqrt(direction_x**2 + direction_y**2)
            if magnitude > 0:
                self.dash_direction = (direction_x / magnitude, direction_y / magnitude)
            else:
                # If no direction, dash forward (right)
                self.dash_direction = (1, 0)

    def is_invincible(self):
        """Check if player is currently invincible

        Returns:
            True if player is invincible
        """
        return self.invincibility_timer > 0

    def fire_projectile(self, target_x, target_y):
        """Fire a projectile towards the target position

        Args:
            target_x: Target x position (usually cursor)
            target_y: Target y position (usually cursor)
        """
        if self.attack_cooldown <= 0:
            # Create projectile from player center
            projectile = Projectile(
                self.x + self.width // 2,
                self.y + self.height // 2,
                target_x,
                target_y
            )
            self.projectiles.append(projectile)
            self.attack_cooldown = 15  # 0.25 second cooldown at 60 FPS

    def update_projectiles(self):
        """Update all projectiles and remove dead ones"""
        # Update cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.is_alive():
                self.projectiles.remove(projectile)

    def draw(self, surface):
        """Draw the player to the screen"""
        surface.blit(self.image, self.rect)

