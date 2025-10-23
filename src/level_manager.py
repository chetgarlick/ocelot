"""
LevelManager - manages level transitions and level state
"""

from src.level_loader import load_level


class LevelManager:
    """Manages all levels and transitions between them"""
    
    def __init__(self):
        """Initialize the level manager"""
        self.levels = {}
        self.current_level_id = None
        self.current_level = None
        
        # Create all levels
        self._create_levels()
        
        # Start with village level
        self.load_level("village")
    
    def _create_levels(self):
        """Create all available levels"""
        # Load levels from JSON files
        self.levels["village"] = load_level("village")
        self.levels["combat"] = load_level("combat")
        self.levels["trap_dungeon"] = load_level("trap_dungeon")
    
    def load_level(self, level_id):
        """Load a level by ID
        
        Args:
            level_id: The ID of the level to load
            
        Returns:
            The loaded level
        """
        if level_id not in self.levels:
            raise ValueError(f"Level '{level_id}' not found")
        
        self.current_level_id = level_id
        self.current_level = self.levels[level_id]
        return self.current_level
    
    def get_current_level(self):
        """Get the current level
        
        Returns:
            The current level
        """
        return self.current_level
    
    def get_level(self, level_id):
        """Get a level by ID
        
        Args:
            level_id: The ID of the level to get
            
        Returns:
            The level, or None if not found
        """
        return self.levels.get(level_id)

