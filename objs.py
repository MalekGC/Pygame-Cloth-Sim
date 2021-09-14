from math import sqrt

from data import *


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def tuple(self):
        return self.x, self.y

    def normalized(self):
        return Vector2(self.x / self.distance(), self.y/self.distance())

    def __iter__(self):
        return self

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, int):
            return Vector2(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x / other, self.y / other)

    def distance(self):
        return sqrt(self.x**2 + self.y**2)

    def distance_between(vect1, vect2):
        return sqrt((vect1.x - vect2.x)**2 + (vect1.y - vect2.y)**2)


class Node:
    def __init__(self, pos, weight=1, locked=False, radius=1):
        self.position = pos
        self.last_pos = pos
        self.weight = weight
        self.locked = locked
        self.radius = radius

    def move(self, dt, external_forces = Vector2(0, 0)):
        if not self.locked:
            next_pos = self.position + (self.position - self.last_pos)
            self.last_pos = self.position
            self.position = next_pos
            gravity_vector = Vector2(0, -gravity)
            self.position += (gravity_vector * (dt / 1000))
            self.position += (external_forces * (dt / 1000))

    def __iter__(self):
        return self


class Line:
    def __init__(self, parents, stretch=0):
        self.parents = parents
        self.stretch = stretch
        self.length = Vector2.distance_between(parents[0].position, parents[1].position)

    def work(self, dt):
        first_node = self.parents[0]
        second_node = self.parents[1]
        current_distance = Vector2.distance_between(first_node.position, second_node.position)
        if current_distance > self.length:
            move_distance = (current_distance - self.length) / 2
            if not first_node.locked:
                move = (second_node.position - first_node.position).normalized() * move_distance
                first_node.position += move
            if not second_node.locked:
                move = (first_node.position - second_node.position).normalized() * move_distance
                second_node.position += move

    def __iter__(self):
        return self


class Camera:
    def __init__(self, position, zoom=10):
        self.position = position
        self.zoom = 1/zoom
        self.center_offset = (Vector2(screen_size[0], screen_size[1]) / 2) / unit * zoom

    def world_to_screen_pos(self, vector2):
        return (vector2 - self.position + self.center_offset) * unit * self.zoom

    def world_to_screen_unit(self, value):
        return value * unit * self.zoom

    def screen_to_world_unit(self, value):
        return value / (unit * self.zoom)

    def screen_to_world_pos(self, position):
        if isinstance(position, tuple):
            x = position[0]
            y = position[1]
        elif isinstance(position, Vector2):
            x = position.x
            y = position.y
        vector = Vector2(x, y)
        screen_size_vector = Vector2(screen_size[0], screen_size[1])
        vector = (vector - (screen_size_vector / 2) + self.world_to_screen_unit(self.position)) / (self.zoom * unit)
        return vector
