from constants import FONT_BOLD, \
    SCREEN_HEIGHT, SCREEN_WIDTH, \
    UI_COLOR
from entity import entity
from pygame import Vector2
from pygame.font import Font


class ui_game_over(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.radius = 30
        self.position = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.font = Font(FONT_BOLD, 100)
        self.text = None
        self.player= None

    def update(self):
        if self.player is None:
            self.player = self.game.ent_manager.get_entity("player")
            return
        self.text = self.font.render("GAME OVER", True, UI_COLOR)

    def draw(self):
        if not self.player.player_dead:
            return
        if self.text is None:
            return
        self.game.screen.blit(self.text,
                              self.position)
