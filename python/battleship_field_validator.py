from collections import defaultdict

CORRECT_SHIPS_COUNT = {
    1: 4,
    2: 3,
    3: 2,
    4: 1,
}

VERTICAL = 'v'
HORIZONTAL = 'h'
UNKNOWN = 'u'


def validate_battlefield(field: list[list[int]]) -> bool:
    ships_count = defaultdict(int)
    visited = set()

    # def _process_ship(x: int, y: int, orient: str, size=1) -> int:
    #     visited.add((x, y))
    #     horizontal = x + 1 < 10 and field[y][x + 1]
    #     vertical = y + 1 < 10 and field[y + 1][x]
    #     diagonal = x + 1 < 10 and y + 1 < 10 and field[y + 1][x + 1]
    #     if diagonal:
    #         return -1
    #     if horizontal and vertical:
    #         return -1
    #     elif horizontal:
    #         if orient == VERTICAL:
    #             return -1
    #         return _process_ship(x + 1, y, HORIZONTAL, size=size + 1)
    #     elif vertical:
    #         if orient == HORIZONTAL:
    #             return False
    #         return _process_ship(x, y + 1, VERTICAL, size=size + 1)
    #     return size

    for y in range(10):
        for x in range(10):
            # print(f'Iteration {x=} {y=} {ships_count=}')
            # print_field( visited, x, y)
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if field[y][x]:
                size = 1
                orient = UNKNOWN
                x_, y_ = x, y
                while True:
                    # print(f'Sub_Iteration {x_=} {y_=} {ships_count=}')
                    # print_field(field, visited, x_, y_)
                    horizontal = x_ + 1 < 10 and field[y_][x_ + 1]
                    vertical = y_ + 1 < 10 and field[y_ + 1][x_]
                    diagonal = x_ + 1 < 10 and y_ + 1 < 10 and field[y_ + 1][x_ + 1]
                    if diagonal:
                        return False
                    if horizontal and vertical:
                        return False
                    elif horizontal:
                        if orient == VERTICAL:
                            return False
                        orient = HORIZONTAL
                        size += 1
                        x_ += 1
                        visited.add((x_, y_))
                    elif vertical:
                        if orient == HORIZONTAL:
                            return False
                        orient = VERTICAL
                        size += 1
                        y_ += 1
                        visited.add((x_, y_))
                    else:
                        # print(f'Adding ship {x_=} {y_=} {size=} {ships_count=}')
                        ships_count[size] += 1
                        orient = UNKNOWN
                        break
    # print(f'Returning, {ships_count=}')
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
    assert validate_battlefield(battleField)

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
    assert not validate_battlefield(battleField)

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
    assert not validate_battlefield(battleField)

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
    assert not validate_battlefield(battleField)
