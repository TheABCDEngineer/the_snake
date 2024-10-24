from modules.class_module.Pixel import Pixel
from typing import Optional, Tuple
from modules.game_settings import BOARD_BACKGROUND_COLOR


class GameObject:
    """Parent class for game objects"""

    def __init__(
            self,
            start_pixel: Optional[Pixel] = None,
            body_color: Optional[Tuple[int, int, int]] = None
    ):
        self.position = start_pixel
        self.body_color = body_color if body_color is not None \
            else BOARD_BACKGROUND_COLOR
        if body_color is None and start_pixel is not None:
            self.body_color = start_pixel.color

    def exist(self) -> bool:
        """Check game object exists"""
        return False

    def draw(self):
        """Draw game object on Ui interface"""
        pass

    def destroy(self):
        """Destroy game object"""
        pass
