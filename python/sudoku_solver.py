from typing import Iterator
from itertools import chain

import cProfile
import pprint as pp


DEFAULT_BITMASK_VALUE = 0b111111111  # 9 ones


class InvalidPuzzleError(Exception):
    pass


class SudokuSolver:
    def __init__(self, puzzle: list[int]):
        self.puzzle = puzzle

        self.row_masks = [DEFAULT_BITMASK_VALUE for i in range(9)]
        self.col_masks = [*self.row_masks]
        self.box_masks = [*self.row_masks]

        self.todo = []  # indices of cells that we need to fill

        for row_index in range(9):
            for col_index in range(9):
                value = puzzle[row_index * 9 + col_index]
                box_index = (row_index // 3) * 3 + col_index // 3
                if value == 0:
                    self.todo.append((row_index, col_index, box_index))
                else:
                    # We are setting bit number <value> to zero meaning we can't use that number anymore
                    self.row_masks[row_index] = self.row_masks[row_index] ^ (
                        1 << value - 1
                    )
                    self.col_masks[col_index] = self.col_masks[col_index] ^ (
                        1 << value - 1
                    )
                    self.box_masks[box_index] = self.box_masks[box_index] ^ (
                        1 << value - 1
                    )

    def get_possible_cell_values(self, row_index: int, col_index: int) -> Iterator[int]:
        box_index = (row_index // 3) * 3 + col_index // 3
        allowed_row_values_mask = (
            self.row_masks[row_index]
            & self.col_masks[col_index]
            & self.box_masks[box_index]
        )
        for value in range(9):
            if allowed_row_values_mask & 1 << value:
                yield value + 1

    def solve(self, todo_index: int, zeros_count: int) -> list[list[int]]:
        solutions = []

        row_index, col_index, box_index = self.todo[todo_index]
        for new_value in self.get_possible_cell_values(row_index, col_index):
            # We set the new value to [row_index, col_index] and reset it back after testing
            self.puzzle[row_index * 9 + col_index] = new_value
            # Updating masks with the new value
            self.row_masks[row_index] ^= 1 << new_value - 1
            self.col_masks[col_index] ^= 1 << new_value - 1
            self.box_masks[box_index] ^= 1 << new_value - 1

            if zeros_count == 1:
                # The sudoku is solved
                solutions.append([*self.puzzle])
            elif new_solutions := self.solve(todo_index + 1, zeros_count - 1):
                solutions.extend(new_solutions)
            if len(solutions) > 1:
                raise InvalidPuzzleError("Puzzle has more than 1 solution")
            # Reseting masks
            self.row_masks[row_index] |= 1 << new_value - 1
            self.col_masks[col_index] |= 1 << new_value - 1
            self.box_masks[box_index] |= 1 << new_value - 1

            self.puzzle[row_index * 9 + col_index] = 0
        return solutions

    # def alternative_solve(self, start_row: int, zeros_count: int) -> list[list[int]]:
    #     solutions = []
    #     for row_index in range(start_row, 9):
    #         for col_index in range(9):
    #             box_index = (row_index // 3) * 3 + col_index // 3
    #             # TODO (Alexander Shein) Use cell coordinates from queue
    #             if self.puzzle[row_index * 9 + col_index] == 0:
    #                 for new_value in self.get_possible_cell_values(
    #                     row_index, col_index
    #                 ):
    #                     # We set the new value to [row_index, col_index] and reset it back after testing
    #                     self.puzzle[row_index * 9 + col_index] = new_value
    #                     # Updating masks with the new value
    #                     self.row_masks[row_index] ^= 1 << new_value - 1
    #                     self.col_masks[col_index] ^= 1 << new_value - 1
    #                     self.box_masks[box_index] ^= 1 << new_value - 1

    #                     if zeros_count == 1:
    #                         # The sudoku is solved
    #                         solutions.append([*self.puzzle])
    #                     elif new_solutions := self.solve(row_index, zeros_count - 1):
    #                         solutions.extend(new_solutions)
    #                     if len(solutions) > 1:
    #                         raise InvalidPuzzleError("Puzzle has more than 1 solution")
    #                     # Reseting masks
    #                     self.row_masks[row_index] |= 1 << new_value - 1
    #                     self.col_masks[col_index] |= 1 << new_value - 1
    #                     self.box_masks[box_index] |= 1 << new_value - 1

    #                     self.puzzle[row_index * 9 + col_index] = 0
    #                 return solutions


def sudoku_solver(puzzle: list[list[int]]) -> list[list[int]]:
    # It should raise an error in cases of:
    # invalid grid (not 9x9, cell with values not in the range 1~9);
    # multiple solutions for the same puzzle or the puzzle is unsolvable
    if len(puzzle) != 9 or any(len(row) != 9 for row in puzzle):
        raise InvalidPuzzleError("Invalid puzzle shape")
    _puzzle = list(chain(*puzzle))
    zeros_count = 0
    for item in _puzzle:
        if item == 0:
            zeros_count += 1
        if not 0 <= item <= 9:
            raise InvalidPuzzleError(
                "Cell value out of range 1~9 and 0 for empty cells"
            )

    solver = SudokuSolver(_puzzle)
    solutions = solver.solve(0, zeros_count)
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

    cProfile.run("sudoku_solver(puzzle)")

    print("** Solution found! **")
    pp.pprint(solver_output)
    assert solver_output == solution, "Failed to solve sample sudoku"
