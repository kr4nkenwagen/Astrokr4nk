from constants import FONT_BOLD, \
    FONT_SIZE, \
    UI_OFFSET, \
    UI_SCORE_HEIGHT, \
    UI_COLOR
from entity import entity
from pygame import Vector2
from pygame.font import Font


class ui_level(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.is_ui = True

    def init(self):
        self.player = self.game.entities.get_entity("player")
        self.radius = 30
        self.position = Vector2(UI_OFFSET * 2.5, self.game.screen_height -
                                ((UI_OFFSET * 3) + UI_SCORE_HEIGHT))
        self.font = Font(FONT_BOLD, FONT_SIZE)
        self.text = None

    def update(self):
        self.text = self.font.render("Level " + str(self.player.level),
                                     True,
                                     UI_COLOR)

    def draw(self):
        if self.text is None or self.player.player_dead:
            return
        self.game.screen.blit(self.text,
                              self.position)
