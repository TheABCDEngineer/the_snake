from typing import Tuple
from modules.game_settings import BOARD_BACKGROUND_COLOR


class Pixel:
    """Logical rectangle which corresponds to Ui elementary unit"""

    def __init__(
            self,
            column: int,
            row: int,
            color: Tuple[int, int, int] = BOARD_BACKGROUND_COLOR
    ):
        self.__column = column
        self.__row = row
        self.__color = color

    @property
    def location(self) -> Tuple[int, int]:
        """Get pixel's position property"""
        return self.__column, self.__row

    @property
    def color(self) -> Tuple[int, int, int]:
        """Get pixel's color property"""
        return self.__color

    def __eq__(self, value):
        """Class equal"""
        if not isinstance(value, type(self)):
            return False
        return value.location == self.location
