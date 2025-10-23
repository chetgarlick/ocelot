"""
Trap class - represents hazards that damage the player on contact
"""

import pygame


class Trap:
    """A trap that damages the player on contact"""
    
    def __init__(self, x, y, width, height, damage=10, trap_type="spike"):
        """Initialize a trap
        
        Args:
            x: X position in pixels
            y: Y position in pixels
            width: Width in pixels
            height: Height in pixels
            damage: Damage dealt to player on contact
            trap_type: Type of trap ("spike", "fire", "acid", etc.)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.damage = damage
        self.trap_type = trap_type
        
        # Create rect for collision detection
        self.rect = pygame.Rect(x, y, width, height)
        
        # Create image for rendering based on trap type
        self.image = pygame.Surface((width, height))
        
        if trap_type == "spike":
            # Red spikes
            self.image.fill((200, 0, 0))
            # Draw spike pattern
            for i in range(0, width, 10):
                pygame.draw.polygon(self.image, (255, 0, 0), [
                    (i, height),
                    (i + 5, 0),
                    (i + 10, height)
                ])
        elif trap_type == "fire":
            # Orange/yellow fire
            self.image.fill((255, 100, 0))
            # Draw flame pattern
            for i in range(0, width, 15):
                pygame.draw.polygon(self.image, (255, 200, 0), [
                    (i + 5, height),
                    (i + 7, height // 2),
                    (i + 10, height)
                ])
        elif trap_type == "acid":
            # Green acid
            self.image.fill((0, 200, 0))
            # Draw drip pattern
            for i in range(0, width, 12):
                pygame.draw.circle(self.image, (100, 255, 100), (i + 6, height // 2), 3)
        else:
            # Default gray trap
            self.image.fill((100, 100, 100))
    
    def draw(self, surface, camera):
        """Draw the trap to the screen with camera offset
        
        Args:
            surface: Pygame surface to draw to
            camera: Camera object for viewport offset
        """
        screen_x, screen_y = camera.apply_point(self.x, self.y)
        
        # Only draw if visible on screen
        if -self.width < screen_x < camera.width and \
           -self.height < screen_y < camera.height:
            surface.blit(self.image, (screen_x, screen_y))

