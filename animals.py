"""
This class is responsible for animals entity like sheep and wolf.
"""

from random import uniform, choice

class Sheep:
    def __init__(self, init_pos_limit: float = 10.0, move_dist: float = 0.5):
        self.pos_x, self.pos_y = (
            uniform(-abs(init_pos_limit), abs(init_pos_limit))
            for _ in range(2)
        )
        self.move_dist = move_dist

    def move(self) -> None:
        directions: list[tuple[float, float]] = [
            (self.move_dist, 0),   # right
            (-self.move_dist, 0),  # left
            (0, self.move_dist),   # up
            (0, -self.move_dist)   # down
        ]

        dx, dy = choice(directions)
        self.pos_x += dx
        self.pos_y += dy

    def get_position(self) -> tuple[float, float]:
        print(f"Sheep x: {self.pos_x}, y: {self.pos_y}")
        return self.pos_x, self.pos_y


class Wolf:
    def __init__(self, pos_x: float = 0.0, pos_y: float = 0.0,
                 move_dist: float = 1.0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.move_dist = move_dist

    def move(self, sheep_list: list[Sheep]) -> None:

        pass

    def hunt(self):


    def closest_sheep(self, sheep_list: list[Sheep]) -> tuple[Sheep, float]:
        closest_sheep = None
        min_euc_dist: float = float("inf")

        for sheep in sheep_list:
            euc_dist: float = self.euclidean_dist(sheep.pos_x, sheep.pos_y)

            if euc_dist < min_euc_dist:
                min_euc_dist = euc_dist
                closest_sheep = sheep

        return closest_sheep, min_euc_dist

    def euclidean_dist(self, sheep_x: float, sheep_y: float) -> float:
        return ((self.pos_x - sheep_x) ** 2) + ((self.pos_y - sheep_y) ** 2)

    def get_position(self) -> tuple[float, float]:
        print(f"Wolf x: {self.pos_x}, y: {self.pos_y}")
        return self.pos_x, self.pos_y
