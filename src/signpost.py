"""
Signpost class - an interactive object that displays dialogue when interacted with
"""

import pygame
from src.config import Config
from src.sprite_renderer import SpriteRenderer


class Signpost:
    """A signpost that the player can interact with to read text"""

    def __init__(self, x, y, text):
        """Initialize a signpost
        
        Args:
            x: X position of the signpost
            y: Y position of the signpost
            text: The text to display when interacted with
        """
        self.config = Config()
        self.x = x
        self.y = y
        self.text = text
        
        # Signpost dimensions
        self.width = 32
        self.height = 48

        # Create detailed signpost sprite
        self.image = SpriteRenderer.create_signpost_sprite(self.width, self.height)

        # Create rect for collision detection
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Interaction range (how close the player needs to be to interact)
        self.interaction_range = 50
        
    def draw(self, surface, camera):
        """Draw the signpost to the screen
        
        Args:
            surface: The pygame surface to draw to
            camera: The camera object for applying offset
        """
        # Apply camera offset
        rect = camera.apply(self)
        surface.blit(self.image, rect)
        
    def can_interact(self, player):
        """Check if the player is close enough to interact with this signpost
        
        Args:
            player: The player object
            
        Returns:
            True if the player is within interaction range
        """
        # Calculate distance between player center and signpost center
        player_center_x = player.x + player.width // 2
        player_center_y = player.y + player.height // 2
        
        signpost_center_x = self.x + self.width // 2
        signpost_center_y = self.y + self.height // 2
        
        dx = player_center_x - signpost_center_x
        dy = player_center_y - signpost_center_y
        
        distance = (dx**2 + dy**2) ** 0.5
        
        return distance <= self.interaction_range
    
    def get_dialogue_text(self):
        """Get the text to display in the dialogue box
        
        Returns:
            The text associated with this signpost
        """
        return self.text

