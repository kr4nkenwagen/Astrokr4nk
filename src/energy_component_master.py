from entity import entity

class energy_component_master(entity):
    def __init__(self, weapon, shield, thrust):
        super().__init__(0, 0, 0)
        self.max_energy = 6
        self.weapon = weapon
        self.shield = shield
        self.thrust = thrust

    def update(self):
        if self.game.io.is_released("energy_weapon"):
            if self.game.io.is_down("energy_remove"):
                self.remove_energy((self.weapon))
            else:
                self.add_energy(self.weapon)
        if self.game.io.is_released("energy_shield"):
            if self.game.io.is_down("energy_remove"):
                self.remove_energy((self.shield))
            else:
                self.add_energy(self.shield)
        if self.game.io.is_released("energy_thruster"):
            if self.game.io.is_down("energy_remove"):
                self.remove_energy((self.thrust))
            else:
                self.add_energy(self.thrust)



    def add_energy(self, entity):
        if self.get_available_energy() == 0 or entity.get_energy() == entity.max_energy:
            return
        entity.add_energy()

    def remove_energy(self, entity):
        if entity.get_energy() == 0:
            return
        entity.remove_energy()

    def get_available_energy(self):
        energy = 0
        energy += self.weapon.get_energy()
        energy += self.shield.get_energy()
        energy += self.thrust.get_energy()
        return self.max_energy - energy
