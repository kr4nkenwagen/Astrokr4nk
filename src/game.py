from collision_manager import collision_manager
from menu_manager import menu_manager
from room_manager import room_manager
from entity_manager import entity_manager
from render_manager import render_manager
from configuration_manager import configuration_manager
from audio_manager import audio_manager
from input_manager import input_manager
from constants import BACKGROUND_COLOR
from pygame import (
    init,
    display,
    time
)

class game():
    screen = None
    clock = None
    dt = 0
    entities: entity_manager
    render: render_manager
    collision: collision_manager
    config: configuration_manager
    io: input_manager
    audio: audio_manager
    men_manager: menu_manager
    game_running = False
    game_paused = False

    def init(self):
        self.io = input_manager(self)
        self.config = configuration_manager(self)
        self.screen_width = self.config.get_int("width")
        self.screen_height = self.config.get_int("height")
        init()
        self.audio = audio_manager(self)
        self.entities = entity_manager(self)
        self.render = render_manager(self)
        self.collision = collision_manager(self)
        self.men_manager = menu_manager(self)
        self.rooms = room_manager(self)
        self.screen = display.set_mode((self.screen_width, self.screen_height))
        self.clock = time.Clock()
        self.dt = 0
        self.rooms.load_room("start_room")
        self.game_running = True

    def update(self):
        if self.config.get_bool("debug"):
            self.screen.fill(BACKGROUND_COLOR)
        if self.io.is_released("exit"):
            self.game_paused = not self.game_paused
        self.io.update()
        if self.game_paused == False:
            self.entities.update()
            self.entities.update_physics()
            self.collision.update()
        self.men_manager.update()
        self.dt = self.clock.tick() / 1000

    def draw(self):
        self.render.draw()

    def end(self):
        print("game closing")
        self.game_paused = False
