"""
Menu system - handles menus and buttons
"""

import pygame
from src.config import Config


class Button:
    """A clickable button for menus"""

    def __init__(self, x, y, width, height, text, callback=None):
        """Initialize a button

        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            text: Button text
            callback: Function to call when button is clicked
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.is_hovered = False
        self.is_selected = False  # For keyboard navigation
        self.font = pygame.font.Font(None, 36)

        # Colors
        self.normal_color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        self.selected_color = (200, 100, 100)  # Red-ish for keyboard selection
        self.text_color = (255, 255, 255)

    def update(self, mouse_pos):
        """Update button state based on mouse position
        
        Args:
            mouse_pos: Current mouse position (x, y)
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        """Draw the button to the screen

        Args:
            surface: Pygame surface to draw to
        """
        # Draw button background
        if self.is_selected:
            color = self.selected_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.normal_color
        pygame.draw.rect(surface, color, self.rect)

        # Draw border (thicker if selected)
        border_width = 3 if self.is_selected else 2
        pygame.draw.rect(surface, (255, 255, 255), self.rect, border_width)

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_click(self, mouse_pos):
        """Handle mouse click

        Args:
            mouse_pos: Mouse position (x, y)

        Returns:
            Result of callback if clicked, None otherwise
        """
        if self.rect.collidepoint(mouse_pos) and self.callback:
            return self.callback()
        return None

    def activate(self):
        """Activate the button (called when selected via keyboard)

        Returns:
            Result of callback if exists, None otherwise
        """
        if self.callback:
            return self.callback()
        return None


class Menu:
    """Base menu class"""

    def __init__(self, title="Menu"):
        """Initialize a menu

        Args:
            title: Menu title
        """
        self.config = Config()
        self.title = title
        self.buttons = []
        self.selected_index = 0  # Index of currently selected button
        self.title_font = pygame.font.Font(None, 72)
        self.bg_color = (20, 20, 40)  # Dark blue background

    def add_button(self, text, callback, y_offset=0):
        """Add a button to the menu

        Args:
            text: Button text
            callback: Function to call when clicked
            y_offset: Y offset from default position
        """
        button_width = 300
        button_height = 60
        button_x = (self.config.SCREEN_WIDTH - button_width) // 2
        button_y = 250 + (len(self.buttons) * 100) + y_offset

        button = Button(button_x, button_y, button_width, button_height, text, callback)
        self.buttons.append(button)

        # Select first button by default
        if len(self.buttons) == 1:
            button.is_selected = True

    def update(self, mouse_pos):
        """Update menu state
        
        Args:
            mouse_pos: Current mouse position
        """
        for button in self.buttons:
            button.update(mouse_pos)

    def handle_click(self, mouse_pos):
        """Handle mouse click

        Args:
            mouse_pos: Mouse position

        Returns:
            Result from button callback if clicked
        """
        for button in self.buttons:
            result = button.handle_click(mouse_pos)
            if result is not None:
                return result
        return None

    def handle_keyboard(self, key):
        """Handle keyboard input for menu navigation

        Args:
            key: Pygame key constant

        Returns:
            Result from button callback if activated, None otherwise
        """
        if key in [pygame.K_UP, pygame.K_w]:
            # Move selection up
            self.buttons[self.selected_index].is_selected = False
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
            self.buttons[self.selected_index].is_selected = True
        elif key in [pygame.K_DOWN, pygame.K_s]:
            # Move selection down
            self.buttons[self.selected_index].is_selected = False
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
            self.buttons[self.selected_index].is_selected = True
        elif key in [pygame.K_RETURN, pygame.K_SPACE]:
            # Activate selected button
            return self.buttons[self.selected_index].activate()

        return None

    def draw(self, surface):
        """Draw the menu to the screen
        
        Args:
            surface: Pygame surface to draw to
        """
        # Draw background
        surface.fill(self.bg_color)
        
        # Draw title
        title_surface = self.title_font.render(self.title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, 80))
        surface.blit(title_surface, title_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)


class MainMenu(Menu):
    """Main menu shown at game start"""

    def __init__(self, on_start, on_options, on_quit):
        """Initialize main menu
        
        Args:
            on_start: Callback for Start Game button
            on_options: Callback for Options button
            on_quit: Callback for Quit button
        """
        super().__init__("OCELOT")
        self.add_button("Start Game", on_start)
        self.add_button("Options", on_options)
        self.add_button("Quit", on_quit)


class OptionsMenu(Menu):
    """Options menu"""

    def __init__(self, on_back):
        """Initialize options menu
        
        Args:
            on_back: Callback for Back button
        """
        super().__init__("Options")
        # Placeholder for future options
        self.add_button("Back", on_back)


class PauseMenu(Menu):
    """Pause menu shown during gameplay"""

    def __init__(self, on_resume, on_options, on_quit):
        """Initialize pause menu
        
        Args:
            on_resume: Callback for Resume button
            on_options: Callback for Options button
            on_quit: Callback for Quit button
        """
        super().__init__("Paused")
        self.add_button("Resume", on_resume)
        self.add_button("Options", on_options)
        self.add_button("Quit", on_quit)

