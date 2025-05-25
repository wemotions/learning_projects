import copy
import random


def display_field(field: list[list[int]]):
    """Отображает игровое поле с заменой 0 на пробел."""
    for row in field:
        print(' '.join(f' ' if item == 0 else f'{item:2}' for item in row))
    print()


def get_position(field: list[list[int]]) -> tuple[int, int]:
    """Возвращает координаты пустой клетки (0)."""
    for i, row in enumerate(field):
        for j, item in enumerate(row):
            if item == 0:
                return i, j


def is_valid_move(x: int, y: int, direction: str) -> bool:
    """Проверяет, возможно ли движение в заданном направлении."""
    if direction == 'w' and x == 0:
        return False
    if direction == 's' and x == 3:
        return False
    if direction == 'a' and y == 0:
        return False
    if direction == 'd' and y == 3:
        return False
    return True


def move_field(x: int, y: int, field: list[list[int]], direction: str) -> None:
    """Перемещает пустую клетку в указанном направлении."""
    if not is_valid_move(x, y, direction):
        raise ValueError('Ошибка: Нельзя двигаться в этом направлении.')

    new_x, new_y = x, y
    if direction == 'w':
        new_x -= 1
    elif direction == 's':
        new_x += 1
    elif direction == 'a':
        new_y -= 1
    elif direction == 'd':
        new_y += 1

    field[x][y], field[new_x][new_y] = field[new_x][new_y], field[x][y]


def mix_field(field: list[list[int]]) -> None:
    """Генерирует разрешимое поле, начиная с упорядоченного состояния."""
    directions = ['w', 's', 'a', 'd']
    for _ in range(100):
        x, y = get_position(field)
        valid_dirs = [d for d in directions if is_valid_move(x, y, d)]
        if valid_dirs:
            move_field(x, y, field, random.choice(valid_dirs))


def check_win(field: list[list[int]]) -> bool:
    """Проверяет, упорядочено ли поле (1-15 с 0 в правом нижнем углу)."""
    flat_field = [item for row in field for item in row]
    return flat_field == list(range(1, 16)) + [0]


def play_game() -> None:
    """Запускает игровой процесс."""
    count = 0
    data = list(range(1, 16)) + [0]
    field = [data[i:i + 4] for i in range(0, len(data), 4)]
    game_field = copy.deepcopy(field)
    mix_field(game_field)

    while True:
        display_field(game_field)
        move = input('Введите направление (w - вверх, s - вниз, a - влево, d - вправо, q - выход): ')

        if move == 'q':
            break
        elif move not in ['w', 'a', 's', 'd']:
            print('Ошибка: Введите корректное направление (w, s, a, d или q для выхода).')
            continue

        try:
            x, y = get_position(game_field)
            move_field(x, y, game_field, move)
            count += 1
            if check_win(game_field):
                display_field(game_field)
                print(f'Поздравляем! Вы победили за {count} ходов!')
                break
            print(f'Количество ходов {count}.')
        except ValueError as e:
            print(e)


def main() -> None:
    """Запускает игру с возможностью повторения."""
    print('Добро пожаловать в игру Пятнашки!')
    while True:
        play_game()
        again = input('Хотите сыграть еще? (да/нет) ').lower()
        if again not in ['да', 'д', 'y', 'yes']:
            print('До свидания!')
            break


if __name__ == '__main__':
    main()
