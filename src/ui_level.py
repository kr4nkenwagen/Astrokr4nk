from constants import FONT_BOLD, \
    FONT_SIZE, \
    SCREEN_HEIGHT, \
    UI_OFFSET, \
    UI_SCORE_HEIGHT, \
    UI_COLOR
from entity import entity
from pygame import Vector2
from pygame.font import Font


class ui_level(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.radius = 30
        self.position = Vector2(UI_OFFSET * 2.5, SCREEN_HEIGHT -
                                ((UI_OFFSET * 3) + UI_SCORE_HEIGHT))
        self.font = Font(FONT_BOLD, FONT_SIZE)
        self.text = None
        self.player = None
        self.is_ui = True

    def update(self):
        if self.player is None:
            self.player = self.game.ent_manager.get_entity("player")
            return
        self.text = self.font.render("Level " + str(self.player.level),
                                     True,
                                     UI_COLOR)

    def draw(self):
        if self.text is None or self.player.player_dead:
            return
        self.game.screen.blit(self.text,
                              self.position)
