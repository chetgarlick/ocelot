"""
Dialogue system for displaying text to the player
"""

import pygame
from src.config import Config


class DialogueChoice:
    """Represents a single choice option in a dialogue"""

    def __init__(self, text, callback=None):
        """Initialize a dialogue choice

        Args:
            text: The text to display for this choice
            callback: Optional callback function to execute when this choice is selected
        """
        self.text = text
        self.callback = callback
        self.is_selected = False


class Dialogue:
    """Represents a dialogue box that displays text to the player"""

    def __init__(self, text, width=600, height=150, choices=None):
        """Initialize a dialogue box

        Args:
            text: The text to display in the dialogue box
            width: Width of the dialogue box (default: 600)
            height: Height of the dialogue box (default: 150)
            choices: List of DialogueChoice objects (optional)
        """
        self.config = Config()
        self.text = text
        self.width = width
        self.height = height
        self.choices = choices or []

        # Calculate total height needed for choices
        choice_height = 0
        if self.choices:
            choice_height = len(self.choices) * 25 + 20  # 25px per choice + padding

        total_height = height + choice_height

        # Position the dialogue box at the bottom center of the screen
        # Adjust Y position to keep the entire box on screen
        self.x = (self.config.SCREEN_WIDTH - width) // 2
        self.y = max(20, self.config.SCREEN_HEIGHT - total_height - 20)

        # Create the background surface
        self.background = pygame.Surface((width, height))
        self.background.fill((0, 0, 0))  # Black background

        # Add a border
        pygame.draw.rect(self.background, (255, 255, 255), (0, 0, width, height), 2)

        # Font for text rendering
        self.font = pygame.font.Font(None, 24)
        self.choice_font = pygame.font.Font(None, 20)

        # Wrap text to fit in the dialogue box
        self.wrapped_text = self._wrap_text(text)

        # Timer for dialogue display (in frames)
        self.timer = 0
        # If there are choices, dialogue doesn't auto-expire
        self.duration = float('inf') if self.choices else 300  # Display for 5 seconds at 60 FPS if no choices

        # Choice selection
        self.selected_choice_index = 0
        if self.choices:
            self.choices[0].is_selected = True
        
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
        # Calculate height needed for choices
        choice_height = 0
        if self.choices:
            choice_height = len(self.choices) * 25 + 20  # 25px per choice + padding

        # Create a larger background if we have choices
        total_height = self.height + choice_height
        background = pygame.Surface((self.width, total_height))
        background.fill((0, 0, 0))  # Black background
        pygame.draw.rect(background, (255, 255, 255), (0, 0, self.width, total_height), 2)

        # Draw the background
        surface.blit(background, (self.x, self.y))

        # Draw the text
        line_height = 30
        start_y = self.y + 10

        for i, line in enumerate(self.wrapped_text):
            text_surface = self.font.render(line, True, (255, 255, 255))
            text_x = self.x + 10
            text_y = start_y + (i * line_height)
            surface.blit(text_surface, (text_x, text_y))

        # Draw choices if available
        if self.choices:
            choices_start_y = self.y + self.height + 10
            for i, choice in enumerate(self.choices):
                choice_y = choices_start_y + (i * 25)

                # Highlight selected choice
                if choice.is_selected:
                    # Draw selection background
                    pygame.draw.rect(surface, (0, 100, 200),
                                   (self.x + 5, choice_y - 2, self.width - 10, 22))
                    choice_text = self.choice_font.render(f"> {choice.text}", True, (0, 255, 255))
                else:
                    choice_text = self.choice_font.render(f"  {choice.text}", True, (200, 200, 200))

                surface.blit(choice_text, (self.x + 10, choice_y))
    
    def is_active(self):
        """Check if the dialogue is still active

        Returns:
            True if the dialogue is still being displayed
        """
        return self.timer < self.duration

    def select_next_choice(self):
        """Move selection to the next choice"""
        if self.choices:
            self.choices[self.selected_choice_index].is_selected = False
            self.selected_choice_index = (self.selected_choice_index + 1) % len(self.choices)
            self.choices[self.selected_choice_index].is_selected = True

    def select_previous_choice(self):
        """Move selection to the previous choice"""
        if self.choices:
            self.choices[self.selected_choice_index].is_selected = False
            self.selected_choice_index = (self.selected_choice_index - 1) % len(self.choices)
            self.choices[self.selected_choice_index].is_selected = True

    def confirm_choice(self):
        """Execute the callback for the selected choice

        Returns:
            The result of the callback, or None if no callback
        """
        if self.choices and self.selected_choice_index < len(self.choices):
            choice = self.choices[self.selected_choice_index]
            if choice.callback:
                return choice.callback()
        return None


class DialogueTree:
    """Represents a branching dialogue tree for complex interactions like merchants and quest givers"""

    def __init__(self, name):
        """Initialize a dialogue tree

        Args:
            name: Name of the dialogue tree (e.g., "merchant_greeting", "quest_giver_main")
        """
        self.name = name
        self.nodes = {}  # Dictionary of node_id -> DialogueNode
        self.current_node_id = None

    def add_node(self, node_id, text, choices=None):
        """Add a node to the dialogue tree

        Args:
            node_id: Unique identifier for this node
            text: The dialogue text to display
            choices: List of tuples (choice_text, next_node_id) or (choice_text, next_node_id, callback)
        """
        self.nodes[node_id] = {
            'text': text,
            'choices': choices or []
        }

    def start(self, start_node_id="start"):
        """Start the dialogue tree at a specific node

        Args:
            start_node_id: The node to start at (default: "start")

        Returns:
            A Dialogue object for the starting node
        """
        self.current_node_id = start_node_id
        return self._create_dialogue_for_node(start_node_id)

    def _create_dialogue_for_node(self, node_id):
        """Create a Dialogue object for a specific node

        Args:
            node_id: The node ID to create dialogue for

        Returns:
            A Dialogue object with choices that navigate the tree
        """
        if node_id not in self.nodes:
            return None

        node = self.nodes[node_id]
        choices = []

        for choice_data in node['choices']:
            if len(choice_data) == 2:
                choice_text, next_node_id = choice_data
                callback = None
            else:
                choice_text, next_node_id, callback = choice_data

            # Create a callback that navigates to the next node
            def make_callback(nid, cb):
                def navigate():
                    self.current_node_id = nid
                    if cb:
                        cb()
                return navigate

            choice = DialogueChoice(choice_text, make_callback(next_node_id, callback))
            choices.append(choice)

        return Dialogue(node['text'], choices=choices)

    def get_next_dialogue(self):
        """Get the dialogue for the current node

        Returns:
            A Dialogue object for the current node, or None if no current node
        """
        if self.current_node_id:
            return self._create_dialogue_for_node(self.current_node_id)
        return None

