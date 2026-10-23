"""Program entry point for the platformer."""

import arcade

from game import PlatformerGame


def main():
    """Create the game, prepare it, and start the game loop."""
    game = PlatformerGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
