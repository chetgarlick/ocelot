"""
OCELOT - A 2D Top-Down Adventure Game
Main entry point for the game
"""

import sys
from src.game import Game


def main():
    """Initialize and run the game"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

