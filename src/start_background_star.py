from background_star_polygon import background_star_polygon
from constants import BACKGROUND_SPEED_MULTIPLIER
from entity import entity
from pygame import Vector2
from random import uniform


class star_background_star(entity):
    player = None
    layer = 1

    def __init__(self, layer):
        super().__init__(0, 0, 1)
        self.layer = layer
        self.polygon = background_star_polygon(self.layer)
        
    def init(self):
        self.position.x = self.game.screen_width // 2
        self.position.y = 250
        self.collideable = False
        self.velocity = Vector2(uniform(-1, 1), uniform(-1, 1)) * \
            -1 * (self.layer * BACKGROUND_SPEED_MULTIPLIER) * 2000


    def update(self):
        center = Vector2((self.game.screen_width // 2), 250)
        self.position += self.velocity * self.game.dt
        if self.position.x < 0:
            self.position = center
        elif self.position.x > self.game.screen_width:
            self.position = center
        if self.position.y < 0:
            self.position = center
        elif self.position.y > self.game.screen_height:
            self.position = center
        self.polygon.velocity = self.velocity
