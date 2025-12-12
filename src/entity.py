import game
from pygame import sprite, \
    Vector2

class entity(sprite.Sprite):
    def __init__(self, x, y, radius):
        self.position = Vector2(x, y)
        self.next = None
        self.game: game = None
        self.parent = None
        self.collideable = False
        self.has_collided_with = set()
        self.has_physics_collided_with = []
        self.id = 0
        self.rotation = 0
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.radius = 0
        self.radius = radius
        self.polygon = None
        self.angular_velocity = 0
        self.use_physics = False
        self.destroyed = False
        self.is_ui = False

    def update(self):
        pass

    def draw(self):
        pass

    def on_collision_enter(self, entity, collision_point):
        pass

    def on_collision(self, entity):
        pass

    def on_collision_exit(self, entity):
        pass

    def on_destroy(self):
        pass

    def on_physics_enter(self, entity):
        pass

    def on_physics(self, entity):
        pass

    def on_physics_exit(self, entity):
        pass


