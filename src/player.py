"""
Player class - represents the player character
"""

import pygame
import math
from src.config import Config
from src.entity import Entity
from src.projectile import Projectile
from src.sprite_renderer import SpriteRenderer


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

        # Create detailed player sprite
        self.image = SpriteRenderer.create_player_sprite(self.width, self.height)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Coin collection
        self.coins_collected = 0

        # Stats system
        self.level = 1
        self.experience = 0
        self.experience_to_level = 100  # XP needed to reach next level

        # Base stats
        self.strength = 1.0  # Multiplier for projectile damage (base 10 damage)
        self.defense = 1.0  # Multiplier for knockback resistance
        self.agility = 1.0  # Multiplier for movement speed

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

        # Rotation
        self.rotation_angle = 0  # Current rotation angle in degrees (0 = pointing right)
        self.last_direction = (1, 0)  # Last movement direction for rotation

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
            movement_x = 0
            movement_y = 0

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self._try_move(0, -self.speed, obstacles)
                movement_y -= 1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self._try_move(0, self.speed, obstacles)
                movement_y += 1
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self._try_move(-self.speed, 0, obstacles)
                movement_x -= 1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self._try_move(self.speed, 0, obstacles)
                movement_x += 1

            # Update rotation based on movement direction
            if movement_x != 0 or movement_y != 0:
                self.last_direction = (movement_x, movement_y)
                self._update_rotation()

        # Update rect position
        self.rect.topleft = (self.x, self.y)

        # Update sprite with current rotation
        self.image = SpriteRenderer.create_player_sprite(self.width, self.height, self.rotation_angle)

    def _update_rotation(self):
        """Update the player's rotation angle based on movement direction"""
        dx, dy = self.last_direction

        # Calculate angle in degrees (0 = right, 90 = down, 180 = left, 270 = up)
        # Using atan2 which returns angle in radians
        angle_rad = math.atan2(dy, dx)
        self.rotation_angle = math.degrees(angle_rad) + 90  # Add 90 to correct orientation

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
            # Create projectile from player center with strength-based damage
            projectile = Projectile(
                self.x + self.width // 2,
                self.y + self.height // 2,
                target_x,
                target_y,
                knockback_power=int(5 * self.strength)  # Scale knockback with strength
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

    def gain_experience(self, amount):
        """Gain experience points and check for level up

        Args:
            amount: Amount of XP to gain
        """
        self.experience += amount

        # Check if leveled up
        while self.experience >= self.experience_to_level:
            self._level_up()

    def _level_up(self):
        """Handle level up - increase stats and reset XP"""
        self.level += 1
        self.experience -= self.experience_to_level

        # Increase XP requirement for next level (scales with level)
        self.experience_to_level = int(100 * (1.1 ** (self.level - 1)))

        # Increase stats on level up
        self.strength += 0.1  # +10% damage per level
        self.defense += 0.05  # +5% knockback resistance per level
        self.agility += 0.05  # +5% movement speed per level

        # Update knockback resistance based on defense stat
        self.knockback_resistance = 0.7 * self.defense

        # Update speed based on agility stat
        self.speed = self.config.PLAYER_SPEED * self.agility

    def draw(self, surface):
        """Draw the player to the screen"""
        surface.blit(self.image, self.rect)

