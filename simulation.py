"""
This class is responsible for managing whole simulation.
"""
import configparser
import logging
import os

from csv import DictWriter
from json import dump

from animals import Sheep, Wolf


class Simulation:
    LOG_LVL_MAP = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    def __init__(self,
                 rounds_number: int,
                 sheep_number: int,
                 do_wait: bool,
                 config_path: str = None,
                 log_lvl: str = None,
                 csv_path: str = "alive.csv",
                 json_path: str = "pos.json"
                 ) -> None:

        logging.basicConfig(
            filename="chase.log",
            filemode="w",
            level=self.LOG_LVL_MAP.get(log_lvl),
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        sheep_range = 10.0
        mv_dist_sheep = 0.5
        mv_dist_wolf = 1.0

        if config_path and os.path.isfile(config_path):
            config = configparser.ConfigParser()
            config.read(config_path)
            sheep_range = config.getfloat("Sheep", "InitPosLimit",
                                          fallback=10.0)
            mv_dist_sheep = config.getfloat("Sheep", "MoveDist",
                                            fallback=0.5)
            mv_dist_wolf = config.getfloat("Wolf", "MoveDist",
                                           fallback=1.0)
            logging.debug(
                f"Loaded configuration values: sheep_range={sheep_range}, "
                f"mv_dist_sheep={mv_dist_sheep}, mv_dist_wolf={mv_dist_wolf}")

        self.rounds_number = rounds_number
        self.sheep_number = sheep_number
        self.do_wait = do_wait
        self.sheep_list = [Sheep(sheep_range, mv_dist_sheep) for _ in
                           range(sheep_number)]

        for i, sheep in enumerate(self.sheep_list, start=1):
            logging.debug(f"Sheep {i}, init position: {sheep.get_position()}")

        logging.info(f"ALL sheep init position determined")

        self.wolf = Wolf(move_dist=mv_dist_wolf)
        self.current_round = 1
        self.csv_path = csv_path
        self.json_path = json_path

        self.init_csv()
        self.init_json()

    def init_csv(self) -> None:
        with open(self.csv_path, "w", newline='') as csv_file:
            fieldnames = ["round_no", "sheep_c"]
            writer = DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()  # Write header only once at the start

    def init_json(self) -> None:
        with open(self.json_path, "w") as json_file:
            json_file.write("[")  # Start a JSON list

    def run(self) -> None:
        while (True):
            logging.info(f"Round number {self.current_round} started.")
            # 1. Moving sheep
            for i, sheep in enumerate(self.sheep_list, start=1):
                if not sheep.is_cought():
                    logging.debug(f"Sheep {i}, direction {sheep.move()}")

            logging.info("All alive sheep moved.")

            # 2. Moving wolf and checking for caught sheep
            caught_or_chased_sheep, dist = (
                self.wolf.closest_sheep(self.sheep_list))

            logging.debug(
                f"Closest sheep is {self.sheep_list.index(
                    caught_or_chased_sheep) + 1} and distans = {dist}")

            self.wolf.move(self.sheep_list)

            if caught_or_chased_sheep.is_cought():
                logging.info(
                    f"Wolf eaten the Sheep "
                    f"{self.sheep_list.index(caught_or_chased_sheep) + 1}")
            else:
                logging.info(
                    f"Wolf is chasing the Sheep "
                    f"{self.sheep_list.index(caught_or_chased_sheep) + 1}")

            if caught_or_chased_sheep.is_cought():
                self.sheep_number -= 1

            logging.info(f"End of round {self.current_round}, "
                         f"alive sheep {self.sheep_number}")

            # 3. Displaying status
            self.display_status(caught_or_chased_sheep)

            # 4. Saving data
            self.save_to_csv()
            self.save_to_json()

            self.current_round += 1

            if self.do_wait:
                os.system('pause')

            if self.current_round > self.rounds_number:
                logging.info("Simulation ended because of rounds")
                break
            elif self.sheep_number == 0:
                logging.info("Simulation ended because of sheep")
                break

        self.finalize_json()

    def display_status(self,
                       caught_or_chased_sheep: Sheep
                       ) -> None:
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

    def save_to_csv(self) -> None:
        with open(self.csv_path, "a", newline='') as csv_file:
            fieldnames = ["round_no", "sheep_c"]
            writer = DictWriter(csv_file, fieldnames=fieldnames)

            writer.writerow({
                "round_no": self.current_round,
                "sheep_c": self.sheep_number
            })
        logging.debug("Round save to .csv")

    def save_to_json(self) -> None:
        with open(self.json_path, "a") as json_file:
            data = {
                "round_no": self.current_round,
                "wolf_pos": self.wolf.get_position(),
                "sheep_pos": [sheep.get_position() for sheep in
                              self.sheep_list
                              if not sheep.is_cought()],
            }
            dump(data, json_file, indent=2)

            if (self.current_round < self.rounds_number
                    and self.sheep_number > 0):
                json_file.write(",")

            logging.debug("Round save to .json")

    def finalize_json(self) -> None:
        with open(self.json_path, "a") as json_file:
            json_file.write("]")
