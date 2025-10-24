"""
Dialogue system for displaying text to the player
"""

import pygame
from src.config import Config


class Dialogue:
    """Represents a dialogue box that displays text to the player"""

    def __init__(self, text, width=600, height=150):
        """Initialize a dialogue box
        
        Args:
            text: The text to display in the dialogue box
            width: Width of the dialogue box (default: 600)
            height: Height of the dialogue box (default: 150)
        """
        self.config = Config()
        self.text = text
        self.width = width
        self.height = height
        
        # Position the dialogue box at the bottom center of the screen
        self.x = (self.config.SCREEN_WIDTH - width) // 2
        self.y = self.config.SCREEN_HEIGHT - height - 20
        
        # Create the background surface
        self.background = pygame.Surface((width, height))
        self.background.fill((0, 0, 0))  # Black background
        
        # Add a border
        pygame.draw.rect(self.background, (255, 255, 255), (0, 0, width, height), 2)
        
        # Font for text rendering
        self.font = pygame.font.Font(None, 24)
        
        # Wrap text to fit in the dialogue box
        self.wrapped_text = self._wrap_text(text)
        
        # Timer for dialogue display (in frames)
        self.timer = 0
        self.duration = 300  # Display for 5 seconds at 60 FPS
        
    def _wrap_text(self, text):
        """Wrap text to fit within the dialogue box width
        
        Args:
            text: The text to wrap
            
        Returns:
            A list of text lines that fit within the box
        """
        words = text.split(' ')
        lines = []
        current_line = []
        
        # Calculate max characters per line based on font width
        max_width = self.width - 20  # 10px padding on each side
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            text_surface = self.font.render(test_line, True, (255, 255, 255))
            
            if text_surface.get_width() > max_width:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
            else:
                current_line.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def update(self):
        """Update the dialogue timer
        
        Returns:
            True if the dialogue is still active, False if it has expired
        """
        self.timer += 1
        return self.timer < self.duration
    
    def draw(self, surface):
        """Draw the dialogue box to the screen
        
        Args:
            surface: The pygame surface to draw to
        """
        # Draw the background
        surface.blit(self.background, (self.x, self.y))
        
        # Draw the text
        line_height = 30
        start_y = self.y + 10
        
        for i, line in enumerate(self.wrapped_text):
            text_surface = self.font.render(line, True, (255, 255, 255))
            text_x = self.x + 10
            text_y = start_y + (i * line_height)
            surface.blit(text_surface, (text_x, text_y))
    
    def is_active(self):
        """Check if the dialogue is still active
        
        Returns:
            True if the dialogue is still being displayed
        """
        return self.timer < self.duration

