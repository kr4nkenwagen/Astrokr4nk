from constants import (
    BACKGROUND_COLOR,
    RENDER_UI
)
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
        if not self.game.config.get_bool("debug"):
            self.game.screen.fill(BACKGROUND_COLOR)
        self.game.entities.draw()
        for pol in self.render_queue:
            if pol.show:
                render.polygon(
                    self.game.screen, pol.color, pol.points, pol.thickness)
        if RENDER_UI:
            self.game.entities.draw_ui()
        display.flip()
        self.render_queue.clear()
