"""Ray caster module."""

import math

import pygame


class RayCaster:
    """The ray caster."""

    def __init__(self, game):
        """Init class."""
        self.game = game
        self.amount = (
            game.config["engine"]["width"]
            // 2
            // (10 - game.config["engine"]["detail"] + 1)
        )

    def cast_ray(self):
        """Cast ray."""
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        field_of_view = self.game.config["engine"]["fov"] * math.pi / 180
        correction = 0.0001
        ray_angle = self.game.player.angle - (field_of_view / 2) + correction
        for ray in range(self.amount):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 0.000001, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            max_depth = int(math.ceil(max(self.game.map.width, self.game.map.height)))

            for _i in range(max_depth):
                tile_hor = int(x_hor), int(y_hor)
                if (
                    not self.game.config["debugging"]["disable_collisions"]
                    and tile_hor in self.game.map.values
                ):
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for _i in range(max_depth):
                tile_vert = int(x_vert), int(y_vert)
                if (
                    not self.game.config["debugging"]["disable_collisions"]
                    and tile_vert in self.game.map.values
                ):
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth
            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor

            if self.game.config["debugging"]["disable_3d_projection"]:
                pygame.draw.line(
                    self.game.screen,
                    self.game.config["engine"]["ray_color_rgb"],
                    (self.game.map.tile_width * ox, self.game.map.tile_height * oy),
                    (
                        self.game.map.tile_width * ox
                        + self.game.map.tile_width * depth * cos_a,
                        self.game.map.tile_height * oy
                        + self.game.map.tile_height * depth * sin_a,
                    ),
                    2,
                )
            else:
                # remove fishbowl effect
                depth *= math.cos(self.game.player.angle - ray_angle)

                # projection
                screen_distance = (
                    self.game.config["engine"]["width"]
                    // 2
                    / math.tan(field_of_view / 2)
                )  # TODO Study
                proj_height = screen_distance / (depth + correction)

                color = [
                    color / (1 + depth**5 * correction)
                    for color in self.game.config["engine"]["wall_color_rgb"]
                ]  # TODO Study
                scale = self.game.config["engine"]["width"] // self.amount
                pygame.draw.rect(
                    self.game.screen,
                    color,
                    (
                        ray * scale,
                        (self.game.config["engine"]["height"] // 2)
                        - (proj_height // 2),
                        scale,
                        proj_height,
                    ),
                )

            delta_angle = field_of_view / self.amount
            ray_angle += delta_angle

    def update(self):
        """Update ray caster."""
        self.cast_ray()
