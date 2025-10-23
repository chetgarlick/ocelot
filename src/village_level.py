"""
Village Level - peaceful starting area with buildings and paths
"""

from src.level import Level, ExitZone
from src.obstacle import Obstacle
from src.coin import Coin


class VillageLevel(Level):
    """A peaceful village with buildings and paths"""
    
    def __init__(self):
        """Initialize the village level"""
        super().__init__(level_id="village", world_width=1600, world_height=1200)
    
    def _generate_obstacles(self):
        """Generate obstacles (buildings and paths) for the village"""
        # Call parent to create boundaries
        super()._generate_obstacles()
        
        # Village buildings (represented as obstacles)
        # Each building is a simple rectangle
        
        # Top-left building
        self.obstacles.append(Obstacle(100, 100, 150, 120))
        
        # Top-center building
        self.obstacles.append(Obstacle(500, 80, 180, 140))
        
        # Top-right building
        self.obstacles.append(Obstacle(1000, 120, 160, 130))
        
        # Middle-left building
        self.obstacles.append(Obstacle(80, 450, 140, 150))
        
        # Middle-center building (larger - town hall)
        self.obstacles.append(Obstacle(450, 400, 200, 200))
        
        # Middle-right building
        self.obstacles.append(Obstacle(1050, 480, 150, 140))
        
        # Bottom-left building
        self.obstacles.append(Obstacle(150, 900, 130, 120))
        
        # Bottom-center building
        self.obstacles.append(Obstacle(550, 920, 160, 130))
        
        # Bottom-right building
        self.obstacles.append(Obstacle(1100, 880, 140, 150))
        
        # Small decorative obstacles (trees, fences, etc.)
        self.obstacles.append(Obstacle(300, 300, 30, 30))
        self.obstacles.append(Obstacle(700, 250, 30, 30))
        self.obstacles.append(Obstacle(1200, 350, 30, 30))
        self.obstacles.append(Obstacle(400, 700, 30, 30))
        self.obstacles.append(Obstacle(900, 650, 30, 30))
    
    def _generate_coins(self):
        """Generate coins scattered throughout the village"""
        coin_positions = [
            (250, 250), (600, 200), (1100, 250),
            (200, 600), (700, 550), (1200, 600),
            (300, 1000), (800, 1000), (1300, 950),
        ]
        
        for x, y in coin_positions:
            self.coins.append(Coin(x, y))
    
    def _generate_enemies(self):
        """Village has no enemies - it's a peaceful starting area"""
        pass
    
    def _generate_exits(self):
        """Generate exit zones for the village"""
        # Exit on the right side leads to the combat level
        # Player spawns at the left side of the combat level
        self.exit_zones.append(ExitZone(
            x=1500,  # Right edge of village
            y=400,
            width=100,
            height=400,
            target_level="combat",
            spawn_x=100,  # Spawn on left side of combat level
            spawn_y=400
        ))

