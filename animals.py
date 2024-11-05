"""
This file is responsible for animals entity like sheep and wolf.
"""
import logging
from random import uniform, choice
from math import sqrt
from typing import Tuple


class Sheep:
    def __init__(self,
                 init_pos_limit: float = 10.0,
                 move_dist: float = 0.5
                 ) -> None:

        self.pos_x, self.pos_y = (
            uniform(-init_pos_limit, abs(init_pos_limit))
            for _ in range(2)
        )
        self.move_dist = move_dist
        self.caught = False

    def move(self) -> str:
        direction = choice(["n", "s", "e", "w"])  # north south east west
        match direction:
            case "n":
                self.pos_y += self.move_dist
            case "s":
                self.pos_y -= self.move_dist
            case "e":
                self.pos_x += self.move_dist
            case "w":
                self.pos_x -= self.move_dist
        return direction

    def get_position(self) -> tuple[float, float]:
        return self.pos_x, self.pos_y

    def is_cought(self) -> bool:
        return self.caught

    def catch(self) -> None:
        self.caught = True


class Wolf:
    def __init__(self,
                 pos_x: float = 0.0,
                 pos_y: float = 0.0,
                 move_dist: float = 1.0
                 ) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.move_dist = move_dist
        self.chasing = False
        self.chased_sheep = None

    def move(self, sheep_list: list[Sheep]) -> None:
        closest_sheep, dist = self.closest_sheep(sheep_list)

        if dist <= self.move_dist:
            self.hunt(closest_sheep)
            logging.debug(f"Wolf's new position {self.get_position()}")
        else:
            self.chase(closest_sheep, dist)
            logging.debug(f"Wolf's new position {self.get_position()}")

        logging.info("Wolf moved position.")

    def hunt(self,
             closest_sheep: Sheep
             ) -> None:
        self.pos_x, self.pos_y = closest_sheep.get_position()
        closest_sheep.catch()

    def chase(self,
              closest_sheep: Sheep,
              dist: float) -> None:
        sheep_x, sheep_y = closest_sheep.get_position()

        dir_vector = (sheep_x - self.pos_x, sheep_y - self.pos_y)

        if dist > 0:
            unit_vector = (dir_vector[0] / dist, dir_vector[1] / dist)

            self.pos_x += unit_vector[0] * self.move_dist
            self.pos_y += unit_vector[1] * self.move_dist

    def closest_sheep(self,
                      sheep_list: list[Sheep]
                      ) -> tuple[Sheep, float]:
        closest_sheep = None
        min_euc_dist: float = float("inf")

        for sheep in sheep_list:
            sheep_x, sheep_y = sheep.get_position()
            euc_dist: float = self.euclidean_dist(sheep_x, sheep_y)

            if euc_dist < min_euc_dist and not sheep.is_cought():
                min_euc_dist = euc_dist
                closest_sheep = sheep

        return closest_sheep, sqrt(min_euc_dist)

    def euclidean_dist(self,
                       sheep_x: float,
                       sheep_y: float
                       ) -> float:
        return ((self.pos_x - sheep_x) ** 2) + ((self.pos_y - sheep_y) ** 2)

    def get_position(self) -> tuple[float, float]:
        return self.pos_x, self.pos_y

