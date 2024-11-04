#!/usr/bin/env python
"""Main program that executes simulation from Ex. 2."""
import os
import argparse

from simulation import Simulation


def arg_validator(args):
    if args.rounds <= 0:
        raise ValueError(
            "Number of rounds (-r/--rounds) must be a positive integer.")

    if args.sheep <= 0:
        raise ValueError(
            "Number of sheep (-s/--sheep) must be a positive integer.")

    if args.config and not os.path.isfile(args.config):
        raise FileNotFoundError(
            f"Configuration file '{args.config}' does not exist.")


def arg_parser():
    parser = argparse.ArgumentParser(description="Symulacja wilka i owiec")

    parser.add_argument(
        "-c", "--config", type=str, metavar="FILE",
        help="Auxiliary configuration file, where FILE stands for a filename"
    )

    parser.add_argument(
        "-l", "--log", type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Recording events to a log, where LEVEL stands for a log level "
             "(DEBUG, INFO, WARNING, ERROR, or CRITICAL)"
    )

    parser.add_argument(
        "-r", "--rounds", type=int, default=50,
        help="The maximum number of rounds, where NUM denotes an integer"
    )

    parser.add_argument(
        "-s", "--sheep", type=int, default=15,
        help="The number of sheep, where NUM denotes an integer"
    )

    parser.add_argument(
        "-w", "--wait", action="store_true",
        help="Introducing a pause after displaying basic information about "
             "the status of the simulation at the end of each round until a "
             "key is pressed"
    )

    args = parser.parse_args()

    arg_validator(args)

    return args


def main():
    args = arg_parser()
    simulation = Simulation(
        rounds_number=args.rounds,
        sheep_number=args.sheep,
        do_wait=args.wait,
        config_path=args.config
    )
    simulation.run()


if __name__ == '__main__':
    main()
