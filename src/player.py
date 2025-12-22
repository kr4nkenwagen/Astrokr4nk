from constants import (
    LEVEL_LIMIT,
    PLAYER_ACCELERATION,
    PLAYER_DEACCELERATION,
    PLAYER_MAX_SPEED,
    PLAYER_RADIUS,
    PLAYER_TURN_SPEED,
    SCREEN_ACCELERATION,
    SCREEN_DEACCELERATION,
    SCREEN_OFFSET_LIMIT
)
from energy_component_master import energy_component_master
from entity import entity
import game
from player_polygon import player_polygon
from laser import laser
from player_thrust_representation import player_thrust_representation
from player_shield import player_shield
from player_laser import player_laser
from pygame import Vector2


class player(entity):
    thrust_representation = None
    shield_representation = None
    laser_representation = None
    energy_master = None
    camera_offset = Vector2(0, 0)
    player_dead = False

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.polygon = player_polygon()
        self.rotation = 180
        self.score = 0
        self.level = 0

    def forward(self):
        return Vector2(0, 1).rotate(self.rotation)

    def rotate(self):
        direction = 0
        if self.game.io.is_down("left"):
            direction += 1
        if self.game.io.is_down("right"):
            direction -= 1
        self.rotation += direction * PLAYER_TURN_SPEED * self.game.dt


    def init(self):
        self.thrust_representation = self.game.entities.add_entity(
            player_thrust_representation(self.position.x,
                                        self.position.y,
                                        10))
        self.shield_representation = self.game.entities.add_entity(player_shield( self.position.x, self.position.y))
        self.thrust_representation.parent = self
        self.laser_representation = self.game.entities.add_entity(player_laser())
        self.energy_master = self.game.entities.add_entity(energy_component_master(self.laser_representation, self.shield_representation, self.thrust_representation))

    def update(self):
        self.rotate()
        if self.score > LEVEL_LIMIT:
            self.score = 0
            self.level += 1
        if self.shield_representation != None:
            self.shield_representation.position.x = self.position.x
            self.shield_representation.position.y = self.position.y

    def on_collision_enter(self, entity, collision_point):
        self.game.game_paused = True
        self.player_dead = True
        self.thrust_representation.polygon.player_dead = True
        self.polygon.flash = True
        print("Player collided with " + str(entity.id))

    def on_collision(self, entity):
        pass

    def on_collision_exit(self, entity):
        print("Player collision with " + str(entity.id) + " ended")
