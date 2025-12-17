
from constants import (
    UI_SCORE_LEVEL_UP_SHAKE_AMOUNT,
    UI_OFFSET,
    UI_SCORE_BAR_BOUNCE_DURATION,
    UI_SCORE_FILL_SPEED,
    UI_SCORE_HEIGHT,
    UI_SCORE_LEVEL_UP_SHAKE_TIMER,
    UI_COLOR,
    LEVEL_LIMIT,
    UI_SCORE_BAR_ZOOM_MAX)
from entity import entity
from pygame import draw as render, Rect, Vector2
import math


class ui_score(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.is_ui = True

    def init(self):
        self.total_width = self.game.screen_width - (UI_OFFSET * 5)
        self.frame = Rect(
            (self.game.screen_width // 2) - self.total_width // 2,
            self.game.screen_height - UI_OFFSET - UI_SCORE_HEIGHT,
            self.total_width,
            UI_SCORE_HEIGHT
        )
        self.fill_width = 0.0
        self.target_fill = 0.0
        self.player = None
        self.last_level = 0
        self.pulse_timer = 0.0
        self.level_up_timer = 0.0
        self.level_up_shake = 0.0
        self.zoom = Vector2(0 ,0)
        self.level_up_bounce_duration = UI_SCORE_BAR_BOUNCE_DURATION

    def update(self):
        dt = self.game.dt
        if self.player is None:
            self.player = self.game.entities.get_entity("player")
            if self.player is None:
                return
            self.last_level = self.player.level
        score_ratio = min(self.player.score / LEVEL_LIMIT, 1.0)
        self.target_fill = score_ratio * self.total_width
        diff = self.target_fill - self.fill_width
        self.fill_width += diff * dt * UI_SCORE_FILL_SPEED# dt lerp
        self.pulse_timer += dt
        if self.player.level > self.last_level:
            self.last_level = self.player.level
            self.level_up_timer = self.level_up_bounce_duration
            self.level_up_shake = UI_SCORE_LEVEL_UP_SHAKE_TIMER
            self.zoom = Vector2(UI_SCORE_BAR_ZOOM_MAX, UI_SCORE_BAR_ZOOM_MAX)
        if self.level_up_timer > 0:
            self.fill_width = 0
            self.level_up_timer -= dt
            if self.level_up_timer < 0:
                self.level_up_timer = 0
        if self.level_up_shake > 0:
            self.level_up_shake -= dt
            self.zoom.x = max((self.level_up_shake / UI_SCORE_BAR_ZOOM_MAX) * dt, 0)
            self.zoom.y = max((self.level_up_shake / UI_SCORE_BAR_ZOOM_MAX) * dt, 0)
            if self.level_up_shake < 0:
                self.level_up_shake = 0

    def draw(self):
        if self.player.player_dead:
            return
        screen = self.game.screen
        overshoot = 1.0
        if self.level_up_timer > 0:
            p = (self.level_up_timer / self.level_up_bounce_duration)
            overshoot = 1.0 + 0.2 * math.sin(p * math.pi)
        shake_offset = 0
        if self.level_up_shake > 0:
            shake_offset = math.sin(self.pulse_timer * UI_SCORE_LEVEL_UP_SHAKE_AMOUNT) * (6 * self.level_up_shake)
        final_fill = self.fill_width * overshoot
        final_fill = min(final_fill, self.total_width)
        pulse_scale = 1.0 + 0.05 * math.sin(self.pulse_timer * 10)
        fill_height = int(self.frame.height * pulse_scale)
        fill_y = self.frame.y + (self.frame.height - fill_height)
        frame = Rect((self.frame.x  - self.zoom.x) + shake_offset, self.frame.y - self.zoom.y, self.frame.width + (self.zoom.x * 2), self.frame.height + (self.zoom.y * 2))
        render.rect(screen, UI_COLOR, frame, 2)
        fill_rect = Rect(
            (self.frame.x - self.zoom.x) + shake_offset,
            fill_y - self.zoom.y,
            final_fill + (self.zoom.x * 2),
            fill_height + (self.zoom.y * 2)
        )
        render.rect(screen, UI_COLOR, fill_rect)
