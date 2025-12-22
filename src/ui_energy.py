from constants import (
    UI_COLOR,
    UI_DISABLED_COLOR,
    FONT_BOLD,
    UI_ENERGY_BOX_SIZE,
    UI_ENERGY_BOX_SPACING,
    UI_ENERGY_POP_TIME,
    UI_ENERGY_POP_SCALE
)
from entity import entity
from pygame import Rect, Color, draw as render, Vector2
from pygame.font import Font




class ui_energy(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self.weapon = None
        self.shield = None
        self.thrust = None
        self.master = None
        self.box_size = UI_ENERGY_BOX_SIZE
        self.box_spacing = UI_ENERGY_BOX_SPACING
        self.row_spacing = UI_ENERGY_BOX_SPACING + UI_ENERGY_BOX_SIZE
        self.color = Color(UI_COLOR)
        self.disabled_color = Color(UI_DISABLED_COLOR)
        self.is_ui = True
        self.prev_energy = {}
        self.pop_timers = {}

    def init(self):
        self.weapon = self.game.entities.get_entity("player_laser")
        self.shield = self.game.entities.get_entity("player_shield")
        self.thrust = self.game.entities.get_entity("player_thrust_representation")
        self.master = self.game.entities.get_entity("energy_component_master")
        self.font = Font(FONT_BOLD, self.box_size)
        for comp in (self.weapon, self.shield, self.thrust):
            self.prev_energy[comp] = comp.get_energy()
            self.pop_timers[comp] = [0.0] * comp.max_energy

    def update(self):
        if self.shield.player.player_dead:
            return
        self._update_component(self.weapon)
        self._update_component(self.shield)
        self._update_component(self.thrust)
        base_y = 20
        self.rows = []
        self._build_row("W", self.weapon, base_y)
        self._build_row("S", self.shield, base_y + self.row_spacing)
        self._build_row("T", self.thrust, base_y + self.row_spacing * 2)
        self._build_unused_row(
            "U",
            self.master.get_available_energy(),
            self.master.max_energy,
            base_y + self.row_spacing * 3
        )

    def _update_component(self, comp):
        current = comp.get_energy()
        previous = self.prev_energy[comp]
        if current != previous:
            changed_index = max(current, previous) - 1
            if 0 <= changed_index < comp.max_energy:
                self.pop_timers[comp][changed_index] = UI_ENERGY_POP_TIME
        self.prev_energy[comp] = current
        for i in range(comp.max_energy):
            if self.pop_timers[comp][i] > 0:
                self.pop_timers[comp][i] -= self.game.dt
                if self.pop_timers[comp][i] < 0:
                    self.pop_timers[comp][i] = 0

    def _build_row(self, label, energy_component, y):
        boxes = []
        energy = energy_component.get_energy()
        for i in range(energy_component.max_energy):
            x = 60 + i * (self.box_size + self.box_spacing)
            rect = Rect(x, y, self.box_size, self.box_size)
            filled = i < energy
            pop = self.pop_timers[energy_component][i]
            boxes.append((rect, filled, pop))
        text = self.font.render(label, True, UI_COLOR)
        self.rows.append((text, Vector2(20, y), boxes))

    def _build_unused_row(self, label, energy, max_energy, y):
        boxes = []
        for i in range(max_energy):
            x = 60 + i * (self.box_size + self.box_spacing)
            rect = Rect(x, y, self.box_size, self.box_size)
            filled = i < energy
            boxes.append((rect, filled, 0))
        text = self.font.render(label, True, UI_COLOR)
        self.rows.append((text, Vector2(20, y), boxes))

    def draw(self):
        if self.shield.player.player_dead:
            return
        for text, text_pos, boxes in self.rows:
            self.game.screen.blit(text, text_pos)
            for rect, filled, pop in boxes:
                scale = 1.0
                if pop > 0:
                    t = pop / UI_ENERGY_POP_TIME
                    scale = 1.0 + (UI_ENERGY_POP_SCALE - 1.0) * t
                size = int(self.box_size * scale)
                offset = (self.box_size - size) // 2
                r = Rect(
                    rect.x + offset,
                    rect.y + offset,
                    size,
                    size
                )
                color = self.color if filled else self.disabled_color
                render.rect(self.game.screen, color, r, 0)
                render.rect(self.game.screen, self.color, r, 1)

