"""
Main Game class - handles the game loop and initialization
"""

import pygame
from src.config import Config
from src.player import Player
from src.world import World
from src.camera import Camera
from src.menu import MainMenu, OptionsMenu, PauseMenu


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

        # Game state
        self.state = "MAIN_MENU"  # MAIN_MENU, OPTIONS_MENU, PLAYING, PAUSED
        self.current_menu = None

        # Initialize game objects (but don't create them yet)
        self.world = None
        self.player = None
        self.camera = None

        # Create menus
        self._create_menus()

    def _create_menus(self):
        """Create all menus"""
        self.main_menu = MainMenu(
            on_start=self._start_game,
            on_options=self._show_main_options,
            on_quit=self._quit_game
        )

        self.options_menu = OptionsMenu(
            on_back=self._back_to_main_menu
        )

        self.pause_menu = PauseMenu(
            on_resume=self._resume_game,
            on_options=self._show_pause_options,
            on_quit=self._quit_to_main_menu
        )

        # Start with main menu
        self.current_menu = self.main_menu
        self.state = "MAIN_MENU"

    def _start_game(self):
        """Start the game"""
        # Initialize game objects
        self.world = World()
        self.player = Player(50, 400)
        self.camera = Camera(
            self.config.SCREEN_WIDTH,
            self.config.SCREEN_HEIGHT,
            self.world.world_width,
            self.world.world_height
        )
        self.state = "PLAYING"
        return None

    def _show_main_options(self):
        """Show options menu from main menu"""
        self.current_menu = self.options_menu
        self.state = "OPTIONS_MENU"
        return None

    def _back_to_main_menu(self):
        """Go back to main menu"""
        self.current_menu = self.main_menu
        self.state = "MAIN_MENU"
        return None

    def _pause_game(self):
        """Pause the game"""
        self.current_menu = self.pause_menu
        self.state = "PAUSED"

    def _resume_game(self):
        """Resume the game"""
        self.state = "PLAYING"
        return None

    def _show_pause_options(self):
        """Show options menu from pause menu"""
        self.current_menu = self.options_menu
        self.state = "OPTIONS_MENU"
        return None

    def _quit_to_main_menu(self):
        """Quit to main menu"""
        self.current_menu = self.main_menu
        self.state = "MAIN_MENU"
        return None

    def _quit_game(self):
        """Quit the game"""
        self.running = False
        return None

    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "PLAYING":
                        self._pause_game()
                    elif self.state == "PAUSED":
                        self._resume_game()
                    elif self.state in ["MAIN_MENU", "OPTIONS_MENU"]:
                        self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.current_menu:
                        self.current_menu.handle_click(event.pos)

    def update(self):
        """Update game state"""
        if self.state == "PLAYING":
            keys = pygame.key.get_pressed()
            self.player.update(keys, self.world.obstacles)
            self.camera.update(self.player)

            # Update enemies
            for enemy in self.world.enemies:
                enemy.update(self.player, self.world.obstacles)

            # Check for coin collection
            self._check_coin_collection()
        elif self.current_menu:
            mouse_pos = pygame.mouse.get_pos()
            self.current_menu.update(mouse_pos)

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
        if self.state == "PLAYING":
            self.screen.fill(self.config.BG_COLOR)

            # Draw world with camera offset
            self.world.draw(self.screen, self.camera)

            # Draw player with camera offset
            player_rect = self.camera.apply(self.player)
            self.screen.blit(self.player.image, player_rect)

            # Draw UI (coin count in bottom-right)
            self._draw_ui()
        elif self.state == "PAUSED":
            # Draw game in background
            self.screen.fill(self.config.BG_COLOR)
            self.world.draw(self.screen, self.camera)
            player_rect = self.camera.apply(self.player)
            self.screen.blit(self.player.image, player_rect)
            self._draw_ui()

            # Draw semi-transparent overlay
            overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

        # Draw menu if active
        if self.current_menu and self.state != "PLAYING":
            self.current_menu.draw(self.screen)

        pygame.display.flip()

    def _draw_ui(self):
        """Draw UI elements like coin count and HP bar"""
        # Draw HP bar (bottom-left)
        self._draw_hp_bar()

        # Draw coin count (bottom-right)
        self._draw_coin_count()

    def _draw_hp_bar(self):
        """Draw the player's HP bar in the bottom-left corner"""
        # HP bar dimensions
        bar_width = 200
        bar_height = 30
        padding = 10

        # Position in bottom-left corner
        bar_x = padding
        bar_y = self.config.SCREEN_HEIGHT - bar_height - padding

        # Calculate HP percentage
        hp_percentage = self.player.current_hp / self.player.max_hp
        filled_width = int(bar_width * hp_percentage)

        # Draw background (dark)
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (50, 50, 50), bg_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), bg_rect, 2)  # Border

        # Draw filled portion (red to green gradient based on health)
        if hp_percentage > 0.5:
            # Green when healthy
            color = (0, 200, 0)
        elif hp_percentage > 0.25:
            # Yellow when moderate damage
            color = (200, 200, 0)
        else:
            # Red when low health
            color = (200, 0, 0)

        filled_rect = pygame.Rect(bar_x, bar_y, filled_width, bar_height)
        pygame.draw.rect(self.screen, color, filled_rect)

        # Draw HP text
        font = pygame.font.Font(None, 24)
        hp_text = f"{int(self.player.current_hp)}/{int(self.player.max_hp)}"
        text_surface = font.render(hp_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=bg_rect.center)
        self.screen.blit(text_surface, text_rect)

    def _draw_coin_count(self):
        """Draw the coin count in the bottom-right corner"""
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

