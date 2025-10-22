"""
Main Game class - handles the game loop and initialization
"""

import pygame
import math
from src.config import Config
from src.player import Player
from src.world import World
from src.camera import Camera
from src.menu import MainMenu, OptionsMenu, PauseMenu
from src.explosion import Explosion


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
        self.explosions = []

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
        self.explosions = []
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
                elif event.key == pygame.K_SPACE:
                    if self.state == "PLAYING":
                        # Initiate dash in direction of current movement
                        self._initiate_dash()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.state == "PLAYING":
                        # Fire projectile towards cursor
                        mouse_pos = pygame.mouse.get_pos()
                        # Convert screen position to world position
                        world_x = mouse_pos[0] + self.camera.x
                        world_y = mouse_pos[1] + self.camera.y
                        self.player.fire_projectile(world_x, world_y)
                    elif self.current_menu:
                        self.current_menu.handle_click(event.pos)

    def update(self):
        """Update game state"""
        if self.state == "PLAYING":
            keys = pygame.key.get_pressed()
            self.player.update(keys, self.world.obstacles)
            self.player.update_projectiles()
            self.camera.update(self.player)

            # Update enemies
            for enemy in self.world.enemies:
                enemy.update(self.player, self.world.obstacles)

            # Update explosions
            for explosion in self.explosions[:]:
                explosion.update()
                if not explosion.is_alive():
                    self.explosions.remove(explosion)

            # Check for coin collection
            self._check_coin_collection()

            # Check for projectile-enemy collisions
            self._check_projectile_collisions()

            # Check for player-enemy collisions
            self._check_player_enemy_collisions()

            # Check if player is dead
            if not self.player.is_alive():
                self._player_died()
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

    def _check_projectile_collisions(self):
        """Check if projectiles hit enemies"""
        projectiles_to_remove = []
        enemies_to_remove = []

        for proj_idx, projectile in enumerate(self.player.projectiles):
            for enemy_idx, enemy in enumerate(self.world.enemies):
                if projectile.rect.colliderect(enemy.rect):
                    # Projectile hit enemy
                    enemy.take_damage(10)  # 10 damage per projectile
                    projectiles_to_remove.append(proj_idx)

                    # Apply knockback to enemy
                    # Calculate direction from projectile to enemy
                    dx = enemy.x - projectile.x
                    dy = enemy.y - projectile.y
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance > 0:
                        direction_x = dx / distance
                        direction_y = dy / distance
                    else:
                        direction_x, direction_y = 1, 0

                    enemy.apply_knockback(projectile.knockback_power, direction_x, direction_y)

                    # Check if enemy died
                    if not enemy.is_alive():
                        # Create explosion at enemy position
                        self.explosions.append(Explosion(enemy.x + enemy.width // 2,
                                                        enemy.y + enemy.height // 2))
                        enemies_to_remove.append(enemy_idx)
                    break

        # Remove hit projectiles (in reverse order)
        for idx in reversed(sorted(set(projectiles_to_remove))):
            if idx < len(self.player.projectiles):
                self.player.projectiles.pop(idx)

        # Remove dead enemies (in reverse order)
        for idx in reversed(sorted(set(enemies_to_remove))):
            if idx < len(self.world.enemies):
                self.world.enemies.pop(idx)

    def _check_player_enemy_collisions(self):
        """Check if player touches enemies and takes damage"""
        if not hasattr(self.player, 'damage_cooldown'):
            self.player.damage_cooldown = 0

        # Update cooldown
        if self.player.damage_cooldown > 0:
            self.player.damage_cooldown -= 1

        # Check collisions (skip if player is invincible)
        if not self.player.is_invincible():
            for enemy in self.world.enemies:
                if self.player.rect.colliderect(enemy.rect):
                    if self.player.damage_cooldown <= 0:
                        self.player.take_damage(10)  # 10 damage per hit
                        self.player.damage_cooldown = 60  # 1 second cooldown at 60 FPS

                        # Apply knockback to player
                        # Calculate direction from enemy to player
                        dx = self.player.x - enemy.x
                        dy = self.player.y - enemy.y
                        distance = math.sqrt(dx**2 + dy**2)
                        if distance > 0:
                            direction_x = dx / distance
                            direction_y = dy / distance
                        else:
                            direction_x, direction_y = 1, 0

                        self.player.apply_knockback(20, direction_x, direction_y)

    def _player_died(self):
        """Handle player death"""
        # Return to main menu
        self.current_menu = self.main_menu
        self.state = "MAIN_MENU"

    def _initiate_dash(self):
        """Initiate a dash in the direction of current movement"""
        keys = pygame.key.get_pressed()

        # Determine dash direction based on current input
        direction_x = 0
        direction_y = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction_y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction_y += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction_x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction_x += 1

        # Start the dash
        self.player.start_dash(direction_x, direction_y)

    def draw(self):
        """Draw everything to the screen"""
        if self.state == "PLAYING":
            self.screen.fill(self.config.BG_COLOR)

            # Draw world with camera offset
            self.world.draw(self.screen, self.camera)

            # Draw projectiles
            for projectile in self.player.projectiles:
                projectile.draw(self.screen, self.camera)

            # Draw explosions
            for explosion in self.explosions:
                explosion.draw(self.screen, self.camera)

            # Draw player with camera offset
            player_rect = self.camera.apply(self.player)

            # Draw dash effect if dashing
            if self.player.is_dashing:
                self._draw_dash_effect(player_rect)

            self.screen.blit(self.player.image, player_rect)

            # Draw UI (coin count in bottom-right)
            self._draw_ui()
        elif self.state == "PAUSED":
            # Draw game in background
            self.screen.fill(self.config.BG_COLOR)
            self.world.draw(self.screen, self.camera)

            # Draw projectiles
            for projectile in self.player.projectiles:
                projectile.draw(self.screen, self.camera)

            # Draw explosions
            for explosion in self.explosions:
                explosion.draw(self.screen, self.camera)

            player_rect = self.camera.apply(self.player)

            # Draw dash effect if dashing
            if self.player.is_dashing:
                self._draw_dash_effect(player_rect)

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

    def _draw_dash_effect(self, player_rect):
        """Draw a visual effect for the dash

        Args:
            player_rect: The player's screen position rect
        """
        # Create a semi-transparent blue circle around the player
        dash_radius = int(self.player.width * 1.5)

        # Create a surface for the dash effect
        dash_surface = pygame.Surface((dash_radius * 2, dash_radius * 2), pygame.SRCALPHA)

        # Draw a glowing circle effect
        alpha = int(150 * (1 - self.player.dash_timer / self.player.dash_duration))
        pygame.draw.circle(dash_surface, (100, 200, 255, alpha),
                         (dash_radius, dash_radius), dash_radius)

        # Blit to screen
        self.screen.blit(dash_surface,
                        (player_rect.centerx - dash_radius,
                         player_rect.centery - dash_radius))

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.config.FPS)
        
        pygame.quit()

