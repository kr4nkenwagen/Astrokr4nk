from constants import LASER_LIFETIME, \
    LASER_MAX_LENGTH, \
    LASER_AIM_ASSIST_DEGREE
from asteroid_explosion import asteroid_explosion
from energy_component import energy_component
from player_shot_polygon import player_shot_polygon
from pygame import Vector2


class laser(energy_component):
    def __init__(self, x, y, rotation):
        super().__init__(x, y, 1)
        self.rotation = rotation
        self.polygon = player_shot_polygon()
        self.lifetime = 0

    def init(self):
        distance = LASER_MAX_LENGTH
        target, distance = self.game.collision.cone_check(
            self.position,
            self.rotation,
            LASER_AIM_ASSIST_DEGREE,
            distance)
        if target is not None:
            direction_to_target = (
                target.position - self.position).normalize()
            forward_vec = Vector2(0, 1).rotate(self.rotation)
            angle_diff = forward_vec.angle_to(direction_to_target)
            self.rotation += angle_diff
        self.position = self.position + \
            (Vector2(0, 1).rotate(self.rotation) * distance / 2)
        self.polygon.length = distance
        if target is not None:
            if target.__class__.__name__ == "asteroid":
                explosion_position = self.position + \
                    (Vector2(0, 1).rotate(self.rotation) *
                        distance / 2)
                self.game.entities.add_entity(asteroid_explosion(
                    explosion_position.x, explosion_position.y, 30))
                target.hit()
        self.game.audio.play("laser")

    def update(self):
        self.lifetime += self.game.dt
        if self.lifetime > LASER_LIFETIME:
            self.game.entities.remove_entity(self)
