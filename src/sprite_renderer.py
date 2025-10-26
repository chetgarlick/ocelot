"""
Sprite Renderer - creates detailed sprite graphics for game entities
"""

import pygame
import math


class SpriteRenderer:
    """Utility class for rendering detailed sprites"""

    @staticmethod
    def create_player_sprite(width, height, rotation=0):
        """Create a sci-fi player spaceship sprite

        Args:
            width: Sprite width
            height: Sprite height
            rotation: Rotation angle in degrees (0 = pointing right)

        Returns:
            Pygame Surface with player spaceship sprite
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Main hull (cyan/light blue spaceship body)
        pygame.draw.polygon(surface, (0, 255, 255), [
            (width // 2, 2),           # Nose cone
            (width - 3, height - 4),   # Right wing
            (width // 2 + 2, height - 2),  # Right engine
            (width // 2 - 2, height - 2),  # Left engine
            (3, height - 4)            # Left wing
        ])

        # Cockpit window (bright white circle)
        pygame.draw.circle(surface, (255, 255, 255), (width // 2, 8), 3)
        pygame.draw.circle(surface, (0, 100, 255), (width // 2, 8), 2)

        # Engine glow (left)
        pygame.draw.circle(surface, (255, 100, 0), (width // 2 - 3, height - 1), 2)
        pygame.draw.circle(surface, (255, 200, 0), (width // 2 - 3, height - 1), 1)

        # Engine glow (right)
        pygame.draw.circle(surface, (255, 100, 0), (width // 2 + 3, height - 1), 2)
        pygame.draw.circle(surface, (255, 200, 0), (width // 2 + 3, height - 1), 1)

        # Wing details (small lines)
        pygame.draw.line(surface, (100, 200, 255), (3, height - 4), (width // 2 - 2, height - 2), 1)
        pygame.draw.line(surface, (100, 200, 255), (width - 3, height - 4), (width // 2 + 2, height - 2), 1)

        # Apply rotation if needed
        if rotation != 0:
            surface = pygame.transform.rotate(surface, -rotation)

        return surface

    @staticmethod
    def create_enemy_sprite(width, height, enemy_type="normal"):
        """Create a sci-fi enemy spaceship sprite

        Args:
            width: Sprite width
            height: Sprite height
            enemy_type: Type of enemy (normal, tanky, ranged, fast)

        Returns:
            Pygame Surface with enemy spaceship sprite
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        if enemy_type == "tanky":
            # Tanky enemy - heavy armored destroyer
            pygame.draw.polygon(surface, (200, 0, 0), [
                (width // 2, 2),           # Nose
                (width - 2, height // 2),  # Right side
                (width - 3, height - 2),   # Right engine
                (width // 2, height - 1),  # Center
                (3, height - 2),           # Left engine
                (2, height // 2)           # Left side
            ])
            # Heavy armor plating
            pygame.draw.line(surface, (100, 0, 0), (2, height // 2), (width - 2, height // 2), 1)
            # Weapon turret
            pygame.draw.circle(surface, (255, 100, 0), (width // 2, height // 2), 2)

        elif enemy_type == "ranged":
            # Ranged enemy - sleek fighter with weapons
            pygame.draw.polygon(surface, (255, 150, 0), [
                (width // 2, 1),           # Nose
                (width - 2, height - 3),   # Right wing
                (width // 2 + 1, height - 1),  # Right engine
                (width // 2 - 1, height - 1),  # Left engine
                (2, height - 3)            # Left wing
            ])
            # Weapon pods
            pygame.draw.circle(surface, (255, 200, 0), (3, height - 3), 1)
            pygame.draw.circle(surface, (255, 200, 0), (width - 3, height - 3), 1)

        elif enemy_type == "fast":
            # Fast enemy - sleek interceptor
            pygame.draw.polygon(surface, (0, 255, 100), [
                (width // 2, 1),           # Nose
                (width - 1, height - 2),   # Right wing
                (width // 2 + 1, height - 1),  # Right engine
                (width // 2 - 1, height - 1),  # Left engine
                (1, height - 2)            # Left wing
            ])
            # Engine glow
            pygame.draw.circle(surface, (0, 255, 150), (width // 2 - 1, height - 1), 1)
            pygame.draw.circle(surface, (0, 255, 150), (width // 2 + 1, height - 1), 1)

        else:  # normal
            # Normal enemy - standard fighter
            pygame.draw.polygon(surface, (255, 0, 0), [
                (width // 2, 2),           # Nose
                (width - 2, height - 3),   # Right wing
                (width // 2 + 1, height - 1),  # Right engine
                (width // 2 - 1, height - 1),  # Left engine
                (2, height - 3)            # Left wing
            ])
            # Cockpit
            pygame.draw.circle(surface, (255, 100, 100), (width // 2, 5), 1)

        return surface

    @staticmethod
    def create_boss_sprite(width, height):
        """Create a sci-fi boss spaceship sprite (massive battleship)

        Args:
            width: Sprite width
            height: Sprite height

        Returns:
            Pygame Surface with boss spaceship sprite
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Main hull (purple/magenta battleship)
        pygame.draw.polygon(surface, (200, 0, 255), [
            (width // 2, 2),           # Nose
            (width - 3, height // 3),  # Right upper
            (width - 2, height - 4),   # Right lower
            (width // 2 + 2, height - 2),  # Right engine
            (width // 2 - 2, height - 2),  # Left engine
            (2, height - 4),           # Left lower
            (3, height // 3)           # Left upper
        ])

        # Heavy armor plating (dark purple lines)
        pygame.draw.line(surface, (150, 0, 200), (3, height // 3), (width - 3, height // 3), 2)
        pygame.draw.line(surface, (150, 0, 200), (2, height - 4), (width - 2, height - 4), 2)

        # Main weapon turrets (bright yellow)
        pygame.draw.circle(surface, (255, 255, 0), (width // 2 - 5, height // 2), 2)
        pygame.draw.circle(surface, (255, 255, 0), (width // 2 + 5, height // 2), 2)
        pygame.draw.circle(surface, (255, 200, 0), (width // 2 - 5, height // 2), 1)
        pygame.draw.circle(surface, (255, 200, 0), (width // 2 + 5, height // 2), 1)

        # Central reactor (bright cyan)
        pygame.draw.circle(surface, (0, 255, 255), (width // 2, height // 2), 2)
        pygame.draw.circle(surface, (100, 255, 255), (width // 2, height // 2), 1)

        # Engine glow (red/orange)
        pygame.draw.circle(surface, (255, 100, 0), (width // 2 - 2, height - 1), 2)
        pygame.draw.circle(surface, (255, 150, 0), (width // 2 - 2, height - 1), 1)
        pygame.draw.circle(surface, (255, 100, 0), (width // 2 + 2, height - 1), 2)
        pygame.draw.circle(surface, (255, 150, 0), (width // 2 + 2, height - 1), 1)

        return surface

    @staticmethod
    def create_projectile_sprite(radius, color):
        """Create a sci-fi energy projectile sprite

        Args:
            radius: Projectile radius
            color: RGB color tuple

        Returns:
            Pygame Surface with projectile sprite
        """
        size = radius * 2
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        # Outer energy glow
        glow_color = tuple(min(c + 100, 255) for c in color)
        pygame.draw.circle(surface, glow_color, (radius, radius), radius + 1)

        # Main energy ball
        pygame.draw.circle(surface, color, (radius, radius), radius)

        # Inner bright core
        core_color = tuple(min(c + 150, 255) for c in color)
        pygame.draw.circle(surface, core_color, (radius, radius), max(1, radius // 2))

        # Bright center point
        pygame.draw.circle(surface, (255, 255, 255), (radius, radius), max(1, radius // 3))

        return surface

    @staticmethod
    def create_coin_sprite(width, height):
        """Create a sci-fi energy crystal sprite

        Args:
            width: Sprite width
            height: Sprite height

        Returns:
            Pygame Surface with energy crystal sprite
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Crystal shape (diamond)
        pygame.draw.polygon(surface, (0, 255, 200), [
            (width // 2, 1),           # Top
            (width - 2, height // 2),  # Right
            (width // 2, height - 1),  # Bottom
            (2, height // 2)           # Left
        ])

        # Inner glow
        pygame.draw.polygon(surface, (100, 255, 200), [
            (width // 2, 3),
            (width - 3, height // 2),
            (width // 2, height - 3),
            (3, height // 2)
        ])

        # Center bright point
        pygame.draw.circle(surface, (255, 255, 255), (width // 2, height // 2), 1)

        return surface

    @staticmethod
    def create_trap_sprite(width, height, trap_type="spike"):
        """Create a sci-fi hazard sprite

        Args:
            width: Sprite width
            height: Sprite height
            trap_type: Type of trap (spike, fire, acid)

        Returns:
            Pygame Surface with hazard sprite
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        if trap_type == "spike":
            # Laser grid trap - cyan energy grid
            pygame.draw.rect(surface, (0, 255, 255), (0, 0, width, height), 1)
            pygame.draw.line(surface, (0, 255, 255), (0, height // 2), (width, height // 2), 1)
            pygame.draw.line(surface, (0, 255, 255), (width // 2, 0), (width // 2, height), 1)
            # Danger corners
            pygame.draw.circle(surface, (255, 0, 0), (0, 0), 2)
            pygame.draw.circle(surface, (255, 0, 0), (width, height), 2)

        elif trap_type == "fire":
            # Plasma field - orange/red energy
            pygame.draw.rect(surface, (255, 100, 0), (0, 0, width, height))
            pygame.draw.rect(surface, (255, 200, 0), (2, 2, width - 4, height - 4))
            # Plasma bolts
            pygame.draw.circle(surface, (255, 255, 0), (width // 3, height // 3), 2)
            pygame.draw.circle(surface, (255, 255, 0), (2 * width // 3, 2 * height // 3), 2)

        elif trap_type == "acid":
            # Radiation field - green/yellow energy
            pygame.draw.rect(surface, (0, 200, 0), (0, 0, width, height))
            pygame.draw.rect(surface, (100, 255, 0), (2, 2, width - 4, height - 4))
            # Radiation symbol (X pattern)
            pygame.draw.line(surface, (255, 255, 0), (0, 0), (width, height), 1)
            pygame.draw.line(surface, (255, 255, 0), (width, 0), (0, height), 1)

        return surface

    @staticmethod
    def create_signpost_sprite(width, height):
        """Create a sci-fi data beacon sprite

        Args:
            width: Sprite width
            height: Sprite height

        Returns:
            Pygame Surface with data beacon sprite
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Antenna post (metallic gray)
        pygame.draw.rect(surface, (150, 150, 150), (width // 2 - 1, height // 2, 2, height // 2))

        # Data beacon (cyan square)
        pygame.draw.rect(surface, (0, 255, 255), (4, 4, width - 8, 16))

        # Beacon border (bright cyan)
        pygame.draw.rect(surface, (100, 255, 255), (4, 4, width - 8, 16), 1)

        # Scanning lines (animated effect)
        pygame.draw.line(surface, (0, 255, 255), (6, 10), (width - 6, 10), 1)
        pygame.draw.line(surface, (0, 255, 255), (6, 14), (width - 6, 14), 1)

        # Transmitter (bright point)
        pygame.draw.circle(surface, (255, 255, 0), (width // 2, height // 2), 1)

        return surface

