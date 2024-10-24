import pygame
from modules.class_module.Pixel import Pixel
from typing import List, Tuple, Optional
from modules.game_settings import UP, DOWN, LEFT, RIGHT


class GameScreen:
    """UI interface add-on class to pygame lib"""

    def __init__(
        self,
        width: int,
        height: int,
        grid_size: int,
        background_color: Tuple[int, int, int],
        title: str
    ):
        self.__view = pygame.display.set_mode((width, height), 0, 32)
        self.__background_color = background_color
        self.__grid_size = grid_size
        self.__grid_width = width // grid_size
        self.__grid_height = height // grid_size
        self.__clock = pygame.time.Clock()
        self.__is_display_update_allow: bool = False

        # pixel's colors cashe to optimize Ui core usage
        self.__cashe: List[List[Optional[Tuple[int, int, int]]]] = list()

        # callback external func
        # which running when user change snake direction with keyboard
        self.__on_direction_change_callback = lambda direction: None

        # callback external func which running when user quit game
        self.__on_game_quit_callback = lambda: None

        pygame.display.set_caption(title)
        pygame.init()
        self.reset()

    @property
    def borders(self) -> Tuple[int, int]:
        """Get screen's borders property"""
        return self.__grid_width - 1, self.__grid_height - 1

    def set_on_direction_change(self, fun):
        """Set external func which runing when user change snake's dirction"""
        self.__on_direction_change_callback = fun

    def set_on_game_quit(self, fun):
        """Set external func which runing when user quit the game"""
        self.__on_game_quit_callback = fun

    def slow(self, framerate: float):
        """
        Pause game proccess using pygame.clock
        with handle user events
        """
        self.__clock.tick(framerate)
        self.__check_events()

    def draw(
        self,
        pixel: Optional[Pixel] = None,
        pixels: Optional[List[Pixel]] = None,
        erase: bool = False
    ):
        """Draw/erase pixels of game objects with pygame.draw"""
        if pixel is None and pixels is None:
            return

        if pixel is not None:
            if not erase:
                self.__draw_pixel(pixel)
            if erase:
                self.__erase_pixel(pixel)

        if pixels is not None:
            if pixels.count == 0:
                return
            if not erase:
                self.__draw_pixels(pixels)
            if erase:
                self.__erase_pixels(pixels)

        if self.__is_display_update_allow:
            pygame.display.update()
            self.__is_display_update_allow = False

    def reset(self):
        """Clean cashe and reset screen state to begining state"""
        width = self.__grid_width
        height = self.__grid_height
        self.__cashe = \
            [[None for _ in range(height)] for _ in range(width)]
        self.__view.fill(self.__background_color)
        pygame.display.update()

    def __draw_pixel(self, pixel: Pixel):
        if self.__add_pixel_to_cashe(pixel):
            self.__set_pixel_on_view(pixel)

    def __draw_pixels(self, pixels: List[Pixel]):
        for pixel in pixels:
            self.__draw_pixel(pixel)

    def __erase_pixel(self, pixel: Pixel):
        if self.__remove_pixel_from_cashe(pixel):
            self.__set_pixel_on_view(pixel, remove=True)

    def __erase_pixels(self, pixels: List[Pixel]):
        for pixel in pixels:
            self.__erase_pixel(pixel)

    def __add_pixel_to_cashe(self, pixel: Pixel) -> bool:
        column, row = pixel.position
        if self.__cashe[column][row] is not None:
            if self.__cashe[column][row] == pixel.color:
                return False
        self.__cashe[column][row] = pixel.color
        self.__is_display_update_allow = True
        return True

    def __remove_pixel_from_cashe(self, pixel: Pixel) -> bool:
        column, row = pixel.position
        if self.__cashe[column][row] is None:
            return False
        self.__cashe[column][row] = None
        self.__is_display_update_allow = True
        return True

    def __set_pixel_on_view(self, pixel: Pixel, remove: bool = False):
        pixel_color = pixel.color if not remove else self.__background_color
        column, row = pixel.position

        rect = pygame.Rect(
            column * self.__grid_size,
            row * self.__grid_size,
            self.__grid_size,
            self.__grid_size
        )
        pygame.draw.rect(self.__view, pixel_color, rect)
        pygame.draw.rect(self.__view, self.__background_color, rect, 1)

    def __check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.__on_game_quit_callback()
                return
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_UP:
                self.__on_direction_change_callback(UP)
            if event.key == pygame.K_DOWN:
                self.__on_direction_change_callback(DOWN)
            if event.key == pygame.K_LEFT:
                self.__on_direction_change_callback(LEFT)
            if event.key == pygame.K_RIGHT:
                self.__on_direction_change_callback(RIGHT)
