from typing import Iterator
from itertools import chain

import cProfile
import pprint as pp


DEFAULT_BITMASK_VALUE = 0b111111111  # 9 ones


class InvalidPuzzleError(Exception):
    pass


class SudokuSolver:
    def __init__(self, puzzle: list[list[int]]):
        # It should raise an error in cases of:
        # invalid grid (not 9x9, cell with values not in the range 1~9);
        # multiple solutions for the same puzzle or the puzzle is unsolvable
        if len(puzzle) != 9 or any(len(row) != 9 for row in puzzle):
            raise InvalidPuzzleError("Invalid puzzle shape")
        self.puzzle = list(chain(*puzzle))

        self.row_masks = [DEFAULT_BITMASK_VALUE for i in range(9)]
        self.col_masks = [*self.row_masks]
        self.box_masks = [*self.row_masks]

        self.todo = []  # indices of cells that we need to fill

        for row_index in range(9):
            for col_index in range(9):
                value = self.puzzle[row_index * 9 + col_index]
                box_index = (row_index // 3) * 3 + col_index // 3
                if value == 0:
                    self.todo.append((row_index, col_index, box_index))
                elif 1 <= value <= 9:
                    # If the corresponding bit is alreay zero, it means the <value> has already been
                    # encountered for this row, col or box
                    if (
                        not (self.row_masks[row_index] & 1 << value - 1)
                        or not (self.col_masks[col_index] & 1 << value - 1)
                        or not (self.box_masks[box_index] & 1 << value - 1)
                    ):
                        raise InvalidPuzzleError("Invalid grid")

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
                else:
                    raise InvalidPuzzleError(
                        "Cell value out of range 1~9 and 0 for empty cells"
                    )
        # Sorting todo list of cells by number of possible values
        self.todo = sorted(
            self.todo,
            key=self.get_number_of_possible_values,
        )

        self.todo_len = len(self.todo)

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

    def get_number_of_possible_values(self, coordinates: tuple[int, int, int]) -> int:
        row_mask, col_mask, box_mask = (
            self.row_masks[coordinates[0]],
            self.col_masks[coordinates[1]],
            self.box_masks[coordinates[2]],
        )
        # row_mask: int, col_mask: int, box_mask: int
        return (row_mask & col_mask & box_mask).bit_count()

    def _solve(
        self,
        todo_index: int,
    ) -> list[list[int]]:
        solutions = []

        # Sorting todos to get next promising value to top
        self.todo[todo_index:] = sorted(
            self.todo[todo_index:],
            key=self.get_number_of_possible_values,
        )

        row_index, col_index, box_index = self.todo[todo_index]
        for new_value in self.get_possible_cell_values(row_index, col_index):
            # We set the new value to [row_index, col_index] and reset it back after testing
            self.puzzle[row_index * 9 + col_index] = new_value
            # Updating masks with the new value
            self.row_masks[row_index] ^= 1 << new_value - 1
            self.col_masks[col_index] ^= 1 << new_value - 1
            self.box_masks[box_index] ^= 1 << new_value - 1

            if todo_index == self.todo_len - 1:
                # The sudoku is solved
                solutions.append([*self.puzzle])
            elif new_solutions := self._solve(
                todo_index + 1,
            ):
                solutions.extend(new_solutions)
            if len(solutions) > 1:
                raise InvalidPuzzleError("Puzzle has more than 1 solution")
            # Reseting masks
            self.row_masks[row_index] |= 1 << new_value - 1
            self.col_masks[col_index] |= 1 << new_value - 1
            self.box_masks[box_index] |= 1 << new_value - 1

            self.puzzle[row_index * 9 + col_index] = 0
        return solutions

    def solve(self):
        solutions = self._solve(0)
        if not solutions:
            raise InvalidPuzzleError("Unsolvable puzzle")
        return [solutions[0][offset : offset + 9] for offset in range(0, 81, 9)]


def sudoku_solver(puzzle: list[list[int]]) -> list[list[int]]:
    solver = SudokuSolver(puzzle)
    return solver.solve()


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
