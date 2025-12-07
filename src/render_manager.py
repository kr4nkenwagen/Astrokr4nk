from constants import BACKGROUND_COLOR, \
    DEBUG_ENABLED
from pygame import draw as render, \
    display

class render_manager():
    game = None
    render_queue = []

    def __init__(self, game):
        self.game = game

    def add_queue(self, polygon):
        self.render_queue.append(polygon)

    def draw(self):
        if not DEBUG_ENABLED:
            self.game.screen.fill(BACKGROUND_COLOR)
        self.game.ent_manager.draw()
        for pol in self.render_queue:
            if pol.show:
                render.polygon(
                    self.game.screen, pol.color, pol.points, pol.thickness)
        display.flip()
        self.render_queue.clear()
