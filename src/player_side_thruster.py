from entity import entity
from player_side_thrust_polygon import player_side_thrust_polygon

class player_side_thruster(entity):
    def __init__(self, side, player):
        super().__init__(0, 0, 0)
        self.side = side
        self.player = player
        self.polygon = player_side_thrust_polygon(self.side)

    def update(self):
        self.position = self.player.position
        self.rotation = self.player.rotation
        self.radius = self.player.radius
        self.polygon.player_dead = self.player.player_dead
        if self.game.io.is_down(self.side):
            self.polygon.show = True
        else:
            self.polygon.show = False
