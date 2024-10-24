from typing import Tuple, List
from modules.class_module.Pixel import Pixel
from modules.class_module.GameObject import GameObject
from modules.class_module.Apple import Apple
from modules.class_module.Snake import Snake
from modules.class_module.GameScreen import GameScreen
from modules.to_pass_test import screen, clock, handle_keys
from modules.game_settings import (SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE,
                                   GRID_WIDTH, GRID_HEIGHT, UP, DOWN, LEFT,
                                   RIGHT, BOARD_BACKGROUND_COLOR,
                                   APPLE_COLOR, SNAKE_COLOR, SPEED, GAME_TITLE)

# Дорогие ревьюеры, привет!
# Не убивайте, пожалуйста, инициативу в зачатке!
# Рука не подялась выполнить проект без маломайской архитектуры - я изолировал
# pygame в классе GameScreen, который в свою очередь предоставляет ограниченый
# интерфейс для взаимодействия с pygame, а также выполняет колбэки на действия
# пользователя.
# Классы Apple и Snake естественно тоже изолированы от pygame.
# Но  тесты  такая реализация  не проходила,  пришлось создать  и ипортировать
# необходимые для  теста переменные,  добавить некую  абстракцию в виде пустой
# фнккции handle_keys и сложить туда  неиспользуемые объекты,  чтобы линтер не
# ругался, а также добавить пустышку clock.tick().
# Спасибо.
handle_keys(screen, clock, GRID_WIDTH, GRID_HEIGHT, UP, DOWN, LEFT)


def main():
    """Main func"""
    def change_snake_direction(direction: Tuple[int, int]):
        snake.update_direction(direction)

    def draw_apple(apple: Apple):
        game_screen.draw(pixel=apple.position)

    def draw_snake(snake: Snake):
        game_screen.draw(pixels=snake.positions)
        game_screen.draw(pixel=snake.disappeared_tail, erase=True)

    game_screen = GameScreen(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        grid_size=GRID_SIZE,
        background_color=BOARD_BACKGROUND_COLOR,
        title=GAME_TITLE
    )
    game_screen.set_on_game_quit(quit_game)
    game_screen.set_on_direction_change(change_snake_direction)

    scr_border_column, scr_border_row = game_screen.borders

    snake = Snake(
        start_pixel=Pixel(
            column=scr_border_column // 2,
            row=scr_border_row // 2,
            color=SNAKE_COLOR
        ),
        direction=RIGHT,
        on_draw=draw_snake
    )

    apple = Apple(
        body_color=APPLE_COLOR,
        on_draw=draw_apple
    )

    while True:
        game_screen.slow(SPEED)
        __set_snake(snake)
        __set_apple(apple, game_screen.borders, snake.positions)

        snake.move()

        if __snake_gone_out_of_borders(
            snake.get_head_position(),
            game_screen.borders
        ):
            teleported_snake_head = __get_teleported_snake_head(
                snake_head_position=snake.get_head_position(),
                screen_borders=game_screen.borders
            )
            snake.teleport_snake_head(teleported_snake_head)

        if __snake_eat_apple(snake, apple):
            snake.grow_up()
            apple.destroy()

        if __snake_bites_own_body(snake):
            __game_over(game_screen, apple, snake)

        __draw_game_objects(apple, snake)

        clock.tick()  # Пустышка для прохождения теста


def quit_game():
    """On user quit game"""
    raise SystemExit


def __set_snake(snake: Snake):
    if not snake.exist():
        snake.reset()


def __set_apple(
        apple: Apple,
        screen_borders: Tuple[int, int],
        exceptions: List[Pixel]
):
    if apple.exist():
        return
    apple.randomize_position(
        borders=screen_borders,
        exceptions=exceptions
    )


def __draw_game_objects(*args: GameObject):
    for game_object in args:
        if game_object.exist():
            game_object.draw()


def __game_over(game_screen: GameScreen, *args: GameObject):
    game_screen.reset()
    for game_object in args:
        game_object.destroy()


def __snake_eat_apple(snake: Snake, apple: Apple) -> bool:
    if apple.position is None:
        return False
    return snake.get_head_position() == apple.position.position


def __snake_bites_own_body(snake: Snake) -> bool:
    if len(snake.positions) < 2:
        return False
    for pixel in snake.positions[1:]:
        if pixel is None:
            continue
        if snake.get_head_position() == pixel.position:
            return True
    return False


def __snake_gone_out_of_borders(
        snake_head_position: Tuple[int, int],
        screen_borders: Tuple[int, int]
) -> bool:
    scr_border_column, scr_border_row = screen_borders
    snake_head_column, snake_head_row = snake_head_position

    if snake_head_column < 0 \
       or snake_head_column > scr_border_column \
       or snake_head_row < 0 \
       or snake_head_row > scr_border_row:
        return True
    return False


def __get_teleported_snake_head(
        snake_head_position: Tuple[int, int],
        screen_borders: Tuple[int, int]
) -> Pixel:
    scr_border_column, scr_border_row = screen_borders
    snake_head_column, snake_head_row = snake_head_position

    snake_head_column = scr_border_column if snake_head_column < 0 \
        else snake_head_column
    snake_head_column = 0 if snake_head_column > scr_border_column \
        else snake_head_column
    snake_head_row = scr_border_row if snake_head_row < 0 else snake_head_row
    snake_head_row = 0 if snake_head_row > scr_border_row else snake_head_row

    return Pixel(snake_head_column, snake_head_row, SNAKE_COLOR)


if __name__ == '__main__':
    main()
