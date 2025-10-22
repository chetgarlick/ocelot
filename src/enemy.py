"""
Enemy class - represents an enemy that patrols and chases the player
"""

import pygame
import math
from src.config import Config
from src.entity import Entity


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

