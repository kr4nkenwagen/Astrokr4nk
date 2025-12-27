from constants import (
    PLAYER_RADIUS,
    PLAYER_SIDE_THRUSTERS_COLOR,
    PLAYER_SIDE_THRUSTERS_EXPANSION,
    PLAYER_SIDE_THRUSTERS_LENGTH_EXPANDER,
    PLAYER_SIDE_THRUSTERS_MAX_LENGTH,
    PLAYER_SIDE_THRUSTERS_MIN_LENGTH,
    PLAYER_SIDE_THRUSTERS_RADIUS_DIVIDE,
    PLAYER_SIDE_THRUSTERS_UPDATE_RATE,
    PLAYER_SIDE_THRUSTERS_WIDTH
)
from pygame import Vector2
from random import randint
from polygon import polygon

class player_side_thrust_polygon(polygon):
    def __init__(self, side="left"):
        super().__init__()
        self.timer = PLAYER_SIDE_THRUSTERS_UPDATE_RATE
        self.flame = []
        self.side = side

    def calc(self, position, rotation, radius, dt):
        self.color = PLAYER_SIDE_THRUSTERS_COLOR
        self.thickness = 0
        self.timer += dt
        if self.timer > PLAYER_SIDE_THRUSTERS_UPDATE_RATE:
            self.randomize_gas_plume()
            self.timer = 0
        side_x = -(PLAYER_RADIUS // PLAYER_SIDE_THRUSTERS_RADIUS_DIVIDE) if self.side == "right" else PLAYER_RADIUS // 5
        side_offset = Vector2(side_x, PLAYER_RADIUS)
        gas_direction = 170 if self.side == "right" else 10
        self.points = [
            position + (side_offset + p.rotate(gas_direction)).rotate(rotation)
            for p in self.flame
        ]

    def randomize_gas_plume(self):
        self.flame = []
        length = randint(PLAYER_SIDE_THRUSTERS_MIN_LENGTH, PLAYER_SIDE_THRUSTERS_MAX_LENGTH)
        width = PLAYER_SIDE_THRUSTERS_WIDTH
        expansion = PLAYER_SIDE_THRUSTERS_EXPANSION
        mirror = -1 if self.side == "left" else 1
        self.flame.append(Vector2(0, width * mirror))          # Port Top
        self.flame.append(Vector2(length * PLAYER_SIDE_THRUSTERS_LENGTH_EXPANDER, expansion * mirror)) # Spray
        self.flame.append(Vector2(length, 0))                  # Tip
        self.flame.append(Vector2(length * PLAYER_SIDE_THRUSTERS_LENGTH_EXPANDER, -expansion * mirror)) # Spray
        self.flame.append(Vector2(0, -width * mirror))         # Port Bottom
