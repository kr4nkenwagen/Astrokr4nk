from constants import PLAYER_SHIELD_MAX, \
    PLAYER_SHIELD_RADIUS, \
    PLAYER_SHIELD_RECHARGE_TIME, \
    UI_COLOR, \
    UI_COLOR_RED, \
    UI_DISABLED_COLOR, \
    UI_SHIELD_CHARGE_SHAKE_MULTIPLIER, \
    UI_SHIELD_HIT_SHAKE_MULTIPLIER, \
    UI_SHIELD_HIT_SHAKE_TIME
from entity import entity
from pygame import Vector2, \
    Rect, \
    Color, \
    draw as render
import random


class ui_shield(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.radius = 30
        self.shield= None
        self.frame = Rect(0, 0, PLAYER_SHIELD_RADIUS * 2, 5)
        self.value = Rect(0, 0, 0, 5)
        self.charge = Rect(0, 0, 0, 5)
        self.prev_shield_value = None
        self.damage_shake_timer = 0
        self.color = Color(UI_COLOR)
        self.is_ui = True

    def init(self):
        self.shield = self.game.entities.get_entity("player_shield")

    def update(self):
        if self.shield.player.player_dead or self.shield.get_energy() == 0:
            return
        if self.prev_shield_value is None:
            self.prev_shield_value = self.shield.value
        else:
            if self.shield.value < self.prev_shield_value:
                self.damage_shake_timer = UI_SHIELD_HIT_SHAKE_TIME
                self.color = Color(UI_COLOR_RED)
            self.prev_shield_value = self.shield.value
        base_x = self.shield.position.x - PLAYER_SHIELD_RADIUS
        base_y = self.shield.position.y + (PLAYER_SHIELD_RADIUS * 1.2)
        self.frame.x = base_x
        self.frame.y = base_y
        self.value.x = base_x
        self.value.y = base_y
        self.charge.x = base_x
        self.charge.y = base_y
        if self.shield.value > 0:
            self.color = Color(UI_COLOR)
            self.value.width = (self.shield.value / PLAYER_SHIELD_MAX) * self.frame.width
            recharge_progress = self.shield.recharge_timer / PLAYER_SHIELD_RECHARGE_TIME
            if recharge_progress > 0:
                self.charge.width = recharge_progress * (self.frame.width - self.value.width)
                self.charge.x += self.value.width
            else:
                self.charge.width = 0
        else:
            self.color = Color(UI_DISABLED_COLOR)
            recharge_progress = self.shield.recharge_timer / PLAYER_SHIELD_RECHARGE_TIME
            self.value.width = recharge_progress * self.frame.width
            shake_amount = UI_SHIELD_CHARGE_SHAKE_MULTIPLIER * recharge_progress
            shake_x = random.uniform(-shake_amount, shake_amount)
            shake_y = random.uniform(-shake_amount, shake_amount)
            self.frame.x += shake_x
            self.frame.y += shake_y
            self.charge.x += shake_x
            self.charge.y += shake_y
            self.value.x += shake_x
            self.value.y += shake_y
            shake_x = shake_y = 0
        if self.damage_shake_timer > 0:
            self.damage_shake_timer -= self.game.dt
            t = self.damage_shake_timer / UI_SHIELD_HIT_SHAKE_TIME
            if t > 0:
                self.color = Color(UI_COLOR).lerp(UI_COLOR_RED, t)
            shake_strength = UI_SHIELD_HIT_SHAKE_MULTIPLIER * t
            shake_x = random.uniform(-shake_strength, shake_strength)
            shake_y = random.uniform(-shake_strength, shake_strength)
            self.frame.x += shake_x
            self.frame.y += shake_y
            self.charge.x += shake_x
            self.charge.y += shake_y
            self.value.x += shake_x
            self.value.y += shake_y

    def draw(self):
        if self.shield.player.player_dead or self.shield.get_energy() == 0:
            return
        if self.charge.width > 0:
            render.polygon(self.game.screen,
                Color(UI_DISABLED_COLOR),
                [
                    Vector2(self.charge.x, self.charge.y),
                    Vector2(self.charge.x + self.charge.width,
                            self.charge.y),
                    Vector2(self.charge.x + self.charge.width,
                            self.charge.y + self.charge.height),
                    Vector2(self.charge.x,
                            self.charge.y + self.charge.height)
                ],
                0)
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
