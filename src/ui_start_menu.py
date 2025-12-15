
from constants import (
    FONT_BOLD,
    FONT_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UI_COLOR,
    UI_DISABLED_COLOR
)
from pygame import (
    Vector2,
    K_s,
    K_w,
    K_SPACE,
    key,
    transform
)
from pygame.font import Font
from entity import entity


class ui_start_menu(entity):
    menu_options = [
        {"text": "Start", "destination": "main_room"},
        {"text": "Quit", "destination": "exit"}
    ]

    selected_index = 0
    spacing = 50

    def __init__(self):
        super().__init__(0, 0, 0)
        self.font = Font(FONT_BOLD, FONT_SIZE)
        self.is_ui = True

    def update(self):
        keys = key.get_pressed()

        if keys[K_w]:
            self.selected_index = max(self.selected_index - 1, 0)

        if keys[K_s]:
            self.selected_index = min(
                self.selected_index + 1,
                len(self.menu_options) - 1
            )
        if keys[K_SPACE]:
            if self.menu_options[self.selected_index]["destination"] == "exit":
                self.game.game_running = False
                return
            print(self.menu_options[self.selected_index]["destination"])
            self.game.rm_manager.load_room(self.menu_options[self.selected_index]["destination"])

    def draw(self):
        total_height = len(self.menu_options) * self.spacing
        start_y = (SCREEN_HEIGHT - total_height) // 2
        for i, option in enumerate(self.menu_options):
            text = option["text"]
            is_selected = (i == self.selected_index)
            color = UI_DISABLED_COLOR if not is_selected else UI_COLOR
            scale = 1.0 if not is_selected else 1.2
            surf = self.font.render(text, True, color)
            if is_selected:
                surf = transform.scale(
                    surf,
                    (int(surf.get_width() * scale),
                     int(surf.get_height() * scale))
                )
            rect = surf.get_rect()
            rect.centerx = SCREEN_WIDTH // 2
            rect.y = start_y + i * self.spacing
            self.game.screen.blit(surf, rect)

