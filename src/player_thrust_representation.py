from constants import (
    PLAYER_MAX_SPEED,
    PLAYER_ACCELERATION,
    PLAYER_DEACCELERATION,
    SCREEN_OFFSET_LIMIT,
    SCREEN_ACCELERATION,
    SCREEN_DEACCELERATION
)
from energy_component import energy_component
from pygame import Vector2
from player_thrust_polygon import player_thrust_polygon


class player_thrust_representation(energy_component):
    show = False

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.polygon = player_thrust_polygon()
        self.max_radius = radius
        self.player = None

    def init(self):
        self.player = self.game.entities.get_entity("player")
        self.polygon.enabled = self.show

    def update(self):
        if self.show:
            if not self.game.audio.is_playing("thrust"):
                self.game.audio.play("thrust", self.max_radius / self.radius, True)
            else:
                self.game.audio.set_channel_audio("thrust", self.max_radius / self.radius)
        else:
            self.game.audio.stop("thrust")
        self.polygon.enabled = self.show
        self.move()

    def accelerate(self):
        if self.get_energy() == 0:
            return
        self.show = True
        self.player.velocity = self.player.velocity.lerp(
            self.player.forward() *
            PLAYER_MAX_SPEED, (PLAYER_ACCELERATION * self.get_energy()) / PLAYER_MAX_SPEED * self.game.dt)
        if self.player.camera_offset.length() < SCREEN_OFFSET_LIMIT:
            self.player.camera_offset = self.player.camera_offset.lerp(self.player.forward() *
                                                         SCREEN_OFFSET_LIMIT,
                                                         SCREEN_ACCELERATION *
                                                         self.game.dt /
                                                         SCREEN_OFFSET_LIMIT)

    def deaccelerate(self):
        self.show = False
        self.player.velocity = self.player.velocity.lerp(Vector2(
            0, 0), PLAYER_DEACCELERATION / PLAYER_MAX_SPEED * self.game.dt)
        if self.player.camera_offset.length() != 0:
            self.player.camera_offset = self.player.camera_offset.lerp(Vector2(0, 0),
                                                         min(
                (SCREEN_DEACCELERATION * self.game.dt) / self.player.camera_offset.length(), 1))

    def move(self):
        if self.game.io.is_down("up"):
            self.accelerate()
        else:
            self.deaccelerate()
        self.player.position = self.player.camera_offset + \
            Vector2(self.game.screen_width // 2, self.game.screen_height // 2)

