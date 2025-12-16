from random import randint
from background_star import background_star
from start_background_star import star_background_star
from constants import BACKGROUND_LAYERS, \
    BACKGROUND_MAX_STARS, \
    BACKGROUND_MIN_STARS
from entity import entity


class background_creator(entity):
    def __init__(self):
        super().__init__(0, 0, 0)

    def update(self):
        layer = BACKGROUND_LAYERS
        while layer > 0:
            amount = randint(BACKGROUND_MIN_STARS, BACKGROUND_MAX_STARS)
            while amount > 0:
                if self.game.rooms.get_current_room_name() == "start_room":
                    self.game.entities.add_entity(star_background_star(layer))
                else:
                    self.game.entities.add_entity(background_star(layer))
                amount -= 1
            layer -= 1
        self.game.entities.remove_entity(self)
