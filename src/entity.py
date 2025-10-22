"""
Entity base class - shared functionality for all game entities (Player, Enemy, NPC, etc.)
"""

import pygame


class Entity:
    """Base class for all game entities with shared HP, knockback, and movement logic"""

    def __init__(self, x, y, width, height, max_hp=100, knockback_resistance=0.5):
        """Initialize an entity
        
        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            width: Width of the entity
            height: Height of the entity
            max_hp: Maximum HP for this entity
            knockback_resistance: Resistance to knockback (0-1, higher = more resistant)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # HP system
        self.max_hp = max_hp
        self.current_hp = max_hp
        
        # Knockback system
        self.knockback_resistance = knockback_resistance
        self.knockback_velocity = [0, 0]  # Current knockback velocity
        
        # Rect for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Image for rendering
        self.image = pygame.Surface((self.width, self.height))

    def update_position(self):
        """Update rect position based on x, y coordinates"""
        self.rect.x = self.x
        self.rect.y = self.y

    def apply_knockback(self, knockback_power, direction_x, direction_y):
        """Apply knockback force to this entity
        
        Args:
            knockback_power: Base knockback power
            direction_x: X component of knockback direction (normalized)
            direction_y: Y component of knockback direction (normalized)
        """
        # Calculate actual knockback based on resistance
        actual_knockback = knockback_power * (1 - self.knockback_resistance)
        
        # Apply knockback velocity
        self.knockback_velocity[0] = direction_x * actual_knockback
        self.knockback_velocity[1] = direction_y * actual_knockback

    def apply_knockback_friction(self):
        """Apply friction to knockback velocity"""
        if self.knockback_velocity[0] != 0 or self.knockback_velocity[1] != 0:
            # Apply friction
            self.knockback_velocity[0] *= 0.85
            self.knockback_velocity[1] *= 0.85
            
            # Stop knockback if velocity is very small
            if abs(self.knockback_velocity[0]) < 0.1:
                self.knockback_velocity[0] = 0
            if abs(self.knockback_velocity[1]) < 0.1:
                self.knockback_velocity[1] = 0

    def take_damage(self, amount):
        """Take damage and reduce HP
        
        Args:
            amount: Amount of damage to take
        """
        self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount):
        """Heal and increase HP
        
        Args:
            amount: Amount of HP to restore
        """
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def is_alive(self):
        """Check if entity is alive
        
        Returns:
            True if HP > 0, False otherwise
        """
        return self.current_hp > 0

    def _try_move(self, dx, dy, obstacles):
        """Try to move the entity, checking for collisions
        
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

