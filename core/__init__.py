"""Init core package."""

import click

from .game import Game


@click.command()
@click.option("--map", "game_map", help="The map file name")
def run(game_map):
    """Run demo."""
    game = Game(game_map)
    game.run()


if __name__ == "__main__":
    run()
