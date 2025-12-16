from background_creator import background_creator
from room import room
import ui_start_menu
from ui_start_menu import ui_start_menu


class start_room(room):
    def load(self):
        self.game.ent_manager.add_entity(background_creator())
        self.game.ent_manager.add_entity(ui_start_menu())
