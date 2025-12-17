from constants import (
    UI_COLOR,
    FONT_BOLD,
    UI_SCORE_MAX_SCALE,
    UI_SCORE_POP_TIME,
    UI_SCORE_SHAKE_DEGREE,
    UI_SCORE_TOTAL_TIME,
    UI_SCORE_BASE_SIZE,
    UI_SCORE_LINGER_TIME,
    UI_SCORE_SHAKE_TIME
)
from entity import entity
from pygame import transform
from pygame import Color
from pygame.font import Font
import math


class ui_score_numbers(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.color = Color(UI_COLOR)
        self.text_stack = []
        self.is_ui = True
        self.player = None

    def update(self):
        if not self.player:
            self.player = self.game.entities.get_entity("player")
        dt = self.game.dt

        for text in self.text_stack[:]:
            text["timer"] += dt
            t = text["timer"]
            if t >= UI_SCORE_TOTAL_TIME:
                self.text_stack.remove(text)
                continue

            if t < UI_SCORE_POP_TIME:
                p = t / UI_SCORE_POP_TIME
                size_mult = text["max_scale"] * (p ** 0.35)
            else:
                size_mult = text["max_scale"]
            if t < UI_SCORE_POP_TIME:
                rotation = 0
            elif t < UI_SCORE_POP_TIME + UI_SCORE_LINGER_TIME:
                p = (t - UI_SCORE_POP_TIME) / UI_SCORE_LINGER_TIME
                rotation = math.sin(p * 16 * math.pi) * text["shake_deg"]
            else:
                p = (t - (UI_SCORE_POP_TIME + UI_SCORE_LINGER_TIME)) / (UI_SCORE_TOTAL_TIME - (UI_SCORE_POP_TIME + UI_SCORE_LINGER_TIME))
                rotation = math.sin(p * 20 * math.pi) * text["shake_deg"] * math.exp(-p * 2)
            text["rotation"] = rotation
            if t < UI_SCORE_SHAKE_TIME:
                alpha = 255
            else:
                fade_p = (t - UI_SCORE_SHAKE_TIME) / (UI_SCORE_TOTAL_TIME - UI_SCORE_SHAKE_TIME)
                alpha = max(0, 255 * (1 - fade_p))
            size_pixels = max(1, int(text["base_size"] * size_mult))
            font = Font(FONT_BOLD, size_pixels)
            surf = font.render(text["value"], True, self.color)
            surf.set_alpha(int(alpha))
            text["surface"] = surf
            text["position"] += self.player.velocity * dt * -1
            text["position"].y -= 20 * dt

    def draw(self):
        for text in self.text_stack:
            if text["surface"] is None:
                continue

            rotated = transform.rotate(text["surface"], text["rotation"])
            rect = rotated.get_rect(center=text["position"])
            self.game.screen.blit(rotated, rect)

    def create_score_text(self, value, position):
        self.text_stack.append({
            "value": f"+{int(value * 100)}",
            "position": position.copy(),
            "timer": 0,
            "base_size": UI_SCORE_BASE_SIZE,
            "max_scale": UI_SCORE_MAX_SCALE,      # stays this big permanently
            "shake_deg": UI_SCORE_SHAKE_DEGREE,       # wobble strength
            "surface": None,
            "rotation": 0,
        })
