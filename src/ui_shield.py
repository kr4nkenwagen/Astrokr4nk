from constants import PLAYER_SHIELD_MAX, \
    PLAYER_SHIELD_RADIUS, \
    PLAYER_SHIELD_RECHARGE_TIME, \
    UI_COLOR, \
    UI_SHIELD_CHARGE_SHAKE_MULTIPLIER, \
    UI_SHIELD_HIT_SHAKE_MULTIPLIER
from entity import entity
from pygame import Vector2, \
    Rect, \
    draw as render
import random


class ui_shield(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.radius = 30
        self.shield= None
        self.frame = Rect(0, 0, PLAYER_SHIELD_RADIUS * 2, 5)
        self.value = Rect(0, 0, 0, 5)
        self.prev_shield_value = None
        self.damage_shake_timer = 0
        self.damage_shake_duration = 0.3   # seconds

    def update(self):
        if self.shield is None:
            self.shield = self.game.ent_manager.get_entity("player_shield")
            return
        if self.shield.player.player_dead:
            return
        if self.prev_shield_value is None:
            self.prev_shield_value = self.shield.value
        else:
            if self.shield.value < self.prev_shield_value:
                self.damage_shake_timer = self.damage_shake_duration
            self.prev_shield_value = self.shield.value
        base_x = self.shield.position.x - PLAYER_SHIELD_RADIUS
        base_y = self.shield.position.y + (PLAYER_SHIELD_RADIUS * 1.2)
        self.frame.x = base_x
        self.frame.y = base_y
        self.value.x = base_x
        self.value.y = base_y
        if self.shield.value > 0:
            self.value.width = (self.shield.value / PLAYER_SHIELD_MAX) * self.frame.width
        else:
            recharge_progress = self.shield.recharge_timer / PLAYER_SHIELD_RECHARGE_TIME
            self.value.width = recharge_progress * self.frame.width
            shake_amount = UI_SHIELD_CHARGE_SHAKE_MULTIPLIER * recharge_progress
            shake_x = random.uniform(-shake_amount, shake_amount)
            shake_y = random.uniform(-shake_amount, shake_amount)
            self.frame.x += shake_x
            self.frame.y += shake_y
            self.value.x += shake_x
            self.value.y += shake_y
            shake_x = shake_y = 0
        if self.damage_shake_timer > 0:
            self.damage_shake_timer -= self.game.dt
            t = self.damage_shake_timer / self.damage_shake_duration
            shake_strength = UI_SHIELD_HIT_SHAKE_MULTIPLIER * t
            shake_x = random.uniform(-shake_strength, shake_strength)
            shake_y = random.uniform(-shake_strength, shake_strength)
            self.frame.x += shake_x
            self.frame.y += shake_y
            self.value.x += shake_x
            self.value.y += shake_y

    def draw(self):
        if self.shield.player.player_dead:
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
        render.polygon(self.game.screen,
                       UI_COLOR,
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

