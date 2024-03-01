from typing import Iterator
from itertools import chain
from collections import namedtuple

# Imports needed for debug purposes
import cProfile
import pprint as pp


DEFAULT_BITMASK_VALUE = 0b111111111  # 9 ones
RowColBoxIndices = namedtuple(
    "RowColBoxIndices", ["row_index", "col_index", "box_index"]
)


class InvalidPuzzleError(Exception):
    """
    Custom exception is not really required, but looks way nicer in the code than e.g. generic ValueError.
    """

    pass


class SudokuSolver:
    """
    SudokuSolver uses slightly optimized backtracking approach to solve sudoku puzzles.
    It starts with transforming 2d puzzle array into 1d representation.
    After that we create bit masks for each row, column and box representing
    Which numbers are still available. We use first 9 bits to represent number 1-9.
    E.g. if [1, 2, 4] are possible values for the cell, it means that
    row_mask & col_mask & box_mask == 0b000001011

    At each step the grid is modified and the solver function is called recursively.
    """

    def __init__(self, puzzle: list[list[int]]):
        """
        Initializes the solver by:
        - Converting puzzle to 1d list representation
        - Initializing bit masks with ones
        - Switching corresponding bits of masks to 0 if number is already used
        - Creating the "todo" empty cell indicies
        - Ordering "todo" by number of possible value (least first)

        It should raise an error in cases of:
        invalid grid (not 9x9, cell with values not in the range 1~9);
        multiple solutions for the same puzzle or the puzzle is unsolvable.
        """
        if len(puzzle) != 9 or any(len(row) != 9 for row in puzzle):
            raise InvalidPuzzleError("Invalid puzzle shape")
        self.puzzle = list(chain(*puzzle))

        # Possible values bit masks for each row, column and box
        self.row_masks = [DEFAULT_BITMASK_VALUE for i in range(9)]
        self.col_masks = [*self.row_masks]
        self.box_masks = [*self.row_masks]

        self.todo: list[
            RowColBoxIndices
        ] = []  # row, col and box indices of cells that we need to fill

        for row_index in range(9):
            for col_index in range(9):
                value = self.puzzle[row_index * 9 + col_index]
                box_index = (row_index // 3) * 3 + col_index // 3
                if value == 0:
                    self.todo.append(RowColBoxIndices(row_index, col_index, box_index))
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

    def get_possible_cell_values(
        self, row_index: int, col_index: int, box_index: int
    ) -> Iterator[int]:
        """
        Return cell candidate values based on corresponding cell, column and row bitmasks.
        """
        allowed_row_values_mask = (
            self.row_masks[row_index]
            & self.col_masks[col_index]
            & self.box_masks[box_index]
        )
        for value in range(9):
            if allowed_row_values_mask & 1 << value:
                yield value + 1

    def get_number_of_possible_values(self, coordinates: RowColBoxIndices) -> int:
        """
        Returns count of possible candidate values for a cell.
        Doing bitwise AND between corresponding row, column and box masks
        And counting non-zero bits in the result.
        """
        row_mask, col_mask, box_mask = (
            self.row_masks[coordinates.row_index],
            self.col_masks[coordinates.col_index],
            self.box_masks[coordinates.box_index],
        )
        return (row_mask & col_mask & box_mask).bit_count()

    def _solve(
        self,
        todo_index: int,
    ) -> list[list[int]]:
        """
        Main solver method. It is called recursively every time we make a gues for a cell.
        Throws an exception if encounters more than 1 solution.

        We find the next cell with least candidate values by sorting todos list.
        After that we iterate over potential values, set each one to the grid, update bit masks for
        row, column and box and call the solve method recursively if there are still cells left in the todo list.

        After the recursive call, we cleanup the cell we made a guess for and restore bit masks.
        """
        solutions = []

        # Sorting todos to get next promising value to top
        self.todo[todo_index:] = sorted(
            self.todo[todo_index:],
            key=self.get_number_of_possible_values,
        )

        row_index, col_index, box_index = self.todo[todo_index]
        for new_value in self.get_possible_cell_values(row_index, col_index, box_index):
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
        """
        Public wrapper for solve method.
        Takes care of formatting the puzzle as a 2d list.
        """
        solutions = self._solve(0)
        if not solutions:
            raise InvalidPuzzleError("Unsolvable puzzle")
        return [solutions[0][offset : offset + 9] for offset in range(0, 81, 9)]


def sudoku_solver(puzzle: list[list[int]]) -> list[list[int]]:
    """
    This function is only required by the task.
    """
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
