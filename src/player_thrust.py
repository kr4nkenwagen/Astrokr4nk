from entity import entity
from player_thrust_polygon import player_thrust_polygon


class player_thrust(entity):
    def __init__(self, x, y):
        self.polygon = player_thrust_polygon()
        super().__init__(x, y, 10)

