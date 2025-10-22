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

        # Update enemies
        for enemy in self.world.enemies:
            enemy.update(self.player, self.world.obstacles)

        # Check for coin collection
        self._check_coin_collection()

    def _check_coin_collection(self):
        """Check if player collides with any coins and collect them"""
        coins_to_remove = []

        for i, coin in enumerate(self.world.coins):
            if self.player.rect.colliderect(coin.rect):
                self.player.collect_coin()
                coins_to_remove.append(i)

        # Remove collected coins (in reverse order to maintain indices)
        for i in reversed(coins_to_remove):
            self.world.coins.pop(i)

    def draw(self):
        """Draw everything to the screen"""
        self.screen.fill(self.config.BG_COLOR)

        # Draw world with camera offset
        self.world.draw(self.screen, self.camera)

        # Draw player with camera offset
        player_rect = self.camera.apply(self.player)
        self.screen.blit(self.player.image, player_rect)

        # Draw UI (star count in bottom-right)
        self._draw_ui()

        pygame.display.flip()

    def _draw_ui(self):
        """Draw UI elements like coin count"""
        # Create font for text
        font = pygame.font.Font(None, 36)

        # Create coin icon and text
        coin_text = f"● {self.player.coins_collected}"
        text_surface = font.render(coin_text, True, (255, 255, 0))  # Yellow text

        # Position in bottom-right corner with padding
        padding = 10
        text_rect = text_surface.get_rect()
        text_rect.bottomright = (
            self.config.SCREEN_WIDTH - padding,
            self.config.SCREEN_HEIGHT - padding
        )

        # Draw semi-transparent background for readability
        bg_rect = text_rect.inflate(20, 10)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surface.set_alpha(200)
        bg_surface.fill((0, 0, 0))
        self.screen.blit(bg_surface, bg_rect)

        # Draw text
        self.screen.blit(text_surface, text_rect)

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.config.FPS)
        
        pygame.quit()

