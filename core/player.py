"""Player module."""

import math

import pygame


class Player:
    """The player."""

    def __init__(self, game):
        """Init class."""
        self.game = game
        self.x, self.y = game.config["player"]["pos"]
        self.angle = game.config["player"]["angle"]
        self.radius = min(self.game.map.tile_width, self.game.map.tile_height) / 2

    def move(self):
        """Move player."""
        sin_a = math.sin(self.angle)  # TODO Study
        cos_a = math.cos(self.angle)  # TODO Study
        dx, dy = 0, 0
        speed = self.game.config["player"]["speed"] * self.game.delta_time  # TODO Study
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pygame.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pygame.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pygame.K_d]:
            dx += -speed_sin
            dy += speed_cos
        if not self.game.config["debugging"]["disable_collisions"]:
            self.check_wall_collision(dx, dy)
        else:
            self.x += dx
            self.y += dy
        if keys[pygame.K_LEFT]:
            self.angle -= (
                self.game.config["player"]["rotation_speed"] * self.game.delta_time
            )
        if keys[pygame.K_RIGHT]:
            self.angle += (
                self.game.config["player"]["rotation_speed"] * self.game.delta_time
            )
        self.angle %= math.tau

    def check_wall(self, x, y):
        """Check wall."""
        return (x, y) not in self.game.map.values

    def check_wall_collision(self, dx, dy):
        """Check wall collision."""
        scale = self.radius * 10 / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        """Draw player."""
        if self.game.config["debugging"]["enable_player_ray"]:
            pygame.draw.line(
                self.game.screen,
                self.game.config["debugging"]["player_ray_color_rgb"],
                (self.x * self.game.map.tile_width, self.y * self.game.map.tile_height),
                (
                    self.x * self.game.map.tile_width
                    + self.game.config["engine"]["width"] * math.cos(self.angle),
                    self.x * self.game.map.tile_height
                    + self.game.config["engine"]["width"]
                    * math.sin(self.angle),  # TODO Study
                ),
                2,
            )
        pygame.draw.circle(
            self.game.screen,
            self.game.config["player"]["color_rgb"],
            (self.x * self.game.map.tile_width, self.y * self.game.map.tile_height),
            self.radius,
        )

    def update(self):
        """Update player."""
        self.move()

    @property
    def pos(self):
        """Return the player position."""
        return self.x, self.y

    @property
    def map_pos(self):
        """Return the tile the player is on."""
        return int(self.x), int(self.y)
