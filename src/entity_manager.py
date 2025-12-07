class entity_manager:
    first_entity = None
    id_count = 0

    def __init__(self, game):
        self.game = game
        pass

    def update(self):
        curr_ent = self.first_entity
        while curr_ent is not None:
            if curr_ent.parent is not None:
                curr_ent.position = curr_ent.parent.position.copy()
                curr_ent.rotation = curr_ent.parent.rotation
                curr_ent.radius = curr_ent.parent.radius
            curr_ent.update()
            curr_ent = curr_ent.next

    def draw(self):
        curr_ent = self.first_entity
        while curr_ent is not None:
            if curr_ent.polygon is not None and curr_ent.polygon.enabled:
                curr_ent.polygon.calc(
                    curr_ent.position,
                    curr_ent.rotation,
                    curr_ent.radius,
                    self.game.dt)
                self.game.rendr_manager.add_queue(curr_ent.polygon)
            curr_ent.draw()
            curr_ent = curr_ent.next

    def update_physics(self):
        curr_ent = self.first_entity
        dt = self.game.dt
        while curr_ent is not None:
            if curr_ent.use_physics:
                hits = self.game.coll_manager.check_velocity_position(curr_ent)
                current_hit_entities = [h["other"] for h in hits]
                if len(hits) == 0:
                    curr_ent.position += curr_ent.velocity * dt
                    curr_ent.rotation += curr_ent.angular_velocity * dt
                else:
                    for h in hits:
                        other = h["other"]
                        normal = h["normal"]
                        depth = h["penetration"]
                        self.physics_bounce(curr_ent, other, normal, depth)
                        if other not in curr_ent.has_physics_collided_with:
                            curr_ent.on_physics_enter(other)
                            curr_ent.has_physics_collided_with.append(other)
                    curr_ent.has_physics_collided_with = [
                        e for e in curr_ent.has_physics_collided_with if e in current_hit_entities
                    ]
                    curr_ent.position += curr_ent.velocity * dt
                    curr_ent.rotation += curr_ent.angular_velocity * dt
            curr_ent = curr_ent.next

    def add_entity(self, entity):
        entity.game = self.game
        entity.id = self.id_count
        self.id_count += 1
        if self.first_entity is None:
            self.first_entity = entity
            return entity
        curr_ent = self.first_entity
        while curr_ent.next is not None:
            curr_ent = curr_ent.next
        curr_ent.next = entity
        return entity

    def add_entities(self, entities):
        first_ent = entities[0]
        for i in range(len(entities)):
            entities[i].game = self.game
            entities[i].id = self.id_count
            self.id_count += 1
            if i > 0:
                entities[i - 1].next = entities[i]
        if self.first_entity is None:
            self.first_entity = first_ent
            return first_ent
        curr_ent = self.first_entity
        while curr_ent.next is not None:
            curr_ent = curr_ent.next
        curr_ent.next = first_ent
        return first_ent

    def remove_entity(self, entity):
        if entity is None:
            return
        if self.first_entity.id == entity.id:
            entity.next = self.first_entity.next
            self.first_entity = entity
            entity.destroyed = True
            entity.on_destroy()
            return
        curr_ent = self.first_entity
        while curr_ent is not None:
            if curr_ent.next.id == entity.id:
                curr_ent.next = curr_ent.next.next
                entity.destroyed = True
                entity.on_destroy()
                return
            curr_ent = curr_ent.next

    def get_entity(self, name):
        curr_ent = self.first_entity
        while type(curr_ent).__name__ != name:
            curr_ent = curr_ent.next
        return curr_ent



    def physics_bounce(self, e1, e2, normal, penetration,
                    restitution=0.8, percent=0.8, slop=0.01):
        if normal.length_squared() > 0:
            normal = normal.normalize()
        else:
            return
        rel_vel = e1.velocity - e2.velocity
        vel_norm = rel_vel.dot(normal)
        if vel_norm > 0:
            return
        j = -(1 + restitution) * vel_norm / 2
        impulse = j * normal
        e1.velocity += impulse
        e2.velocity -= impulse
        if penetration > slop:
            correction = normal * ((penetration - slop) * (percent / 2))
            e1.position += correction
            e2.position -= correction
