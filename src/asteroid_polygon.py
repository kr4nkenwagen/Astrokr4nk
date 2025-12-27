from random import uniform
from constants import (
    ASTEROID_COLOR,
    ASTEROID_JAGGEDNESS,
    ASTEROID_POINTS,
    ASTEROID_THICKNESS
)
from polygon import polygon
from pygame import Vector2
from math import (
    cos,
    sin,
    pi
)


class asteroid_polygon(polygon):
    def generate_asteroid_shape(self):
        shape = []
        for i in range(ASTEROID_POINTS):
            angle = (i / ASTEROID_POINTS) * 2 * pi
            variation = uniform(-ASTEROID_JAGGEDNESS, ASTEROID_JAGGEDNESS)
            radius = 0.8 + variation
            radius = max(0.3, min(1.0, radius))
            x = cos(angle) * radius
            y = sin(angle) * radius
            shape.append(Vector2(x, y))
        return shape

    def __init__(self):
        super().__init__()
        self.shape = self.generate_asteroid_shape()

    def calc(self, position, rotation, radius, dt):
        self.points = [(point.rotate(rotation) * radius + position)
                       for point in self.shape]
        self.color = ASTEROID_COLOR
        self.thickness = ASTEROID_THICKNESS
