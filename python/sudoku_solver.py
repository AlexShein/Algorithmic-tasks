from typing import Iterator
import pprint as pp
from itertools import chain

ALLOWED_VALUES_SET = set(range(1, 10))
SOLVED_SUDOKU_SUM = 405


class InvalidPuzzleError(Exception):
    pass


def is_solved(puzzle: list[int]) -> bool:
    return sum(puzzle) == SOLVED_SUDOKU_SUM


def get_box(puzzle: list[list[int]], row_index: int, col_index: int) -> set[int]:
    row_min = (row_index // 3) * 3
    col_min = (col_index // 3) * 3

    return (
        *puzzle[row_min * 9 + col_min : row_min * 9 + col_min + 3],
        *puzzle[(row_min + 1) * 9 + col_min : (row_min + 1) * 9 + col_min + 3],
        *puzzle[(row_min + 2) * 9 + col_min : (row_min + 2) * 9 + col_min + 3],
    )


def get_possible_cell_values(
    puzzle: list[list[int]], row_index: int, col_index: int
) -> Iterator[int]:
    for value in ALLOWED_VALUES_SET - {
        *puzzle[row_index * 9 : (row_index + 1) * 9],
        *(puzzle[_row_index * 9 + col_index] for _row_index in range(9)),
        *get_box(puzzle, row_index, col_index),
    }:
        yield value


def solve(puzzle: list[int], start_row: int) -> list[list[int]]:
    solutions = []
    for row_index in range(start_row, 9):
        for col_index in range(9):
            if puzzle[row_index * 9 + col_index] == 0:
                # TODO (Alexander Shein) Find the most constrained cell
                for new_value in get_possible_cell_values(puzzle, row_index, col_index):
                    # We copy the puzzle and set the new value to [row_index, col_index]
                    _puzzle = list(
                        value if index != row_index * 9 + col_index else new_value
                        for index, value in enumerate(puzzle)
                    )
                    if is_solved(_puzzle):
                        solutions.append(_puzzle)
                    else:
                        solutions.extend(solve(_puzzle, row_index))
                    if len(solutions) > 1:
                        raise InvalidPuzzleError("Puzzle has more than 1 solution")
                return solutions


def sudoku_solver(puzzle: list[list[int]]) -> list[list[int]]:
    # It should raise an error in cases of:
    # invalid grid (not 9x9, cell with values not in the range 1~9);
    # multiple solutions for the same puzzle or the puzzle is unsolvable
    if len(puzzle) != 9 or any(len(row) != 9 for row in puzzle):
        raise InvalidPuzzleError("Invalid puzzle shape")
    _puzzle = list(chain(*puzzle))
    for item in _puzzle:
        if not 0 <= item <= 9:
            raise InvalidPuzzleError(
                "Cell value out of range 1~9 and 0 for empty cells"
            )

    solutions = solve(_puzzle, 0)
    if not solutions:
        raise InvalidPuzzleError("Unsolvable puzzle")
    return [solutions[0][offset : offset + 9] for offset in range(0, 81, 9)]


if __name__ == "__main__":
    puzzle = [
        [0, 0, 6, 1, 0, 0, 0, 0, 8],
        [0, 8, 0, 0, 9, 0, 0, 3, 0],
        [2, 0, 0, 0, 0, 5, 4, 0, 0],
        [4, 0, 0, 0, 0, 1, 8, 0, 0],
        [0, 3, 0, 0, 7, 0, 0, 4, 0],
        [0, 0, 7, 9, 0, 0, 0, 0, 3],
        [0, 0, 8, 4, 0, 0, 0, 0, 6],
        [0, 2, 0, 0, 5, 0, 0, 8, 0],
        [1, 0, 0, 0, 0, 2, 5, 0, 0],
    ]

    solution = [
        [3, 4, 6, 1, 2, 7, 9, 5, 8],
        [7, 8, 5, 6, 9, 4, 1, 3, 2],
        [2, 1, 9, 3, 8, 5, 4, 6, 7],
        [4, 6, 2, 5, 3, 1, 8, 7, 9],
        [9, 3, 1, 2, 7, 8, 6, 4, 5],
        [8, 5, 7, 9, 4, 6, 2, 1, 3],
        [5, 9, 8, 4, 1, 3, 7, 2, 6],
        [6, 2, 4, 7, 5, 9, 3, 8, 1],
        [1, 7, 3, 8, 6, 2, 5, 9, 4],
    ]

    solver_output = sudoku_solver(puzzle)
    print("** Solution found! **")
    pp.pprint(solver_output)
    assert solver_output == solution, "Failed to solve sample sudoku"
