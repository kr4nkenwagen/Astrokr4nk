from constants import FONT_BOLD, \
    SCREEN_HEIGHT, SCREEN_WIDTH, \
    UI_COLOR
from entity import entity
from pygame import Vector2
from pygame.font import Font


class ui_game_over(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.header_position = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.header_font = Font(FONT_BOLD, 100)
        self.header = None
        self.desc_position = Vector2(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 100)
        self.desc_font = Font(FONT_BOLD, 32)
        self.desc = None
        self.player = None
        self.is_ui = True

    def update(self):
        if self.player is None:
            self.player = self.game.ent_manager.get_entity("player")
            self.header = self.header_font.render("GAME OVER", True, UI_COLOR)
            self.desc = self.desc_font.render("Press any key to try again!", True, UI_COLOR)

    def draw(self):
        if not self.player.player_dead:
            return
        self.game.screen.blit(self.header,
                              self.header_position)
        self.game.screen.blit(self.desc,
                              self.desc_position)
