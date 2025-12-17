from constants import ASTEROID_EXPLOSION_LIFETIME
from entity import entity
from asteroid_explosion_polygon import asteroid_explosion_polygon


class asteroid_explosion(entity):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.polygon = asteroid_explosion_polygon()
        self.timer = 0

    def update(self):
        self.timer += self.game.dt
        if self.timer > ASTEROID_EXPLOSION_LIFETIME:
            self.game.entities.remove_entity(self)
