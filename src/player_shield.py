from entity import entity
from pygame import Vector2
from player_shield_polygon import player_shield_polygon
from constants import PLAYER_SHIELD_MAX, \
    PLAYER_SHIELD_RADIUS, \
    PLAYER_SHIELD_RIPPLE_MAX


class player_shield(entity):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_SHIELD_RADIUS)
        self.polygon = player_shield_polygon()
        self.collideable = True
        self.use_physics = True
        self.radius = PLAYER_SHIELD_RADIUS
        self.first_frame = True
        self.player = None
        self.value = PLAYER_SHIELD_MAX

    def update(self):
        if self.first_frame:
            self.player = self.game.ent_manager.get_entity("player")
            self.first_frame = False
        self.velocity = self.player.velocity

    def on_physics_enter(self, entity):
        if self.value > 0:
            #self.value -= 10
            direction = entity.position - self.position
            direction = Vector2.normalize(direction)
            self.polygon.ripple_direction.append(direction)
            self.polygon.ripple = PLAYER_SHIELD_RIPPLE_MAX



