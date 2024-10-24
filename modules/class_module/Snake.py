from modules.class_module.Pixel import Pixel
from modules.class_module.GameObject import GameObject
from typing import List, Tuple, Optional


class Snake(GameObject):
    """Snake game object"""

    def __init__(
            self,
            start_pixel: Optional[Pixel] = None,
            direction: Optional[Tuple[int, int]] = None,
            on_draw=lambda: None
    ):
        super().__init__(start_pixel)
        self.positions: List[Optional[Pixel]] = list()
        self.positions.append(start_pixel)
        self.__on_draw = on_draw  # external Ui interface func
        self.__direction = direction
        self.__disappeared_tail: Optional[Pixel] = None

    @property
    def disappeared_tail(self) -> Optional[Pixel]:
        """Get snake's tail property for its erase from Ui interface"""
        return self.__disappeared_tail

    @property
    def direction(self) -> Optional[Tuple[int, int]]:
        """Get snake current direction property"""
        return self.__direction

    def exist(self) -> bool:
        """Check snake exists"""
        return len(self.positions) > 0

    def draw(self):
        """Draw snake on Ui interface"""
        self.__on_draw(self)

    def move(self):
        """Calculate snake's positions when its move one step"""
        if self.__direction is None:
            return
        head_column, head_row = self.positions[0].position
        new_head_position = Pixel(
            head_column + self.__direction[0],
            head_row + self.__direction[1],
            self.body_color
        )
        self.positions.insert(0, new_head_position)
        self.__disappeared_tail = self.positions.pop()

    def grow_up(self):
        """Calculate snake's positions when its ete apple and grow up"""
        self.positions.append(self.__disappeared_tail)
        self.__disappeared_tail = None

    def update_direction(self, direction: Tuple[int, int]):
        """Change snake's current direction"""
        if not self.__change_direction_allowed(direction):
            return
        self.__direction = direction

    def teleport_snake_head(self, new_head: Pixel):
        """
        Change snake's head position
        when snake gets out of Ui interface screen borders
        """
        self.positions[0] = new_head

    def reset(self, start_pixel: Optional[Pixel] = None):
        """Reset snake game object"""
        self.destroy()
        start_position = start_pixel if start_pixel is not None \
            else self.position
        self.position = start_position
        if start_position is not None:
            self.positions.append(start_position)

    def destroy(self):
        """Destroy snake"""
        self.positions.clear()
        self.__disappeared_tail = None

    def get_head_position(self) -> Optional[Tuple[int, int]]:
        """Get snake's head position"""
        if self.positions[0] is None:
            return None
        return self.positions[0].position

    def __change_direction_allowed(self, direction: Tuple[int, int]) -> bool:
        if self.__direction is None:
            return True
        return (self.__direction[0] != direction[0]
                and self.__direction[1] != direction[1])
