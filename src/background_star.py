from random import randint
from background_star_polygon import background_star_polygon
from constants import BACKGROUND_SPEED_MULTIPLIER, SCREEN_HEIGHT, SCREEN_WIDTH
from entity import entity


class background_star(entity):
    player = None
    layer = 1

    def __init__(self, layer):
        super().__init__(0, 0, 1)
        self.layer = layer
        self.polygon = background_star_polygon(self.layer)
        self.position.x = randint(0, SCREEN_WIDTH)
        self.position.y = randint(0, SCREEN_HEIGHT)
        self.collideable = False

    def update(self):
        if self.player is None:
            self.player = self.game.ent_manager.get_entity("player")
        self.velocity = (self.player.velocity - self.player.camera_offset) * \
            -1 * (self.layer * BACKGROUND_SPEED_MULTIPLIER)
        self.position += self.player.get_relative_position()
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        self.velocity = self.player.velocity
        self.rotation = self.player.rotation
        self.polygon.velocity = self.velocity
