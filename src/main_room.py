from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)
from entity import entity
from player import player
from ui import ui
from background_creator import background_creator
from asteroid_spawner import asteroid_spawner
from room import room

class main_room(room):
    def load(self):
        self.game.ent_manager.add_entity(
            player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.game.ent_manager.add_entity(ui())
        self.game.ent_manager.add_entity(background_creator())
        self.game.ent_manager.add_entity(asteroid_spawner())

