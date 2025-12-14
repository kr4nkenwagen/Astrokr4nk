from entity import entity
from player_thrust_polygon import player_thrust_polygon


class player_thrust(entity):
    def __init__(self, x, y):
        self.polygon = player_thrust_polygon()
        super().__init__(x, y, 10)
        self.player = None

    def update(self):
        print("dd")
        if not self.player:
            self.player = self.game.ent_manager.get_entity("player")
        self.polygon.player_velocity = self.player.velocity
        print(self.polygon.player_velocity.length())
