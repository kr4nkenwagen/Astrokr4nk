from constants import (
    FONT_BOLD,
    UI_COLOR
)
from entity import entity
from pygame import Vector2
from pygame.font import Font


class ui_game_over(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.is_ui = True

    def init(self):
        self.header_position = Vector2(self.game.screen_width // 2, self.game.screen_height // 2)
        self.header_font = Font(FONT_BOLD, 100)
        self.header = None
        self.desc_position = Vector2(self.game.screen_width // 2, (self.game.screen_height // 2) + 100)
        self.desc_font = Font(FONT_BOLD, 32)
        self.desc = None
        self.player = self.game.entities.get_entity("player")
        self.header = self.header_font.render("GAME OVER", True, UI_COLOR)
        self.desc = self.desc_font.render("Press <space> to try again!", True, UI_COLOR)

    def draw(self):
        if not self.player.player_dead:
            return
        if self.game.io.is_released("space"):
            self.game.game_paused = False
            self.game.rooms.load_room("main_room")
        self.game.screen.blit(self.header,
                              self.header_position)
        self.game.screen.blit(self.desc,
                              self.desc_position)
