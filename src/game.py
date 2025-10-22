"""
Main Game class - handles the game loop and initialization
"""

import pygame
from src.config import Config
from src.player import Player
from src.world import World
from src.camera import Camera


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
        # Spawn player in a safe location (bottom-left area)
        self.player = Player(50, 400)

        # Initialize camera
        self.camera = Camera(
            self.config.SCREEN_WIDTH,
            self.config.SCREEN_HEIGHT,
            self.world.world_width,
            self.world.world_height
        )

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
        self.player.update(keys, self.world.obstacles)
        self.camera.update(self.player)

    def draw(self):
        """Draw everything to the screen"""
        self.screen.fill(self.config.BG_COLOR)

        # Draw world with camera offset
        self.world.draw(self.screen, self.camera)

        # Draw player with camera offset
        player_rect = self.camera.apply(self.player)
        self.screen.blit(self.player.image, player_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.config.FPS)
        
        pygame.quit()

