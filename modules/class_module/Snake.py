from modules.class_module.Pixel import Pixel
from modules.class_module.GameObject import GameObject
from typing import List, Tuple, Optional
from modules.game_settings import GRID_WIDTH, GRID_HEIGHT


class Snake(GameObject):
    """Snake game object"""

    def __init__(
            self,
            body_color: Optional[Tuple[int, int, int]] = None,
            direction: Optional[Tuple[int, int]] = None,
            on_draw=lambda: None
    ):
        super().__init__(body_color=body_color)
        self.positions: List[Pixel] = list()
        self.__on_draw = on_draw  # external Ui interface func
        self.__direction = direction
        self.__disappeared_tail: Optional[Pixel] = None
        self.reset()

    @property
    def disappeared_tail(self) -> Optional[Pixel]:
        """Get snake's tail property for its erase from Ui interface"""
        return self.__disappeared_tail

    @property
    def direction(self) -> Optional[Tuple[int, int]]:
        """Get snake current direction property"""
        return self.__direction

    def draw(self):
        """Draw snake on Ui interface"""
        self.__on_draw(self)

    def move(self):
        """Calculate snake's positions when its move one step"""
        if self.__direction is None:
            return
        head_column, head_row = self.get_head_position().location
        horizontal_step, vertical_step = self.__direction

        if horizontal_step:
            head_column = (head_column + horizontal_step) % GRID_WIDTH

        if vertical_step:
            head_row = (head_row + vertical_step) % GRID_HEIGHT

        new_head_position = Pixel(
            head_column,
            head_row,
            self.body_color
        )
        self.positions.insert(0, new_head_position)
        self.__disappeared_tail = self.positions.pop()

    def grow_up(self):
        """Calculate snake's positions when its ete apple and grow up"""
        if self.__disappeared_tail is None:
            return
        self.positions.append(self.__disappeared_tail)
        self.__disappeared_tail = None

    def update_direction(self, direction: Tuple[int, int]):
        """Change snake's current direction"""
        if not self.__change_direction_allowed(direction):
            return
        self.__direction = direction

    def reset(self):
        """Reset snake game object"""
        self.positions.clear()
        start_pixel = Pixel(
            column=GRID_WIDTH // 2,
            row=GRID_HEIGHT // 2,
            color=self.body_color
        )
        self.positions.append(start_pixel)

    def get_head_position(self) -> Pixel:
        """Get snake's head position"""
        return self.positions[0]

    def __change_direction_allowed(self, direction: Tuple[int, int]) -> bool:
        if self.__direction is None:
            return True
        current_column_step, current_row_step = self.__direction
        new_column_step, new_row_step = direction

        return (current_column_step != new_column_step
                and current_row_step != new_row_step)
