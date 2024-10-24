from typing import Tuple


class Pixel:
    """Logical rectangle which ccorresponds to Ui elementary unit"""

    def __init__(self, column: int, row: int, color: Tuple[int, int, int]):
        self.__column = column
        self.__row = row
        self.__color = color

    @property
    def position(self) -> Tuple[int, int]:
        """Get pixel's position property"""
        return self.__column, self.__row

    @property
    def color(self) -> Tuple[int, int, int]:
        """Get pixel's color property"""
        return self.__color

    def __hash__(self):
        """Class hash"""
        return hash((self.position, self.color))

    def __eq__(self, value):
        """Class equal"""
        if not isinstance(value, type(self)):
            return False
        return value.position == self.position and value.color == self.color
