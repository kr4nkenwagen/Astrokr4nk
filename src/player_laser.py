from energy_component import energy_component
from laser import laser
from constants import PLAYER_FIRE_RATE

class player_laser(energy_component):
    player_fire_rate_counter = 0
    def __init__(self):
        super().__init__(0, 0, 0)
        self.player = None

    def init(self):
        self.player = self.game.entities.get_entity("player")

    def update(self):
        if self.game.io.is_down("shoot"):
            self.shoot()
        self.reload()

    def shoot(self):
        if self.player_fire_rate_counter > 0:
            return
        origin = self.player.position + self.player.forward() * (self.player.radius + 10)
        self.game.entities.add_entity(
            laser(origin.x, origin.y, self.player.rotation))
        self.player_fire_rate_counter += self.game.dt

    def reload(self):
        if self.player_fire_rate_counter > 0:
            self.player_fire_rate_counter += self.game.dt
            if self.player_fire_rate_counter > PLAYER_FIRE_RATE:
                self.player_fire_rate_counter = 0


