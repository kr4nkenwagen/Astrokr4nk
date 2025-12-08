from constants import FONT_BOLD, \
    FONT_SIZE, PLAYER_SHIELD_MAX, \
    SCREEN_HEIGHT, \
    UI_OFFSET, \
    UI_SCORE_HEIGHT, \
    UI_COLOR
from entity import entity
from pygame import Vector2
from pygame.font import Font


class ui_shield(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.radius = 30
        self.position = Vector2(UI_OFFSET, SCREEN_HEIGHT -
                                ((UI_OFFSET * 3) + (UI_SCORE_HEIGHT * 3)))
        self.font = Font(FONT_BOLD, FONT_SIZE)
        self.text = None
        self.shield= None

    def update(self):
        if self.shield is None:
            self.shield = self.game.ent_manager.get_entity("player_shield")
            return
        self.text = self.font.render("shield: " + str(int((self.shield.value / PLAYER_SHIELD_MAX) * 100)) + "%",
                                     True,
                                     UI_COLOR)

    def draw(self):
        if self.text is None:
            return
        self.game.screen.blit(self.text,
                              self.position)
