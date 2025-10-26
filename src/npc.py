"""
NPC class - an interactive character that displays dialogue trees when interacted with
"""

import pygame
from src.config import Config
from src.sprite_renderer import SpriteRenderer
from src.dialogue import DialogueTree


class NPC:
    """An NPC that the player can interact with to have conversations"""

    def __init__(self, x, y, name, dialogue_tree):
        """Initialize an NPC
        
        Args:
            x: X position of the NPC
            y: Y position of the NPC
            name: Name of the NPC
            dialogue_tree: DialogueTree object for this NPC's dialogue
        """
        self.config = Config()
        self.x = x
        self.y = y
        self.name = name
        self.dialogue_tree = dialogue_tree
        
        # NPC dimensions
        self.width = 32
        self.height = 48

        # Create NPC sprite (using enemy sprite for now, can be customized)
        self.image = SpriteRenderer.create_enemy_sprite(self.width, self.height, enemy_type="fast")

        # Create rect for collision detection
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Interaction range (how close the player needs to be to interact)
        self.interaction_range = 150  # Increased for easier testing
        
        # Track if dialogue has been started
        self.dialogue_active = False
        
    def draw(self, surface, camera):
        """Draw the NPC to the screen

        Args:
            surface: The pygame surface to draw to
            camera: The camera object for applying offset
        """
        # Apply camera offset
        screen_x, screen_y = camera.apply_point(self.x, self.y)

        # Only draw if visible on screen
        if -self.width < screen_x < camera.width and \
           -self.height < screen_y < camera.height:
            surface.blit(self.image, (screen_x, screen_y))
        
    def can_interact(self, player):
        """Check if the player is close enough to interact with this NPC

        Args:
            player: The player object

        Returns:
            True if the player is within interaction range
        """
        # Calculate distance between player center and NPC center
        player_center_x = player.x + player.width // 2
        player_center_y = player.y + player.height // 2

        npc_center_x = self.x + self.width // 2
        npc_center_y = self.y + self.height // 2

        dx = player_center_x - npc_center_x
        dy = player_center_y - npc_center_y

        distance = (dx**2 + dy**2) ** 0.5

        in_range = distance <= self.interaction_range
        if in_range:
            with open("debug.log", "a") as f:
                f.write(f"DEBUG: Player in range of {self.name}! Distance: {distance:.1f}\n")

        return in_range
    
    def start_dialogue(self):
        """Start the dialogue tree for this NPC
        
        Returns:
            A Dialogue object for the starting node
        """
        self.dialogue_active = True
        return self.dialogue_tree.start()
    
    def end_dialogue(self):
        """End the current dialogue"""
        self.dialogue_active = False

