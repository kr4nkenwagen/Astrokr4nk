from constants import PLAYER_MAX_SPEED, \
    PLAYER_SHIELD_RADIUS, \
    UI_COLOR, UI_SPEEDOMETER_SECTIONS
from entity import entity
from pygame import Vector2, \
    Rect, \
    Color, \
    draw as render
import random


class ui_speedometer(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.player = None
        self.frame = Rect(0, 0, 5, PLAYER_SHIELD_RADIUS * 2)
        self.value = Rect(0, 0, 5, 0)
        self.color = Color(UI_COLOR)

    def update(self):
        if self.player is None:
            self.player = self.game.ent_manager.get_entity("player")
            return
        if self.player.player_dead:
            return
        fill_ratio = self.player.velocity.length() / PLAYER_MAX_SPEED
        base_x = self.player.position.x + (PLAYER_SHIELD_RADIUS * 1.2)
        base_y = self.player.position.y - PLAYER_SHIELD_RADIUS
        MAX_SHAKE_AMOUNT = 2
        if fill_ratio >= 0.7:
            shake_strength = (fill_ratio - 0.7) / 0.3
            shake_strength = max(0, min(shake_strength, 1))
            shake_amount = MAX_SHAKE_AMOUNT * shake_strength
            shake_x = random.uniform(-shake_amount, shake_amount)
            shake_y = random.uniform(-shake_amount, shake_amount)
        else:
            shake_x = 0
            shake_y = 0
        self.frame.x = base_x + shake_x
        self.frame.y = base_y + shake_y
        self.value.x = self.frame.x
        self.value.height = fill_ratio * self.frame.height
        self.value.y = self.frame.y + (self.frame.height - self.value.height)

    def draw(self):
        if self.player.player_dead:
            return
        render.polygon(self.game.screen,
                       self.color,
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
        render.polygon(self.game.screen,
                       self.color,
                       [
                           Vector2(self.value.x, self.value.y),
                           Vector2(self.value.x + self.value.width,
                                   self.value.y),
                           Vector2(self.value.x + self.value.width,
                                   self.value.y + self.value.height),
                           Vector2(self.value.x,
                                   self.value.y + self.value.height)
                       ],
                       0)
        marker_length = self.frame.width + 4
        marker_thickness = 1

        for i in range(1, UI_SPEEDOMETER_SECTIONS):
            ratio = i / UI_SPEEDOMETER_SECTIONS
            y = self.frame.y + (self.frame.height * (1 - ratio))

            render.line(
                self.game.screen,
                UI_COLOR,
                (self.frame.x, y),
                (self.frame.x + marker_length, y),
                marker_thickness
            )

