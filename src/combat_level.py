"""
Combat Level - the main adventure area with enemies and obstacles
"""

from src.level import Level, ExitZone
from src.obstacle import Obstacle
from src.coin import Coin
from src.enemy import Enemy, TankyEnemy, RangedEnemy, FastEnemy


class CombatLevel(Level):
    """The main combat area with enemies and obstacles"""
    
    def __init__(self):
        """Initialize the combat level"""
        super().__init__(level_id="combat", world_width=2400, world_height=1800)
    
    def _generate_obstacles(self):
        """Generate obstacles in the combat level"""
        # Call parent to create boundaries
        super()._generate_obstacles()
        
        # Create obstacles scattered throughout the larger world
        
        # Top-left area
        self.obstacles.append(Obstacle(100, 50, 300, 20))
        self.obstacles.append(Obstacle(600, 100, 20, 250))
        
        # Top-right area
        self.obstacles.append(Obstacle(1500, 100, 400, 30))
        self.obstacles.append(Obstacle(2000, 200, 100, 150))
        
        # Middle area
        self.obstacles.append(Obstacle(150, 500, 300, 20))
        self.obstacles.append(Obstacle(350, 250, 100, 100))
        self.obstacles.append(Obstacle(1000, 600, 200, 50))
        self.obstacles.append(Obstacle(1200, 400, 50, 200))
        
        # Bottom-left area
        self.obstacles.append(Obstacle(200, 1400, 250, 30))
        self.obstacles.append(Obstacle(100, 1200, 30, 300))
        
        # Bottom-right area
        self.obstacles.append(Obstacle(1800, 1500, 300, 40))
        self.obstacles.append(Obstacle(2100, 1200, 100, 200))
        
        # Center-right area
        self.obstacles.append(Obstacle(1600, 800, 150, 150))
    
    def _generate_coins(self):
        """Generate coins scattered throughout the combat level"""
        coin_positions = [
            (200, 200), (400, 150), (700, 300), (900, 250),
            (300, 700), (800, 900), (1200, 700), (1400, 600),
            (500, 1200), (1000, 1400), (1600, 1300), (1900, 1100),
            (2100, 400), (1800, 800), (600, 1600), (1300, 1600),
            (400, 900), (1100, 300), (1700, 500), (2200, 1400),
        ]
        
        for x, y in coin_positions:
            self.coins.append(Coin(x, y))
    
    def _generate_enemies(self):
        """Generate enemies scattered throughout the combat level"""
        enemy_positions = [
            (400, 400, 150, "normal"),      # Normal red enemy
            (1200, 300, 150, "tanky"),      # Tanky blue enemy
            (1600, 1000, 150, "ranged"),    # Ranged purple enemy
            (800, 1400, 150, "fast"),       # Fast green enemy
            (2000, 600, 150, "normal"),     # Another normal enemy
        ]
        
        for x, y, patrol_radius, enemy_type in enemy_positions:
            if enemy_type == "tanky":
                self.enemies.append(TankyEnemy(x, y, patrol_radius))
            elif enemy_type == "ranged":
                self.enemies.append(RangedEnemy(x, y, patrol_radius))
            elif enemy_type == "fast":
                self.enemies.append(FastEnemy(x, y, patrol_radius))
            else:  # normal
                self.enemies.append(Enemy(x, y, patrol_radius))
    
    def _generate_exits(self):
        """Generate exit zones for the combat level"""
        # Exit on the left side leads back to the village
        # Player spawns at the right side of the village
        self.exit_zones.append(ExitZone(
            x=-100,  # Left edge of combat level
            y=400,
            width=100,
            height=400,
            target_level="village",
            spawn_x=1400,  # Spawn on right side of village
            spawn_y=400
        ))

