from entity import entity
from player_thrust_polygon import player_thrust_polygon


class player_thrust_representation(entity):
    show = False

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.polygon = player_thrust_polygon()

    def update(self):
        if self.show:
            self.game.audio.play("thrust")
        else:
            self.game.audio.stop("thrust")

        self.polygon.enabled = self.show
