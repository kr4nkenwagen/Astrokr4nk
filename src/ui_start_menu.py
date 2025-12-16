from constants import (
    FONT_BOLD,
    FONT_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UI_COLOR,
    UI_DISABLED_COLOR,
    START_ROOM_SCROLL_SPEED,
    START_ROOM_SHAKE_AMPLITUDE,
    START_ROOM_SHAKE_FREQUENCY,
    START_ROOM_SPACING
)
from pygame import (
    K_s,
    K_w,
    K_SPACE,
    key,
    image,
    transform,
    Vector2
)
from pygame.font import Font
from entity import entity
from math import (
    sin,
    tau
)


class ui_start_menu(entity):
    menu_options = [
        {"text": "Start", "destination": "main_room"},
        {"text": "Quit", "destination": "exit"}
    ]
    current_index = 0
    selected_index = 0

    def __init__(self):
        super().__init__(0, 0, 0)
        self.font = Font(FONT_BOLD, FONT_SIZE)
        self.is_ui = True
        self.shake_time = 0.0
        logo = image.load("src/astrokr4nk.png").convert_alpha()
        self.logo = transform.smoothscale(logo, (500, 250))
        self.logo_rect = logo.get_rect()
        self.logo_rect.x += SCREEN_WIDTH // 2 - 250
        self.logo_rect.y += 100

    def update(self):
        keys = key.get_pressed()
        prev_index = self.selected_index
        if keys[K_w]:
            self.selected_index = max(self.selected_index - 1, 0)
        if keys[K_s]:
            self.selected_index = min(
                self.selected_index + 1,
                len(self.menu_options) - 1
            )
        if keys[K_SPACE]:
            dest = self.menu_options[self.selected_index]["destination"]
            if dest == "exit":
                self.game.game_running = False
                return
            self.game.rm_manager.load_room(dest)
        if prev_index != self.selected_index:
            self.shake_time = 0.0
        diff = self.selected_index - self.current_index
        self.current_index += diff * min(1.0, START_ROOM_SCROLL_SPEED * self.game.dt)
        self.shake_time += self.game.dt

    def draw(self):
        self.game.screen.blit(self.logo, self.logo_rect)
        center_y = SCREEN_HEIGHT // 2
        center_x = SCREEN_WIDTH // 2
        for i, option in enumerate(self.menu_options):
            offset = i - self.current_index
            y = center_y + offset * START_ROOM_SPACING
            is_selected = abs(offset) < 0.01
            color = UI_COLOR if i == self.selected_index else UI_DISABLED_COLOR
            scale = 1.2 if is_selected else 1.0
            surf = self.font.render(option["text"], True, color)
            surf = transform.scale(
                surf,
                (int(surf.get_width() * scale),
                int(surf.get_height() * scale))
            )
            if i == self.selected_index:
                angle = sin(
                    self.shake_time * tau * START_ROOM_SHAKE_FREQUENCY
                ) * START_ROOM_SHAKE_AMPLITUDE
                surf = transform.rotate(surf, angle)

            rect = surf.get_rect(center=(center_x, int(y)))
            self.game.screen.blit(surf, rect)

