"""
Boss class - represents a boss enemy with multiple attack patterns
"""

import pygame
import math
import random
from enum import Enum
from src.config import Config
from src.entity import Entity
from src.projectile import Projectile
from src.loot import HealthPotion, CoinDrop
from src.sprite_renderer import SpriteRenderer


class BossAttackType(Enum):
    """Enum for different boss attack types"""
    PROJECTILE_BURST = "projectile_burst"
    CHARGE = "charge"
    SPIN_ATTACK = "spin_attack"
    SUMMON_PROJECTILES = "summon_projectiles"


class Boss(Entity):
    """A boss enemy with multiple attack patterns and high HP"""
    
    def __init__(self, x, y, name="Boss"):
        """Initialize a boss
        
        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            name: Name of the boss to display
        """
        self.config = Config()
        self.name = name
        
        # Initialize parent Entity class
        super().__init__(
            x, y,
            40, 40,  # width, height
            max_hp=200,
            knockback_resistance=0.5
        )
        
        self.start_x = x
        self.start_y = y
        self.speed = 1.5
        
        # Experience reward
        self.xp_reward = 100  # Large XP reward for defeating boss
        
        # Boss-specific attributes
        self.projectiles = []
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.current_attack = None
        self.attack_sequence = 0
        
        # Attack patterns
        self.attack_patterns = [
            BossAttackType.PROJECTILE_BURST,
            BossAttackType.CHARGE,
            BossAttackType.SPIN_ATTACK,
            BossAttackType.SUMMON_PROJECTILES,
        ]
        
        # Create detailed boss sprite
        self.image = SpriteRenderer.create_boss_sprite(self.width, self.height)
    
    def update(self, player, obstacles):
        """Update boss position and attacks

        Args:
            player: Player object to target
            obstacles: List of obstacles to check collision against
        """
        with open('debug.log', 'a') as f:
            f.write(f"Boss update called. Cooldown: {self.attack_cooldown}\n")

        # Apply knockback velocity with friction
        if self.knockback_velocity[0] != 0 or self.knockback_velocity[1] != 0:
            self._try_move(self.knockback_velocity[0], self.knockback_velocity[1], obstacles)
            self.apply_knockback_friction()

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Update attack timer
        self.attack_timer += 1

        # Calculate distance to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance_to_player = math.sqrt(dx**2 + dy**2)

        # Move towards player
        if distance_to_player > 50:
            direction_x = dx / distance_to_player
            direction_y = dy / distance_to_player
            self._try_move(direction_x * self.speed, direction_y * self.speed, obstacles)

        # Perform attacks
        if self.attack_cooldown <= 0:
            with open('debug.log', 'a') as f:
                f.write(f"Boss attacking! Cooldown: {self.attack_cooldown}, Projectiles: {len(self.projectiles)}\n")
            self._perform_attack(player)

        # Update rect position for collision detection
        self.update_position()
    
    def _perform_attack(self, player):
        """Perform a boss attack

        Args:
            player: Player object to target
        """
        attack_type = self.attack_patterns[self.attack_sequence % len(self.attack_patterns)]
        print(f"Boss performing attack: {attack_type}")

        if attack_type == BossAttackType.PROJECTILE_BURST:
            self._projectile_burst(player)
        elif attack_type == BossAttackType.CHARGE:
            self._charge_attack(player)
        elif attack_type == BossAttackType.SPIN_ATTACK:
            self._spin_attack()
        elif attack_type == BossAttackType.SUMMON_PROJECTILES:
            self._summon_projectiles(player)

        self.attack_sequence += 1
        self.attack_cooldown = 120  # 2 seconds between attacks at 60 FPS
    
    def _projectile_burst(self, player):
        """Fire projectiles in a burst pattern"""
        # Fire 8 projectiles in a circle
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            direction_x = math.cos(angle)
            direction_y = math.sin(angle)

            # Calculate target position based on direction
            target_x = self.x + self.width // 2 + direction_x * 500
            target_y = self.y + self.height // 2 + direction_y * 500

            projectile = Projectile(
                self.x + self.width // 2,
                self.y + self.height // 2,
                target_x,
                target_y,
                speed=4
            )
            projectile.damage = 5  # Set damage as attribute
            projectile.color = (255, 0, 0)  # Red for boss projectiles
            self.projectiles.append(projectile)
    
    def _charge_attack(self, player):
        """Charge towards the player"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            direction_x = dx / distance
            direction_y = dy / distance
            
            # Apply knockback to self to charge forward
            self.apply_knockback(50, direction_x, direction_y)
    
    def _spin_attack(self):
        """Spin and fire projectiles in all directions"""
        # Fire 12 projectiles in a circle
        for i in range(12):
            angle = (i / 12) * 2 * math.pi
            direction_x = math.cos(angle)
            direction_y = math.sin(angle)

            # Calculate target position based on direction
            target_x = self.x + self.width // 2 + direction_x * 500
            target_y = self.y + self.height // 2 + direction_y * 500

            projectile = Projectile(
                self.x + self.width // 2,
                self.y + self.height // 2,
                target_x,
                target_y,
                speed=3
            )
            projectile.damage = 3  # Set damage as attribute
            projectile.color = (255, 0, 0)  # Red for boss projectiles
            self.projectiles.append(projectile)
    
    def _summon_projectiles(self, player):
        """Fire projectiles at the player from multiple angles"""
        # Fire 5 projectiles aimed at player
        for i in range(5):
            dx = player.x - self.x
            dy = player.y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 0:
                # Spread the projectiles slightly
                angle_offset = (i - 2) * 0.3  # Spread across ~90 degrees
                angle = math.atan2(dy, dx) + angle_offset
                direction_x = math.cos(angle)
                direction_y = math.sin(angle)

                # Calculate target position based on direction
                target_x = self.x + self.width // 2 + direction_x * 500
                target_y = self.y + self.height // 2 + direction_y * 500

                projectile = Projectile(
                    self.x + self.width // 2,
                    self.y + self.height // 2,
                    target_x,
                    target_y,
                    speed=5
                )
                projectile.damage = 4  # Set damage as attribute
                projectile.color = (255, 0, 0)  # Red for boss projectiles
                self.projectiles.append(projectile)
    
    def _try_move(self, dx, dy, obstacles):
        """Try to move the boss, checking for collisions

        Args:
            dx: Change in x
            dy: Change in y
            obstacles: List of obstacles to check against
        """
        new_x = self.x + dx
        new_y = self.y + dy

        test_rect = pygame.Rect(new_x, new_y, self.width, self.height)

        for obstacle in obstacles:
            if test_rect.colliderect(obstacle.rect):
                return

        self.x = new_x
        self.y = new_y
        self.update_position()  # Update rect to match new position
    
    def generate_loot(self):
        """Generate loot drops when boss dies
        
        Returns:
            List of loot items dropped by this boss
        """
        loot_drops = []
        
        # Boss always drops health potions and coins
        for _ in range(3):
            loot_drops.append(HealthPotion(
                self.x + self.width // 2,
                self.y + self.height // 2,
                heal_amount=50
            ))
        
        for _ in range(5):
            loot_drops.append(CoinDrop(
                self.x + self.width // 2,
                self.y + self.height // 2,
                coin_value=5
            ))
        
        return loot_drops
    
    def draw(self, surface, camera):
        """Draw the boss to the screen with camera offset
        
        Args:
            surface: Pygame surface to draw to
            camera: Camera object for viewport offset
        """
        screen_x, screen_y = camera.apply_point(self.x, self.y)
        
        # Only draw if visible on screen
        if -self.width < screen_x < camera.width and \
           -self.height < screen_y < camera.height:
            surface.blit(self.image, (screen_x, screen_y))

