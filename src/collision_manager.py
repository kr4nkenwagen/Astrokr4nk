from constants import DEBUG_ENABLED
from pygame import Vector2, \
    draw
from math import degrees, \
    atan2


class collision_manager():
    game = None

    def __init__(self, game):
        self.game = game

    def update(self):
        cur_ent = self.game.entities.first_entity
        while cur_ent is not None:
            if cur_ent.collideable and len(cur_ent.polygon.points) > 0:
                sec_ent = cur_ent.next
                while sec_ent is not None:
                    if sec_ent.collideable and len(sec_ent.polygon.points) > 0:
                        dist = cur_ent.position.distance_to(sec_ent.position)
                        radius = cur_ent.radius + sec_ent.radius
                        if dist < radius:
                            collides, _, _= self.polygons_collide(cur_ent.polygon.points,
                                                     sec_ent.polygon.points)
                            if collides:
                                if sec_ent.id not in cur_ent.has_collided_with:
                                    collision_point = self.get_collision_point(
                                        cur_ent.polygon.points,
                                        sec_ent.polygon.points)
                                    cur_ent.on_collision_enter(
                                        sec_ent, collision_point)
                                    sec_ent.on_collision_enter(
                                        cur_ent, collision_point)
                                else:
                                    cur_ent.on_collision(sec_ent)
                                    sec_ent.on_collision(cur_ent)
                                cur_ent.has_collided_with.add(sec_ent.id)
                                sec_ent.has_collided_with.add(cur_ent.id)
                            else:
                                if sec_ent.id in cur_ent.has_collided_with:
                                    cur_ent.has_collided_with.discard(
                                        sec_ent.id)
                                    cur_ent.on_collision_exit(sec_ent)
                                if cur_ent.id in sec_ent.has_collided_with:
                                    sec_ent.has_collided_with.discard(
                                        cur_ent.id)
                                    sec_ent.on_collision_exit(cur_ent)
                    sec_ent = sec_ent.next
            cur_ent = cur_ent.next


    def polygons_collide(self, pol1, pol2):
        min_overlap = float('inf')
        smallest_axis = None
        for polygon in (pol1, pol2):
            count = len(polygon)
            for i1 in range(count):
                i2 = (i1 + 1) % count
                edge = polygon[i2] - polygon[i1]
                if edge.length_squared() < 1e-12:
                    continue
                axis = Vector2(-edge.y, edge.x)
                axis.normalize_ip()
                min_a, max_a = self.polygon_projection(pol1, axis)
                min_b, max_b = self.polygon_projection(pol2, axis)
                if max_a < min_b or max_b < min_a:
                    return False, None, 0  # NO collision
                overlap = min(max_a, max_b) - max(min_a, min_b)
                if overlap < min_overlap:
                    min_overlap = overlap
                    smallest_axis = axis
        center1 = sum(pol1, Vector2()) / len(pol1)
        center2 = sum(pol2, Vector2()) / len(pol2)
        if (center2 - center1).dot(smallest_axis) < 0:
            smallest_axis = -smallest_axis
        return True, smallest_axis, min_overlap


    def polygon_projection(self, pol, axis):
        dots = [point.dot(axis) for point in pol]
        return min(dots), max(dots)

    def get_collision_point(self, pol1, pol2):
        best = None
        best_dist = float('inf')
        for p1 in pol1:
            for p2 in pol2:
                d = p1.distance_to(p2)
                if d < best_dist:
                    best_dist = d
                    best = (p1 + p2) * 0.5  # midpoint
        return best if best is not None else Vector2()

    def shift_points(self, points, shift, rotation, center):
        transformed_points = []
        for p in points:
            rel = p - center
            rel_rotated = rel.rotate(rotation)
            new_p = center + rel_rotated + shift
            transformed_points.append(new_p)
        return transformed_points


    def check_velocity_position(self, entity):
        if len(entity.polygon.points) == 0:
            return []
        dt = self.game.dt
        results = []
        ent_future_poly = self.shift_points(
            entity.polygon.points,
            entity.velocity * dt,
            entity.angular_velocity * dt,
            entity.position
        )
        cur = entity.next
        while cur is not None:
            if cur.use_physics and len(cur.polygon.points) > 0:
                pos1 = cur.position + cur.velocity * dt
                pos2 = entity.position + entity.velocity * dt
                if pos1.distance_to(pos2) < (cur.radius + entity.radius):
                    cur_future_poly = self.shift_points(
                        cur.polygon.points,
                        cur.velocity * dt,
                        cur.angular_velocity * dt,
                        cur.position
                    )
                    if DEBUG_ENABLED:
                        draw.polygon(self.game.screen, "red", cur_future_poly, 2)
                        draw.polygon(self.game.screen, "blue", ent_future_poly, 2)
                    collides, normal, depth = self.polygons_collide(
                        cur_future_poly, ent_future_poly
                    )
                    if collides:
                        contact_point = self.get_collision_point(
                            cur_future_poly, ent_future_poly
                        )
                        results.append({
                            "other": cur,
                            "normal": normal,
                            "penetration": depth,
                            "point": contact_point
                        })
            cur = cur.next

        return results

    def polygon_line(self, position, rotation, length, thickness):
        half_length = length / 2
        half_thickness = thickness / 2
        points = [
            Vector2(-half_length, -half_thickness),
            Vector2(half_length, -half_thickness),
            Vector2(half_length, half_thickness),
            Vector2(-half_length, half_thickness)
        ]
        points = [position + p.rotate(rotation) for p in points]
        draw.polygon(self.game.screen, "red", points, 20)
        return points

    def polygon_raycast(self, origin, direction, max_distance, step, width):
        distance = 0
        while distance < max_distance:
            ray_center = origin + \
                (Vector2(0, 1).rotate(direction) * distance)
            ray = self.polygon_line(ray_center, direction, step, width)
            cur_ent = self.game.entities.first_entity
            while cur_ent is not None:
                if cur_ent.collideable and len(cur_ent.polygon.points) > 0:
                    if self.polygons_collide(ray, cur_ent.polygon.points):
                        return cur_ent, distance
                cur_ent = cur_ent.next
            distance += step
        return None, distance

    def cone_check(self, origin, direction, angle, length):
        closest_entity = None
        closest_dist = float('inf')
        dir_vec = Vector2(0, 1).rotate(direction)
        cur_ent = self.game.entities.first_entity
        while cur_ent is not None:
            if cur_ent.collideable and len(cur_ent.polygon.points) > 0:
                to_ent = cur_ent.position - origin
                dist = to_ent.length()
                effective_dist = max(dist - cur_ent.radius, 0)
                if effective_dist > length:
                    cur_ent = cur_ent.next
                    continue
                if dist == 0:
                    cur_ent = cur_ent.next
                    continue
                ang_diff = dir_vec.angle_to(to_ent)
                if dist > 0:
                    angular_radius = degrees(
                        atan2(cur_ent.radius, dist))
                else:
                    angular_radius = 0
                if abs(ang_diff) <= (angle / 2 + angular_radius):
                    if effective_dist < closest_dist:
                        closest_entity = cur_ent
                        closest_dist = effective_dist
            cur_ent = cur_ent.next
        if closest_entity is not None:
            return closest_entity, closest_dist
        return None, length
