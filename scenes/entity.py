from collections import UserDict
from typing import Union


class SubtractableDict(UserDict):
    """A subclass of dict which follows subtraction rules of sets."""

    def __sub__(self, other: Union["SubtractableDict", dict]) -> "SubtractableDict":
        return SubtractableDict({k: v for k, v in self.items() if k not in other})


class Entity:
    """
    The entity class is the definition of an object in the game.

    Door, frame, enemy,..
    Every thing the the player can interact with.
    """

    def __init__(self, position: tuple[int, int], sprite: list[str]):
        self.position = position
        self.sprite = sprite

    def get_to_be_rendered(self) -> SubtractableDict:
        """
        Get the coordinates where this entity is to be rendered, and the characters at those coordinates.

        :return: dict subclass in the form of {(i, j): character}, where (i, j) is the coordinate.
        """
        to_be_rendered = SubtractableDict()
        for i, line in enumerate(self.sprite):
            for j, char in enumerate(line):
                to_be_rendered[i + self.position[0], j + self.position[1]] = char
        return to_be_rendered
