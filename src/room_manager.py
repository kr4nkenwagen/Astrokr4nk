from main_room import main_room
from start_room import start_room

class room_manager():
    rooms = [
        main_room(),
        start_room()
    ]
    current_room = None
    game = None

    def __init__(self, game):
        self.game = game
        for room in self.rooms:
            room.game = game

    def load_room(self, name):
        for room in self.rooms:
            if type(room).__name__ == name:
                if self.current_room:
                    self.current_room.unload()
                self.game.entities.purge_entities()
                self.current_room = room
                self.current_room.load()

    def get_current_room_name(self):
        return type(self.current_room).__name__

