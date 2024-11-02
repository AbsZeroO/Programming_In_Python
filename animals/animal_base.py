"""
This class is responsible for animals entity like sheep and wolf.
"""

from abc import ABC, abstractmethod


class AnimalBase(ABC):

    @abstractmethod
    def move(self):
        pass
