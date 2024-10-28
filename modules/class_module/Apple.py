from modules.class_module.Pixel import Pixel
from modules.class_module.GameObject import GameObject
from random import randint
from typing import List, Tuple, Optional
from modules.game_settings import GRID_WIDTH, GRID_HEIGHT


class Apple(GameObject):
    """Apple game object"""

    def __init__(
            self,
            body_color: Optional[Tuple[int, int, int]] = None,
            on_draw=lambda: None
    ):
        super().__init__(body_color=body_color)
        self.__on_draw = on_draw  # external Ui interface func

    def draw(self):
        """Draw apple on Ui interface"""
        self.__on_draw(self)

    def randomize_position(
        self,
        exceptions: List[Pixel] = list()
    ):
        """Set apple with its random position"""
        pixel_column = 0
        pixel_row = 0

        while True:
            pixel_column = randint(0, GRID_WIDTH - 1)
            pixel_row = randint(0, GRID_HEIGHT - 1)
            if self.__check_pixel_position_off_exception(
                pixel_column, pixel_row, exceptions
            ):
                break

        self.position = Pixel(pixel_column, pixel_row, self.body_color)

    def __check_pixel_position_off_exception(
        self,
        pixel_column: int,
        pixel_row: int,
        exceptions: List[Pixel]
    ) -> bool:
        if not exceptions:
            return True
        return Pixel(pixel_column, pixel_row) not in exceptions
