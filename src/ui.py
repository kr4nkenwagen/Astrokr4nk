from entity import entity
from ui_game_over import ui_game_over
from ui_score import ui_score
from ui_level import ui_level
from ui_shield import ui_shield
from ui_speedometer import ui_speedometer
from ui_score_numbers import ui_score_numbers
from ui_energy import ui_energy


class ui(entity):
    def __init__(self):
        super().__init__(0, 0, 0)
        self. initialized = False

    def update(self):
        if self.initialized is False:
            self.game.entities.add_entity(ui_score())
            self.game.entities.add_entity(ui_level())
            self.game.entities.add_entity(ui_shield())
            self.game.entities.add_entity(ui_speedometer())
            self.game.entities.add_entity(ui_game_over())
            self.game.entities.add_entity(ui_score_numbers())
            self.game.entities.add_entity(ui_energy())
            self.initialized = True
