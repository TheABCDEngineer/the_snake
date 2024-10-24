from modules.class_module.Pixel import Pixel
from modules.class_module.GameObject import GameObject
from random import randint
from typing import List, Tuple, Optional


class Apple(GameObject):
    """Apple game object"""

    def __init__(
            self,
            body_color: Optional[Tuple[int, int, int]] = None,
            on_draw=lambda: None
    ):
        super().__init__(body_color=body_color)
        self.__on_draw = on_draw  # external Ui interface func

    def exist(self) -> bool:
        """Check apple exists"""
        return self.position is not None

    def draw(self):
        """Draw apple on Ui interface"""
        self.__on_draw(self)

    def randomize_position(
        self,
        borders: Tuple[int, int],
        exceptions: List[Pixel] = list()
    ):
        """Set apple with its random position"""
        max_column, max_row = borders
        pixel_column = -1
        pixel_row = -1

        while True:
            pixel_column = randint(0, max_column)
            pixel_row = randint(0, max_row)
            if self.__check_pixel_position_off_exception(
                pixel_column, pixel_row, exceptions
            ):
                break

        self.position = Pixel(pixel_column, pixel_row, self.body_color)

    def destroy(self):
        """Destroy game object"""
        self.position = None

    def __check_pixel_position_off_exception(
        self,
        pixel_column: int,
        pixel_row: int,
        exceptions: List[Pixel]
    ) -> bool:
        if exceptions.count == 0:
            return True

        for pixel in exceptions:
            if (pixel_column, pixel_row) == pixel.position:
                return False
        return True
