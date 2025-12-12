from constants import PLAYER_MAX_SPEED, \
    SCREEN_HEIGHT, \
    SCREEN_WIDTH, \
    UI_COLOR, UI_OFFSET, \
    UI_SPEEDOMETER_MAX_SHAKE_AMOUNT, \
    UI_SPEEDOMETER_SECTIONS, \
    FONT_BOLD, \
    FONT_SIZE, \
    UI_COLOR_RED, UI_SPEEDOMETER_SHAKE_THRESHOLD
from entity import entity
from pygame import Vector2, \
    Rect, \
    Color, \
    draw as render
import random
from pygame.font import Font


class ui_speedometer(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.player = None
        self.frame = Rect(SCREEN_WIDTH - 30 - UI_OFFSET, UI_OFFSET, 30, SCREEN_HEIGHT - (UI_OFFSET * 2))
        self.value = Rect(SCREEN_WIDTH - 30 - UI_OFFSET, UI_OFFSET, 30, 0)
        self.color = Color(UI_COLOR)
        self.font = Font(FONT_BOLD, FONT_SIZE)
        self.text = None
        self.is_ui = True


    def update(self):
        if self.player is None:
            self.player = self.game.ent_manager.get_entity("player")
            return
        if self.player.player_dead:
            return
        fill_ratio = self.player.velocity.length() / PLAYER_MAX_SPEED
        base_x = SCREEN_WIDTH - 30 - UI_OFFSET
        base_y = UI_OFFSET
        if fill_ratio >= UI_SPEEDOMETER_SHAKE_THRESHOLD:
            self.color = Color(UI_COLOR).lerp(UI_COLOR_RED, fill_ratio)
            shake_strength = (fill_ratio - UI_SPEEDOMETER_SHAKE_THRESHOLD) / (1 - UI_SPEEDOMETER_SHAKE_THRESHOLD)
            shake_strength = max(0, min(shake_strength, 1))
            shake_amount = UI_SPEEDOMETER_MAX_SHAKE_AMOUNT * shake_strength
            shake_x = random.uniform(-shake_amount, shake_amount)
            shake_y = random.uniform(-shake_amount, shake_amount)
        else:
            shake_x = 0
            shake_y = 0
            self.color = UI_COLOR
        self.frame.x = base_x + shake_x
        self.frame.y = base_y + shake_y
        self.value.x = self.frame.x
        self.value.height = fill_ratio * self.frame.height
        self.value.y = self.frame.y + (self.frame.height - self.value.height)
        self.text = self.font.render(str(int(self.player.velocity.length())),
                                     True,
                                     self.color)



    def draw(self):
        if self.player.player_dead:
            return
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
                       1)


        for i in range(1, UI_SPEEDOMETER_SECTIONS):
            ratio = i / UI_SPEEDOMETER_SECTIONS
            y = self.frame.y + (self.frame.height * (1 - ratio))

            render.line(
                self.game.screen,
                UI_COLOR,
                (self.frame.x, y),
                (self.frame.x + self.frame.width, y),
               2
            )

        if not self.text:
            return
        text_width = self.text.get_width() if self.text.get_width() > 80 else 80
        self.game.screen.blit(self.text,
                              (self.value.x - text_width, self.value.y - self.text.get_height()))
        render.line(
            self.game.screen,
            self.color,
            (self.frame.x - text_width, self.value.y),
            (self.frame.x + self.frame.width, self.value.y),
            2
        )

