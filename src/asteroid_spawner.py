from asteroid import asteroid
from math import radians
from pygame import Vector2
from random import uniform, \
    choice, \
    randint
from constants import (
    ASTEROID_MAX_RADIUS,
    ASTEROID_MAX_SPEED,
    ASTEROID_MIN_RADIUS,
    ASTEROID_MIN_SPEED,
    ASTEROID_SPAWN_RATE
)
from entity import entity


class asteroid_spawner(entity):
    timer = 0
    player = None

    def __init__(self):
        super().__init__(0, 0, 0)

    def update(self):
        if not self.player:
            self.player = self.game.entities.get_entity("player")
        if self.timer >= ASTEROID_SPAWN_RATE:
            self.timer = 0
            self.spawn_asteroid()
        self.timer += self.game.dt

    def spawn_asteroid(self):
        if not self.player:
            return
        position = self.create_asteroid_position()
        asteroid_ent = self.game.entities.add_entity(
            asteroid(position.x, position.y, self.create_asteroid_radius()))
        asteroid_ent.velocity = self.create_asteroid_velocity(position)
        asteroid_ent.radius = self.create_asteroid_radius()

    def create_asteroid_position(self):
        player_pos = self.player.position
        player_vel = self.player.velocity
        if player_vel.length() > 0:
            player_dir = player_vel.normalize()
            max_angle_offset = radians(60)
            angle_offset = uniform(-max_angle_offset, max_angle_offset)
            spawn_dir = player_dir.rotate_rad(angle_offset)
            distance = max(self.game.screen_width, self.game.screen_height) * 0.6
            position = player_pos + spawn_dir * distance
            position.x = max(0, min(position.x, self.game.screen_width))
            position.y = max(0, min(position.y, self.game.screen_height))
            return position
        else:
            edge = choice(["top", "bottom", "left", "right"])
            position = Vector2(0, 0)
            if edge == "top":
                position.x = randint(0, self.game.screen_width)
            if edge == "bottom":
                position.x = randint(0, self.game.screen_width)
                position.y = self.game.screen_height
            if edge == "left":
                position.y = randint(0, self.game.screen_height)
            if edge == "right":
                position.x = self.game.screen_width
                position.x = randint(0, self.game.screen_height)
            return position

    def create_asteroid_velocity(self, start):
        if not self.player:
            return (Vector2(self.game.screen_width // 2,
                            self.game.screen_height // 2) - start).normalize() * \
                randint(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        return (self.player.position - start).normalize() * \
            randint(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)

    def create_asteroid_radius(self):
        return randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
