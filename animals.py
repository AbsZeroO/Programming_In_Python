"""
This file is responsible for animals entity like sheep and wolf.
"""

from random import uniform, choice
from math import sqrt


class Sheep:
    def __init__(self, init_pos_limit: float = 10.0, move_dist: float = 0.5):
        self.pos_x, self.pos_y = (
            uniform(-abs(init_pos_limit), abs(init_pos_limit))
            for _ in range(2)
        )
        self.move_dist = move_dist
        self.caught = False

    def move(self) -> None:
        directions: list[tuple[float, float]] = [
            (self.move_dist, 0.0),  # right
            (-self.move_dist, 0.0),  # left
            (0.0, self.move_dist),  # up
            (0.0, -self.move_dist)  # down
        ]

        dir_x, dir_y = choice(directions)
        self.pos_x += dir_x
        self.pos_y += dir_y

    def get_position(self) -> tuple[float, float]:
        return self.pos_x, self.pos_y

    def is_cought(self):
        return self.caught

    def catch(self):
        self.caught = True


class Wolf:
    def __init__(self, pos_x: float = 0.0, pos_y: float = 0.0,
                 move_dist: float = 1.0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.move_dist = move_dist
        self.chasing = False
        self.chased_sheep = None

    def move(self, sheep_list: list[Sheep]) -> Sheep | None:
        closest_sheep, dist = self.closest_sheep(sheep_list)

        if dist <= self.move_dist:
            self.hunt(closest_sheep)
            return closest_sheep
        else:
            self.chase(closest_sheep, dist)
            return closest_sheep

    def hunt(self, closest_sheep: Sheep) -> None:
        self.pos_x, self.pos_y = closest_sheep.get_position()
        closest_sheep.catch()

    def chase(self, closest_sheep: Sheep, dist):
        sheep_x, sheep_y = closest_sheep.get_position()

        dir_vector = (sheep_x - self.pos_x, sheep_y - self.pos_y)

        if dist > 0:
            unit_vector = (dir_vector[0] / dist, dir_vector[1] / dist)

            self.pos_x += unit_vector[0] * self.move_dist
            self.pos_y += unit_vector[1] * self.move_dist

    def closest_sheep(self, sheep_list: list[Sheep]) -> tuple[Sheep, float]:
        closest_sheep = None
        min_euc_dist: float = float("inf")

        for sheep in sheep_list:
            sheep_x, sheep_y = sheep.get_position()
            euc_dist: float = self.euclidean_dist(sheep_x, sheep_y)

            if euc_dist < min_euc_dist and not sheep.is_cought():
                min_euc_dist = euc_dist
                closest_sheep = sheep

        return closest_sheep, sqrt(min_euc_dist)

    def euclidean_dist(self, sheep_x: float, sheep_y: float) -> float:
        return ((self.pos_x - sheep_x) ** 2) + ((self.pos_y - sheep_y) ** 2)

    def get_position(self) -> tuple[float, float]:
        return self.pos_x, self.pos_y

    def get_chased_sheep(self):
        return self.chased_sheep
