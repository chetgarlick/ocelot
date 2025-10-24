"""
Level Loader - loads levels from JSON files
"""

import json
import os
from src.level import Level, ExitZone
from src.obstacle import Obstacle
from src.coin import Coin
from src.enemy import Enemy, TankyEnemy, RangedEnemy, FastEnemy
from src.trap import Trap
from src.boss import Boss
from src.signpost import Signpost


class JSONLevel(Level):
    """A level loaded from a JSON file"""
    
    def __init__(self, json_path):
        """Initialize a level from a JSON file
        
        Args:
            json_path: Path to the JSON level file
        """
        # Load JSON data
        with open(json_path, 'r') as f:
            self.data = json.load(f)
        
        # Extract level properties
        self.level_id = self.data.get('level_id', 'unknown')
        world_width = self.data.get('world_width', 2400)
        world_height = self.data.get('world_height', 1800)
        
        # Initialize parent Level class
        super().__init__(level_id=self.level_id, world_width=world_width, world_height=world_height)
    
    def _generate_obstacles(self):
        """Generate obstacles from JSON data"""
        # Call parent to create boundaries
        super()._generate_obstacles()
        
        # Load obstacles from JSON
        for obstacle_data in self.data.get('obstacles', []):
            x = obstacle_data['x']
            y = obstacle_data['y']
            width = obstacle_data['width']
            height = obstacle_data['height']
            obstacle_type = obstacle_data.get('type', 'solid')
            color = tuple(obstacle_data.get('color', [128, 128, 128]))
            
            obstacle = Obstacle(x, y, width, height, color=color)
            
            # Add to appropriate list based on type
            if obstacle_type == 'visual':
                self.visual_obstacles.append(obstacle)
            else:  # 'solid' or default
                self.obstacles.append(obstacle)
    
    def _generate_coins(self):
        """Generate coins from JSON data"""
        for coin_data in self.data.get('coins', []):
            x = coin_data['x']
            y = coin_data['y']
            coin = Coin(x, y)
            self.coins.append(coin)
    
    def _generate_enemies(self):
        """Generate enemies from JSON data"""
        for enemy_data in self.data.get('enemies', []):
            x = enemy_data['x']
            y = enemy_data['y']
            enemy_type_str = enemy_data.get('type', 'normal')
            patrol_radius = enemy_data.get('patrol_radius', 150)

            # Instantiate the correct enemy class based on type
            if enemy_type_str.lower() == 'tanky':
                enemy = TankyEnemy(x, y, patrol_radius)
            elif enemy_type_str.lower() == 'ranged':
                enemy = RangedEnemy(x, y, patrol_radius)
            elif enemy_type_str.lower() == 'fast':
                enemy = FastEnemy(x, y, patrol_radius)
            else:  # 'normal' or default
                enemy = Enemy(x, y, patrol_radius)

            self.enemies.append(enemy)

    def _generate_traps(self):
        """Generate traps from JSON data"""
        for trap_data in self.data.get('traps', []):
            x = trap_data['x']
            y = trap_data['y']
            width = trap_data['width']
            height = trap_data['height']
            damage = trap_data.get('damage', 10)
            trap_type = trap_data.get('type', 'spike')

            trap = Trap(x, y, width, height, damage=damage, trap_type=trap_type)
            self.traps.append(trap)

    def _generate_boss(self):
        """Generate boss from JSON data"""
        boss_data = self.data.get('boss')
        if boss_data:
            x = boss_data['x']
            y = boss_data['y']
            name = boss_data.get('name', 'Boss')

            self.boss = Boss(x, y, name=name)

    def _generate_signposts(self):
        """Generate signposts from JSON data"""
        for signpost_data in self.data.get('signposts', []):
            signpost = Signpost(
                x=signpost_data['x'],
                y=signpost_data['y'],
                text=signpost_data['text']
            )
            self.signposts.append(signpost)

    def _generate_exits(self):
        """Generate exit zones from JSON data"""
        for exit_data in self.data.get('exits', []):
            exit_zone = ExitZone(
                x=exit_data['x'],
                y=exit_data['y'],
                width=exit_data['width'],
                height=exit_data['height'],
                target_level=exit_data['target_level'],
                spawn_x=exit_data['spawn_x'],
                spawn_y=exit_data['spawn_y']
            )
            self.exit_zones.append(exit_zone)


def load_level(level_id):
    """Load a level by ID

    Args:
        level_id: The ID of the level to load

    Returns:
        A JSONLevel instance
    """
    # Construct path to level JSON file
    # Try multiple possible paths to handle different working directories
    possible_paths = [
        os.path.join('levels', f'{level_id}.json'),  # When running from ocelot directory
        os.path.join('ocelot', 'levels', f'{level_id}.json'),  # When running from project root
    ]

    json_path = None
    for path in possible_paths:
        if os.path.exists(path):
            json_path = path
            break

    if json_path is None:
        raise FileNotFoundError(f"Level file not found: {level_id}. Tried: {possible_paths}")

    return JSONLevel(json_path)

