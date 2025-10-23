"""
Loot system - items dropped by enemies
"""

import pygame
import random


class Loot:
    """Base class for all loot items"""

    def __init__(self, x, y, loot_type="generic"):
        """Initialize a loot item
        
        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            loot_type: Type of loot (used for identification)
        """
        self.x = x
        self.y = y
        self.loot_type = loot_type
        self.width = 16
        self.height = 16
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Visual properties
        self.image = pygame.Surface((self.width, self.height))
        self.color = (255, 255, 255)  # Default white
        self.image.fill(self.color)
        
        # Lifetime (frames before disappearing)
        self.lifetime = 600  # 10 seconds at 60 FPS
        self.age = 0

    def update(self):
        """Update loot (age and lifetime)"""
        self.age += 1
        self.rect.x = self.x
        self.rect.y = self.y

    def is_alive(self):
        """Check if loot is still valid
        
        Returns:
            True if loot hasn't expired
        """
        return self.age < self.lifetime

    def apply_effect(self, player):
        """Apply the loot's effect to the player
        
        Args:
            player: Player object to apply effect to
        """
        pass  # Override in subclasses

    def draw(self, surface, camera):
        """Draw the loot to the screen with camera offset
        
        Args:
            surface: Pygame surface to draw to
            camera: Camera object for viewport offset
        """
        screen_x, screen_y = camera.apply_point(self.x, self.y)
        
        # Only draw if visible on screen
        if -self.width < screen_x < camera.width and \
           -self.height < screen_y < camera.height:
            surface.blit(self.image, (screen_x, screen_y))


class HealthPotion(Loot):
    """Health potion that restores player HP"""

    def __init__(self, x, y, heal_amount=25):
        """Initialize a health potion
        
        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            heal_amount: Amount of HP to restore
        """
        super().__init__(x, y, loot_type="health_potion")
        self.heal_amount = heal_amount
        
        # Red color for health potion
        self.color = (255, 0, 0)
        self.image.fill(self.color)

    def apply_effect(self, player):
        """Heal the player
        
        Args:
            player: Player object to heal
        """
        player.heal(self.heal_amount)


class CoinDrop(Loot):
    """Coin drop that adds to player's coin collection"""

    def __init__(self, x, y, coin_value=1):
        """Initialize a coin drop
        
        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            coin_value: Number of coins to add
        """
        super().__init__(x, y, loot_type="coin")
        self.coin_value = coin_value
        
        # Yellow color for coins
        self.color = (255, 255, 0)
        self.image.fill(self.color)

    def apply_effect(self, player):
        """Add coins to player's collection
        
        Args:
            player: Player object to add coins to
        """
        player.coins_collected += self.coin_value

