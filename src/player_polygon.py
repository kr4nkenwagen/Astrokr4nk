from constants import BACKGROUND_COLOR, \
    PLAYER_COLOR, \
    PLAYER_DEATH_BLINK_SPEED, \
    PLAYER_RADIUS, \
    PLAYER_THICKNESS
from pygame import Vector2
from polygon import polygon


class player_polygon(polygon):
    flash = False
    flash_state = False
    flash_timer = 0

    def calc(self, position, rotation, radius, dt):
        self.color = PLAYER_COLOR
        if self.flash:
            self.flash_timer += dt
            if self.flash_timer >= PLAYER_DEATH_BLINK_SPEED:
                self.flash_timer = 0
                self.flash_state = not self.flash_state
            if not self.flash_state:
                self.color = BACKGROUND_COLOR

        right = Vector2(0, 1).rotate(rotation + 90)
        forward = Vector2(0, 1).rotate(rotation)
        r = PLAYER_RADIUS
        a = position + forward * r * 1.3
        b = position - forward * r * 0.3 + right * r * 0.4
        c = position - forward * r * 0.5 + right * r * 1.0
        d = position - forward * r * 0.9 + right * r * 0.3
        e = position - forward * r * 0.9 - right * r * 0.3
        f = position - forward * r * 0.5 - right * r * 1.0
        g = position - forward * r * 0.3 - right * r * 0.4
        self.points = [a, b, c, d, e, f, g]
        self.thickness = PLAYER_THICKNESS
