from constants import ASTEROID_CHILD_DIVIDER, \
    ASTEROID_CHILD_VELOCITY_MULTIPLIER, \
    ASTEROID_GROW_SPEED, \
    ASTEROID_LIFETIME, \
    ASTEROID_MAX_ROTATION_SPEED, \
    ASTEROID_MIN_RADIUS, \
    ASTEROID_MIN_RADIUS_SPAN, \
    ASTEROID_SHRINK_SPEED, \
    SCORE_MULTIPLIER
from entity import entity
from random import randint, \
    uniform
from asteroid_polygon import asteroid_polygon


class asteroid(entity):
    player = None

    def __init__(self, x, y, radius):
        super().__init__(x, y, 0)
        self.target_radius = radius
        self.radius = radius
        self.max_radius = radius
        self.collideable = True
        self.polygon = asteroid_polygon()
        self.angular_velocity = randint(-ASTEROID_MAX_ROTATION_SPEED,
                                        ASTEROID_MAX_ROTATION_SPEED)
        self.use_physics = True
        self.destroyed_by_player = True
        self.rotation_speed = 0
        self.life_timer = 0

    def update(self):
        if not self.player:
            self.player = self.game.ent_manager.get_entity("player")
            while len(self.game.coll_manager.check_velocity_position(self)) \
                    != 0:
                player_dir = (self.position -
                              self.player.position).normalize()
                self.position += player_dir * self.target_radius
        if self.player:
            self.position += self.player.velocity * self.game.dt * -1
        self.life_timer += self.game.dt
        if self.life_timer > ASTEROID_LIFETIME:
            self.destroyed_by_player = False
            self.game.ent_manager.remove_entity(self)
        if self.radius < self.target_radius:
            self.radius += self.game.dt * ASTEROID_GROW_SPEED
            if self.radius > self.target_radius:
                self.radius = self.target_radius
        if self. radius > self.target_radius:
            self.radius -= self.game.dt * ASTEROID_SHRINK_SPEED
            if self.radius < 1:
                self.destroyed_by_player = True
                self.game.ent_manager.remove_entity(self)

    def on_collision_enter(self, entity, collision_point):
        velocity = (self.position + self.velocity).reflect(entity.position)
        self.velocity = velocity.normalize() * self.velocity.length()

    def on_destroy(self):
        if not self.destroyed_by_player:
            return
        self.player.score += SCORE_MULTIPLIER / self.max_radius
        self.game.ent_manager.get_entity("ui_score_numbers").create_score_text(SCORE_MULTIPLIER / self.max_radius, self.position)
        if self.max_radius < ASTEROID_MIN_RADIUS + ASTEROID_MIN_RADIUS_SPAN:
            return
        child_count = max(2, self.max_radius // ASTEROID_CHILD_DIVIDER)
        half_count = child_count // 2
        entities = []
        cell_size = self.max_radius / half_count
        half_radius = self.max_radius / 2
        for x in range(half_count):
            for y in range(half_count):
                x_pos = self.position.x - half_radius + (x * cell_size)
                y_pos = self.position.y - half_radius + (y * cell_size)
                jitter = cell_size * 0.25
                x_pos += uniform(-jitter, jitter)
                y_pos += uniform(-jitter, jitter)
                child_radius = self.max_radius / (ASTEROID_CHILD_DIVIDER / 2)
                cur_ent = asteroid(x_pos, y_pos, child_radius)
                random_vel = (uniform(-0.5, 0.5), uniform(-0.5, 0.5))
                cur_ent.velocity = (
                    self.velocity +
                    ((cur_ent.position - self.position) *
                        ASTEROID_CHILD_VELOCITY_MULTIPLIER) +
                    random_vel
                )
                entities.append(cur_ent)
        self.game.ent_manager.add_entities(entities)

    def hit(self):
        self.target_radius = 0
        self.use_physics = False
        self.collideable = False
