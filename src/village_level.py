"""
Village Level - peaceful starting area with buildings and paths
"""

from src.level import Level, ExitZone
from src.obstacle import Obstacle
from src.npc import NPC
from src.dialogue import DialogueTree


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
        # Smaller buildings are solid, larger buildings are hollow (walls only)

        # Brown color for wooden flooring inside buildings
        brown_floor = (139, 90, 43)

        # Top-left building (solid)
        self.obstacles.append(Obstacle(100, 100, 150, 120))

        # Top-center building (solid)
        self.obstacles.append(Obstacle(500, 80, 180, 140))

        # Top-right building (solid) - REMOVED (outskirts)
        # self.obstacles.append(Obstacle(1000, 120, 160, 130))

        # Middle-left building (solid) - REMOVED (outskirts)
        # self.obstacles.append(Obstacle(80, 450, 140, 150))

        # Middle-center building (larger - town hall) - HOLLOW with brown floor
        wall_thickness = 15
        # Brown floor background (visual only - no collision)
        self.visual_obstacles.append(Obstacle(450, 400, 200, 200, color=brown_floor))
        # Top wall with large door gap (leave gap in middle for player to enter)
        self.obstacles.append(Obstacle(450, 400, 60, wall_thickness))  # Left part
        self.obstacles.append(Obstacle(590, 400, 60, wall_thickness))  # Right part
        # Bottom wall with large door gap
        self.obstacles.append(Obstacle(450, 585, 60, wall_thickness))  # Left part
        self.obstacles.append(Obstacle(590, 585, 60, wall_thickness))  # Right part
        # Left wall (no gaps - solid)
        self.obstacles.append(Obstacle(450, 400, wall_thickness, 200))
        # Right wall (no gaps - solid)
        self.obstacles.append(Obstacle(635, 400, wall_thickness, 200))

        # Middle-left building (enlarged and hollow) - HOLLOW with brown floor
        # Increased from 140x150 to 180x180
        wall_thickness = 15
        # Brown floor background (visual only - no collision)
        self.visual_obstacles.append(Obstacle(250, 350, 180, 180, color=brown_floor))
        # Top wall with large door gap
        self.obstacles.append(Obstacle(250, 350, 55, wall_thickness))  # Left part
        self.obstacles.append(Obstacle(375, 350, 55, wall_thickness))  # Right part
        # Bottom wall with large door gap
        self.obstacles.append(Obstacle(250, 515, 55, wall_thickness))  # Left part
        self.obstacles.append(Obstacle(375, 515, 55, wall_thickness))  # Right part
        # Left wall (no gaps - solid)
        self.obstacles.append(Obstacle(250, 350, wall_thickness, 180))
        # Right wall (no gaps - solid)
        self.obstacles.append(Obstacle(415, 350, wall_thickness, 180))

        # Middle-right building (enlarged and hollow) - HOLLOW with brown floor
        # Moved to the right and increased from 150x140 to 180x180
        wall_thickness = 15
        # Brown floor background (visual only - no collision)
        self.visual_obstacles.append(Obstacle(900, 350, 180, 180, color=brown_floor))
        # Top wall (no gaps - solid)
        self.obstacles.append(Obstacle(900, 350, 180, wall_thickness))
        # Bottom wall (no gaps - solid)
        self.obstacles.append(Obstacle(900, 515, 180, wall_thickness))
        # Left wall with large door gap
        self.obstacles.append(Obstacle(900, 350, wall_thickness, 55))  # Top part
        self.obstacles.append(Obstacle(900, 475, wall_thickness, 60))  # Bottom part
        # Right wall with large door gap
        self.obstacles.append(Obstacle(1065, 350, wall_thickness, 55))  # Top part
        self.obstacles.append(Obstacle(1065, 475, wall_thickness, 60))  # Bottom part

        # Bottom-left building (solid) - REMOVED (outskirts)
        # self.obstacles.append(Obstacle(150, 900, 130, 120))

        # Bottom-center building (solid)
        self.obstacles.append(Obstacle(550, 920, 160, 130))

        # Bottom-right building (solid) - REMOVED (outskirts)
        # self.obstacles.append(Obstacle(1100, 880, 140, 150))

        # Small decorative obstacles (trees, fences, etc.) - REMOVED (outskirts)
        # self.obstacles.append(Obstacle(300, 300, 30, 30))
        # self.obstacles.append(Obstacle(700, 250, 30, 30))
        # self.obstacles.append(Obstacle(1200, 350, 30, 30))
        # self.obstacles.append(Obstacle(400, 700, 30, 30))
        # self.obstacles.append(Obstacle(900, 650, 30, 30))
    
    def _generate_coins(self):
        """Village has no coins - it's a peaceful starting area"""
        pass
    
    def _generate_enemies(self):
        """Village has no enemies - it's a peaceful starting area"""
        pass

    def _generate_npcs(self):
        """Generate NPCs for the village"""
        # Create a merchant NPC in the main building (town hall)
        merchant_tree = DialogueTree("merchant_greeting")

        # Add dialogue nodes
        merchant_tree.add_node(
            "start",
            "Welcome, traveler! I'm the village merchant. What brings you here?",
            choices=[
                ("Tell me about the world", "world_info"),
                ("I'm looking for supplies", "supplies"),
                ("Just passing through", "end")
            ]
        )

        merchant_tree.add_node(
            "world_info",
            "Beyond our peaceful village lies danger and adventure. Many have ventured out seeking fortune and glory. Some return as heroes, others... well, we don't see them again.",
            choices=[
                ("Sounds exciting!", "excited"),
                ("That sounds dangerous", "cautious"),
                ("Back to main topic", "start")
            ]
        )

        merchant_tree.add_node(
            "excited",
            "Ah, a brave soul! You'll fit right in with the adventurers. Head east when you're ready to test your skills!",
            choices=[
                ("I'll head out soon", "end"),
                ("Tell me more", "world_info")
            ]
        )

        merchant_tree.add_node(
            "cautious",
            "Wise to be cautious. But fortune favors the bold! When you're ready, head east to find your destiny.",
            choices=[
                ("I'll think about it", "end"),
                ("Tell me more", "world_info")
            ]
        )

        merchant_tree.add_node(
            "supplies",
            "Ah, supplies! I have everything an adventurer needs. Unfortunately, my shop isn't quite ready yet. Check back soon!",
            choices=[
                ("Understood", "end"),
                ("Back to main topic", "start")
            ]
        )

        merchant_tree.add_node(
            "end",
            "Safe travels, adventurer!",
            choices=[]
        )

        # Create the merchant NPC in the center of the main building
        merchant = NPC(
            x=540,  # Center of the main building
            y=480,  # Center of the main building
            name="Merchant",
            dialogue_tree=merchant_tree
        )
        self.npcs.append(merchant)

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

