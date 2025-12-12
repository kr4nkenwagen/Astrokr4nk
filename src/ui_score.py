from constants import LEVEL_LIMIT, \
    SCREEN_HEIGHT, \
    SCREEN_WIDTH, \
    UI_OFFSET, \
    UI_SCORE_HEIGHT, \
    UI_SCORE_WIDTH, \
    UI_COLOR
from entity import entity
from pygame import draw as render, \
    Rect, \
    Vector2


class ui_score(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.frame = Rect((SCREEN_WIDTH // 2) - UI_SCORE_WIDTH // 2,
                          SCREEN_HEIGHT - UI_OFFSET + UI_SCORE_HEIGHT,
                          UI_SCORE_WIDTH, UI_SCORE_HEIGHT)
        self.value_rect = Rect(
            self.frame.x, self.frame.y, 0, self.frame.height)
        self.player = None
        self.value = 0
        self.player_score_position = Vector2(UI_OFFSET, self.frame.y)
        self.is_ui = True

    def update(self):
        if self.player is None:
            self.player = self.game.ent_manager.get_entity("player")
        self.player_score_position.x = \
            UI_OFFSET + \
            ((self.player.score / LEVEL_LIMIT) * UI_SCORE_WIDTH)

    def draw(self):
        render.polygon(self.game.screen,
                       UI_COLOR,
                       [
                           Vector2(self.frame.x, self.frame.y),
                           Vector2(self.frame.x + self.frame.width,
                                   self.frame.y),
                           Vector2(self.frame.x + self.frame.width,
                                   self.frame.y + self.frame.height),
                           Vector2(self.frame.x,
                                   self.frame.y + self.frame.height)
                       ],
                       2)
        render.polygon(self.game.screen,
                       UI_COLOR,
                       [
                           self.player_score_position,
                           Vector2(self.player_score_position.x,
                                   self.player_score_position.y
                                   + UI_SCORE_HEIGHT)
                       ],
                       8)
