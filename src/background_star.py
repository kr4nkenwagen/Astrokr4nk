from random import randint
from background_star_polygon import background_star_polygon
from constants import BACKGROUND_SPEED_MULTIPLIER
from entity import entity


class background_star(entity):
    player = None
    layer = 1

    def __init__(self, layer):
        super().__init__(0, 0, 1)
        self.layer = layer
        self.collideable = False
        self.polygon = background_star_polygon(self.layer)

    def init(self):
        self.position.x = randint(0, self.game.screen_width)
        self.position.y = randint(0, self.game.screen_height)

    def update(self):
        if self.player is None:
            self.player = self.game.entities.get_entity("player")
        self.velocity = (self.player.velocity - self.player.camera_offset) * \
            -1 * (self.layer * BACKGROUND_SPEED_MULTIPLIER)
        self.position += self.velocity * self.game.dt
        if self.position.x < 0:
            self.position.x = self.game.screen_width
        elif self.position.x > self.game.screen_width:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = self.game.screen_height
        elif self.position.y > self.game.screen_height:
            self.position.y = 0
        self.velocity = self.player.velocity
        self.rotation = self.player.rotation
        self.polygon.velocity = self.velocity
