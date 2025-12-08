from entity import entity
from pygame import Vector2
from player_shield_polygon import player_shield_polygon
from constants import PLAYER_SHIELD_MAX, \
    PLAYER_SHIELD_RADIUS, \
    PLAYER_SHIELD_RIPPLE_MAX, \
    PLAYER_SHIELD_COOLDOWN


class player_shield(entity):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_SHIELD_RADIUS)
        self.polygon = player_shield_polygon()
        self.collideable = True
        self.use_physics = True
        self.radius = PLAYER_SHIELD_RADIUS
        self.player = None
        self.value = PLAYER_SHIELD_MAX
        self.collision_list = []

    def update(self):
        if not self.player:
            self.player = self.game.ent_manager.get_entity("player")
        self.velocity = self.player.velocity
        if self.value == 0:
            self.polygon.show = False
            self.collideable = False
            self.use_physics = False
            self.player.collideable = True
        else:
            self.polygon.show = True
            self.collideable = True
            self.use_physics = True
            self.player.collideable = False
        for timer in self.collision_list[:]:
            if timer["timer"] > 0:
                timer["timer"] -= self.game.dt

    def on_physics_enter(self, entity):
        if self.value > 0:
            self.collision_list.append({"id": entity.id, "timer": PLAYER_SHIELD_COOLDOWN})
            self.value -= 10
            direction = entity.position - self.position
            direction = Vector2.normalize(direction)
            self.polygon.ripple_direction.append(direction)
            self.polygon.ripple = PLAYER_SHIELD_RIPPLE_MAX

    def on_physics(self, entity):
        if self.value > 0:
            direction = entity.position - self.position
            direction = Vector2.normalize(direction)
            self.polygon.ripple_direction.append(direction)
            self.polygon.ripple = PLAYER_SHIELD_RIPPLE_MAX
        for e in self.collision_list:
            if e["id"] == entity.id:
                if e["timer"] <= 0:
                    self.value -= 10
                    e["timer"] = PLAYER_SHIELD_COOLDOWN


    def on_physics_exit(self, entity):
        for e in self.collision_list:
            if e["id"] == entity.id:
                self.collision_list.remove(e)


