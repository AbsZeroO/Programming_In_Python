"""
This class is responsible for animals entity like sheep and wolf.
"""

from abc import ABC, abstractmethod
from random import uniform, choice


class AnimalBase(ABC):
    DIRECTIONS: list[tuple[int, int]] = [
        (1, 0),  # right
        (-1, 0),  # left
        (0, 1),  # up
        (0, -1)  # down
    ]

    @abstractmethod
    def move(self) -> None:
        pass

    @abstractmethod
    def get_position(self) -> tuple[float, float]:
        pass


class Sheep(AnimalBase):
    def __init__(self, init_pos_limit: float = 10.0, move_dist: float = 0.5):
        self.pos_x, self.pos_y = (
            uniform(-abs(init_pos_limit), abs(init_pos_limit))
            for _ in range(2)
        )
        self.move_dist = move_dist

    def move(self) -> None:
        direction_x, direction_y = choice(self.DIRECTIONS)

        self.pos_x += self.move_dist * direction_x
        self.pos_y += self.move_dist * direction_y

    def get_position(self) -> tuple[float, float]:
        print(f"Sheep x: {self.pos_x}, y: {self.pos_y}")
        return self.pos_x, self.pos_y


class Wolf(AnimalBase):
    def __init__(self, pos_x: float = 0.0, pos_y: float = 0.0,
                 move_dist: float = 1.0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.move_dist = move_dist

    def move(self) -> None:
        pass

    def get_position(self) -> tuple[float, float]:
        print(f"Wolf x: {self.pos_x}, y: {self.pos_y}")
        return self.pos_x, self.pos_y
