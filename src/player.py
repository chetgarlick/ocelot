"""
Player class - represents the player character
"""

import pygame
from src.config import Config


class Player:
    """Player character"""

    def __init__(self, x, y):
        """Initialize the player"""
        self.config = Config()
        self.x = x
        self.y = y
        self.width = self.config.PLAYER_SIZE
        self.height = self.config.PLAYER_SIZE
        self.speed = self.config.PLAYER_SPEED
        
        # Create a simple colored rectangle for the player
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((100, 149, 237))  # Blue color (cornflower blue)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, keys, obstacles=None):
        """Update player position based on input

        Args:
            keys: Pygame key states
            obstacles: List of obstacles to check collision against
        """
        if obstacles is None:
            obstacles = []

        # Handle movement with collision detection
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

    def draw(self, surface):
        """Draw the player to the screen"""
        surface.blit(self.image, self.rect)

