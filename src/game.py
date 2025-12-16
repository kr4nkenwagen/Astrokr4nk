from collision_manager import collision_manager
from menu_manager import menu_manager
from room_manager import room_manager
from entity_manager import entity_manager
from render_manager import render_manager
from input_manager import input_manager
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    DEBUG_ENABLED,
    BACKGROUND_COLOR
)
from pygame import (
    init,
    display,
    time,
    K_ESCAPE,
    K_RETURN,
    K_SPACE,
    K_w,
    K_a,
    K_s,
    K_d
)

class game():
    screen = None
    clock = None
    dt = 0
    ent_manager: entity_manager
    rendr_manager: render_manager
    coll_manager: collision_manager
    men_manager: menu_manager
    game_running = False
    game_paused = False

    def init(self):
        print("Starting Asteroids!")
        print("Screen width: " + str(SCREEN_WIDTH))
        print("Screen height: " + str(SCREEN_HEIGHT))
        init()
        self.io = input_manager(self)
        self.io.register_keybind("up", K_w)
        self.io.register_keybind("down", K_s)
        self.io.register_keybind("left", K_a)
        self.io.register_keybind("right", K_d)
        self.io.register_keybind("shoot", K_SPACE)
        self.io.register_keybind("enter", K_RETURN)
        self.io.register_keybind("exit", K_ESCAPE)

        self.ent_manager = entity_manager(self)
        self.rendr_manager = render_manager(self)
        self.coll_manager = collision_manager(self)
        self.men_manager = menu_manager(self)
        self.rm_manager = room_manager(self)
        self.screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = time.Clock()
        self.dt = 0
        self.rm_manager.load_room("start_room")
        self.game_running = True

    def update(self):
        if DEBUG_ENABLED:
            self.screen.fill(BACKGROUND_COLOR)
        if self.io.is_released("exit"):
            self.game_paused = not self.game_paused
        self.io.update()
        if self.game_paused == False:
            self.ent_manager.update()
            self.ent_manager.update_physics()
            self.coll_manager.update()
        self.men_manager.update()
        self.dt = self.clock.tick() / 1000

    def draw(self):
        self.rendr_manager.draw()

    def end(self):
        print("game closing")
        self.game_paused = False
