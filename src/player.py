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
        self.image.fill((255, 100, 100))  # Red color
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, keys):
        """Update player position based on input"""
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        
        # Update rect position
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        """Draw the player to the screen"""
        surface.blit(self.image, self.rect)

