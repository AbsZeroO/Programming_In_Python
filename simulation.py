"""
This class is responsible for managing whole simulation.
 """

from animals import Sheep, Wolf


class Simulation:

    def __init__(self, rounds_number: int = 50, sheep_number: int = 15,
                 sheep_range: float = 10):
        self.rounds_number = rounds_number
        self.sheep_number = sheep_number
        self.sheep_list = [Sheep(sheep_range) for _ in range(sheep_number)]
        self.wolf = Wolf()
        self.current_round = 1

    def run(self):
        while self.current_round <= self.rounds_number and self.sheep_list:
            # 1. Moving sheep
            for sheep in self.sheep_list:
                sheep.move()

            # 2. Moving wolf and checking for caught sheep
            caught_or_chased_sheep = self.wolf.move(self.sheep_list)

            if caught_or_chased_sheep.is_cought():
                self.sheep_number -= 1

            # 3. Displaying status
            self.display_status(caught_or_chased_sheep)

            # 4. Saving positions
            self.save_positions()

            # Increment round number
            self.current_round += 1

    def display_status(self, caught_or_chased_sheep: Sheep = None):
        wolf_x, wolf_y = self.wolf.get_position()
        print(f"Round: {self.current_round}")
        print(f"Wolf position: {wolf_x: .3f}, {wolf_y: .3f}")
        print(f"Alive sheep: {self.sheep_number}")
        if caught_or_chased_sheep.is_cought():
            sheep_index = self.sheep_list.index(caught_or_chased_sheep) + 1
            print(f"Sheep {sheep_index} has been caught!")
        else:
            sheep_index = self.sheep_list.index(caught_or_chased_sheep) + 1
            print(f"Sheep {sheep_index} is being chased!")

    def save_positions(self):
        pass
