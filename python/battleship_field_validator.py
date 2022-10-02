from collections import defaultdict

VERTICAL = 'v'
HORIZONTAL = 'h'
UNKNOWN = 'u'


def validate_battlefield(field: list[list[int]]) -> bool:
    ships_count = defaultdict(int)
    visited = set()

    def _ship_size(x: int, y: int, orient: str, size=1) -> int:
        # Returns ship size or -1 if the ship shape is invalid
        visited.add((x, y))
        horizontal = x + 1 < 10 and field[y][x + 1]
        vertical = y + 1 < 10 and field[y + 1][x]
        diagonal_up = x + 1 < 10 and y - 1 >= 0 and field[y - 1][x + 1]
        diagonal_down = x + 1 < 10 and y + 1 < 10 and field[y + 1][x + 1]
        if any((diagonal_up, diagonal_down, horizontal and vertical)):
            return -1
        elif horizontal:
            if orient == VERTICAL:
                return -1
            return _ship_size(x + 1, y, HORIZONTAL, size=size + 1)
        elif vertical:
            if orient == HORIZONTAL:
                return -1
            return _ship_size(x, y + 1, VERTICAL, size=size + 1)
        return size

    for y in range(10):
        for x in range(10):
            if (x, y) in visited:
                continue
            if field[y][x]:
                size = _ship_size(x, y, UNKNOWN)
                ships_count[size] += 1
    return ships_count == dict(zip(range(1, 5), range(4, 0, -1)))


def print_field(field, visited, x_, y_):
    for y in range(10):
        for x in range(10):
            if x == x_ and y == y_:
                print('# ', end='')
            # elif (x, y) in visited:
            elif field[y][x]:
                print('x ', end='')
            else:
                print('. ', end='')
        print('\n', end='')


if __name__ == '__main__':

    battleField = [
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert validate_battlefield(battleField), 'OK case'

    battleField = [
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert not validate_battlefield(battleField), 'Wrong size'

    battleField = [
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert not validate_battlefield(battleField), 'Invalid shape (extra horizontal deck)'

    battleField = [
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert not validate_battlefield(battleField), 'Invalid shape (diagonal down)'

    battleField = [
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert not validate_battlefield(battleField), 'Invalid shape (diagonal up)'
