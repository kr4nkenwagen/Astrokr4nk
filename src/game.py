from asteroid_spawner import asteroid_spawner
from background_creator import background_creator
from collision_manager import collision_manager
from menu_manager import menu_manager
from constants import SCREEN_WIDTH, \
    SCREEN_HEIGHT, \
    DEBUG_ENABLED, \
    BACKGROUND_COLOR
from entity_manager import entity_manager
from player import player
from pygame import init, \
    display, \
    time, \
    K_ESCAPE, \
    key


from render_manager import render_manager
from ui import ui

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
        self.ent_manager = entity_manager(self)
        self.rendr_manager = render_manager(self)
        self.coll_manager = collision_manager(self)
        self.men_manager = menu_manager(self)
        self.screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = time.Clock()
        self.dt = 0
        self.ent_manager.add_entity(
            player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.ent_manager.add_entity(ui())
        self.ent_manager.add_entity(background_creator())
        self.ent_manager.add_entity(asteroid_spawner())
        self.game_running = True

    def update(self):
        if DEBUG_ENABLED:
            self.screen.fill(BACKGROUND_COLOR)
        keys = key.get_pressed()
        if keys[K_ESCAPE]:
            self.game_paused = not self.game_paused
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
