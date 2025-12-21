from entity import entity
class energy_component(entity):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.current_energy_count = 0;
        self.max_energy = 3

    def add_energy(self):
        self.current_energy_count += 1

    def remove_energy(self):
        if self.current_energy_count <= 0:
            return
        self.current_energy_count -= 0

    def get_energy(self):
        return self.current_energy_count
