from constants import PLAYER_SHIELD_COLOR, \
    PLAYER_SHIELD_RIPPLE_RESET_TIME, \
    PLAYER_SHIELD_SEGMENTS, \
    PLAYER_SHIELD_THICKNESS, \
    PLAYER_SHIELD_RIPPLE
from pygame import Vector2
from polygon import polygon
import math
from random import randint

class player_shield_polygon(polygon):
    ripple = 0
    initial_ripple = 0
    ripple_direction = []


    def calc(self, position, rotation, radius, dt):
        unique_vectors = []
        for v in self.ripple_direction:
            if v not in unique_vectors:
                unique_vectors.append(v)
        base_points = []
        for i in range(PLAYER_SHIELD_SEGMENTS):
            angle = (i / PLAYER_SHIELD_SEGMENTS) * 2 * math.pi
            x = position.x + math.cos(angle) * radius + randint(-PLAYER_SHIELD_RIPPLE, PLAYER_SHIELD_RIPPLE)
            y = position.y + math.sin(angle) * radius + randint(-PLAYER_SHIELD_RIPPLE, PLAYER_SHIELD_RIPPLE)
            base_points.append(Vector2(x, y))
        points = []
        for point in base_points:
            offset = Vector2(0, 0)
            for dir_vector in unique_vectors:
                shield_dir = (point - position).normalize()
                dot = shield_dir.dot(dir_vector)
                if dot > 0:
                    weight = dot
                    ripple_amount = randint(-int(self.ripple), int(self.ripple)) * weight
                    offset += dir_vector * ripple_amount
            points.append(point + offset)
        if self.ripple > self.initial_ripple:
            self.initial_ripple = self.ripple
        if self.ripple > 0:
            self.ripple -= (dt / PLAYER_SHIELD_RIPPLE_RESET_TIME) * self.initial_ripple
            if self.ripple <= 0:
                self.initial_ripple = 0
                self.ripple = 0
                self.ripple_direction.clear()
        self.color = PLAYER_SHIELD_COLOR
        self.points = points
        self.thickness = PLAYER_SHIELD_THICKNESS
