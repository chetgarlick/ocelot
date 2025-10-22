"""
Main Game class - handles the game loop and initialization
"""

import pygame
from src.config import Config
from src.player import Player
from src.world import World


class Game:
    """Main game class"""

    def __init__(self):
        """Initialize the game"""
        pygame.init()
        
        self.config = Config()
        self.screen = pygame.display.set_mode(
            (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(self.config.GAME_TITLE)
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game objects
        self.world = World()
        self.player = Player(self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT // 2)

    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Update game state"""
        keys = pygame.key.get_pressed()
        self.player.update(keys)

    def draw(self):
        """Draw everything to the screen"""
        self.screen.fill(self.config.BG_COLOR)
        
        # Draw world
        self.world.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.config.FPS)
        
        pygame.quit()

