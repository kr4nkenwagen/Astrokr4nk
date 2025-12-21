from entity import entity
from player_thrust_polygon import player_thrust_polygon


class player_thrust_representation(entity):
    show = False

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.polygon = player_thrust_polygon()
        self.max_radius = radius

    def update(self):
        if self.show:
            if not self.game.audio.is_playing("thrust"):
                self.game.audio.play("thrust", self.max_radius / self.radius, True)
            else:
                self.game.audio.set_channel_audio("thrust", self.max_radius / self.radius)
        else:
            self.game.audio.stop("thrust")
        self.polygon.enabled = self.show
