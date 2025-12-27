from player import player
from ui import ui
from background_creator import background_creator
from asteroid_spawner import asteroid_spawner
from room import room

class main_room(room):
    def load(self):
        self.game.entities.add_entity(
            player(self.game.screen_width // 2, self.game.screen_height // 2))
        print(self.game.entities.id_count)
        self.game.entities.add_entity(ui())
        self.game.entities.add_entity(background_creator())
        self.game.entities.add_entity(asteroid_spawner())
        print(self.game.entities.id_count)
