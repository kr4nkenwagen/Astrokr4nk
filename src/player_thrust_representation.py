from entity import entity
from player_thrust_polygon import player_thrust_polygon


class player_thrust_representation(entity):
    show = False

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.polygon = player_thrust_polygon()
        self.player = None

    def update(self):
        self.polygon.enabled = self.show
        if not self.player:
            self.player = self.game.ent_manager.get_entity("player")
        self.polygon.player_velocity = self.player.velocity
