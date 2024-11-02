#!/usr/bin/env python
"""Main program that executes simulation from Ex. 2."""

from simulation import Simulation
from animals import AnimalBase, Wolf, Sheep


def main():
    test1 = Sheep()
    for i in range(100):
        test1.get_position()
        test1.move()


if __name__ == '__main__':
    main()
