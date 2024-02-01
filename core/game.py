"""Main module."""

import sys

import pygame
import tomli

from .player import Player
from .raycaster import RayCaster


class Game:
    """The game."""

    def __init__(self, game_map):
        """Init class."""
        pygame.init()
        pygame.mouse.set_visible(False)
        self.config = self.get_config()
        self.map_filename = game_map
        self.screen = pygame.display.set_mode(
            (self.config["engine"]["width"], self.config["engine"]["height"])
        )
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        """Init a new game."""
        self.map = Map(self, self.map_filename)
        self.player = Player(self)
        self.ray_caster = RayCaster(self)

    def update(self):
        """Update game."""
        self.player.update()
        if not self.config["debugging"]["enable_player_ray"]:
            self.ray_caster.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.config["engine"]["fps"])
        pygame.display.set_caption(f"{self.clock.get_fps():.1f}")

    def draw(self):
        """Draw game."""
        self.screen.fill(self.config["engine"]["background_color_rgb"])
        if self.config["debugging"]["disable_3d_projection"]:
            self.map.draw()
            self.player.draw()

    def check_events(self):
        """Check game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()

    def get_config(self):
        """Return configuration."""
        with open("pyproject.toml", "rb") as f:
            return tomli.load(f)["configuration"]

    def run(self):
        """Run game."""
        while True:
            self.check_events()
            self.update()
            self.draw()


class Map:
    """The map."""

    def __init__(self, game, filename):
        """Init class."""
        self.game = game
        self.filename = filename
        self.raw_values = self.read()
        self.width = len(self.raw_values[0])
        self.height = len(self.raw_values)
        self.tile_width = game.config["engine"]["width"] / len(self.raw_values[0])
        self.tile_height = game.config["engine"]["height"] / len(self.raw_values)
        self.values = self.get()

    def read(self):
        """Read map as list."""
        with open(f"maps/{self.filename}.txt") as f:
            content_lines = list(filter(None, f.read().split("\n")))
            game_map = []
            for line in content_lines:
                tile_values = []
                for tile in line.split(" "):
                    tile_value = {
                        "X": True,
                        "_": False,
                    }[tile]
                    tile_values.append(tile_value)
                game_map.append(tile_values)
            return game_map

    def get(self):
        """Return map."""
        values = {}
        for j, row in enumerate(self.raw_values):
            for i, value in enumerate(row):
                if value:
                    values[(i, j)] = value
        return values

    def draw(self):
        """Draw map."""
        [
            pygame.draw.rect(
                self.game.screen,
                self.game.config["engine"]["wall_color_rgb"],
                (
                    pos[0] * self.tile_width,
                    pos[1] * self.tile_height,
                    self.tile_width,
                    self.tile_height,
                ),
                2,
            )
            for pos in self.values
        ]
