import pygame
from typing import List, Optional
from modules.class_module.Pixel import Pixel
from modules.class_module.Apple import Apple
from modules.class_module.Snake import Snake
from modules.class_module.GameObject import GameObject
from modules.game_settings import (SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE,
                                   GRID_WIDTH, GRID_HEIGHT, UP, DOWN, LEFT,
                                   RIGHT, BOARD_BACKGROUND_COLOR, SPEED,
                                   APPLE_COLOR, SNAKE_COLOR, GAME_TITLE)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)
pygame.display.set_caption(GAME_TITLE)
pygame.init()
pygame.display.update()

clock = pygame.time.Clock()


def main():
    """Main func"""
    snake = Snake(
        body_color=SNAKE_COLOR,
        direction=RIGHT,
        on_draw=draw_snake
    )

    apple = Apple(
        body_color=APPLE_COLOR,
        on_draw=draw_apple
    )

    apple.randomize_position(
        exceptions=snake.positions
    )

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if __snake_eat_apple(snake, apple):
            snake.grow_up()
            apple.randomize_position(
                exceptions=snake.positions
            )

        elif __snake_bites_own_body(snake):
            __game_over(snake, apple)

        apple.draw()
        snake.draw()
        pygame.display.update()


def handle_keys(snake: Snake):
    """Handle user keys pressed"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT \
           or event.type == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit
        if event.type != pygame.KEYDOWN:
            continue
        if event.key == pygame.K_UP:
            snake.update_direction(UP)
        if event.key == pygame.K_DOWN:
            snake.update_direction(DOWN)
        if event.key == pygame.K_LEFT:
            snake.update_direction(LEFT)
        if event.key == pygame.K_RIGHT:
            snake.update_direction(RIGHT)


def draw_apple(apple: Apple):
    """Draw apple on pygame lib surface"""
    __draw_pixel(apple.position)


def draw_snake(snake: Snake):
    """Draw snake on pygame lib surface"""
    __draw_pixels(snake.positions)
    __draw_pixel(pixel=snake.disappeared_tail, remove=True)


def __game_over(snake: Snake, apple: Apple):
    screen.fill(BOARD_BACKGROUND_COLOR)
    pygame.display.update()
    snake.reset()
    apple.randomize_position(
        exceptions=snake.positions
    )


def __snake_eat_apple(snake: Snake, apple: Apple) -> bool:
    if apple.position is None:
        return False
    return snake.get_head_position() == apple.position


def __snake_bites_own_body(snake: Snake) -> bool:
    if len(snake.positions) < 5:
        return False
    return snake.get_head_position() in snake.positions[5:]


def __draw_pixel(pixel: Optional[Pixel], remove: bool = False):
    if pixel is None:
        return
    pixel_color = pixel.color if not remove else BOARD_BACKGROUND_COLOR
    column, row = pixel.location

    rect = pygame.Rect(
        column * GRID_SIZE,
        row * GRID_SIZE,
        GRID_SIZE,
        GRID_SIZE
    )
    pygame.draw.rect(screen, pixel_color, rect)
    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect, 1)


def __draw_pixels(pixels: List[Pixel]):
    for pixel in pixels:
        __draw_pixel(pixel)


if __name__ == '__main__':
    # для прохождения теста
    # и соответствия PEP 8 (исключить неиспользованные импорты)
    GameObject, GRID_WIDTH, GRID_HEIGHT

    main()
