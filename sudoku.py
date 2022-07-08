'''
This module provides SudokuSolver, a class that solves
any sudoku puzzle.
One example puzzle is also provided, which is solved
using when running this file.
Examples:
    Unfortunately, this package is not yet on PyPi, so to
    use this code, you will need to Fork or Clone.

    You can run this file using the code below
    ```bash
    $ python sudoku.py
    ```
    This will print to the console a starting puzzle, along
    with its solution.
    You can also use the solver for your own cases by following
    along with the example in the main block.  You will want to
    import the solver:
    ```python
    from sudoku import SudokuSolver
    ```

    And you will need to replicate your sudoku puzzle:
    ```python
    def create_sudoku():
        container = []
        container.append([0, 0, 0, 0, 0, 8, 3, 0, 0])
        container.append([0, 0, 0, 0, 2, 4, 0, 9, 0])
        container.append([0, 0, 4, 0, 7, 0, 0, 0, 6])
        container.append([0, 0, 0, 0, 0, 3, 0, 7, 9])
        container.append([7, 5, 0, 0, 0, 0, 0, 8, 4])
        container.append([9, 2, 0, 5, 0, 0, 0, 0, 0])
        container.append([4, 0, 0, 0, 9, 0, 1, 0, 0])
        container.append([0, 3, 0, 4, 6, 0, 0, 0, 0])
        container.append([0, 0, 5, 8, 0, 0, 0, 0, 0])
        return container
    ```
    And then you simply create the puzzle, instantiate, and use
    the solve() method:
    ```python
    PUZZLE = create_sudoku()
    SUDOKU = SudokuSolver(PUZZLE)
    SUDOKU.print_container()
    SUDOKU.solve()
    SUDOKU.print_container()
    ```
'''
from copy import deepcopy

class SudokuSolver():
    '''
    Description
    ------------------------------------------------------
    input:
        original_container (list): Always provides original `container`
        container (list): Should be in the below format -
                    container = []
                    container.append([0, 0, 0, 0, 0, 8, 3, 0, 0])
                    container.append([0, 0, 0, 0, 2, 4, 0, 9, 0])
                    container.append([0, 0, 4, 0, 7, 0, 0, 0, 6])
                    container.append([0, 0, 0, 0, 0, 3, 0, 7, 9])
                    container.append([7, 5, 0, 0, 0, 0, 0, 8, 4])
                    container.append([9, 2, 0, 5, 0, 0, 0, 0, 0])
                    container.append([4, 0, 0, 0, 9, 0, 1, 0, 0])
                    container.append([0, 3, 0, 4, 6, 0, 0, 0, 0])
                    container.append([0, 0, 5, 8, 0, 0, 0, 0, 0])

    - Zeros are unknown values
    - All values must be between 1 and 9 when known
    - Solves standard sudoku puzzle
    - Learn more here: https://youtu.be/8zRXDsGydeQ

    Recommended User Interface
    ------------------------------------------------------
        SUDOKU = SudokuSolver(container)
        SUDOKU.print_container()
        SUDOKU.solve()
        SUDOKU.print_container()
        SUDOKU.print_original_container()


    Methods and Attributes
    ------------------------------------------------------
    solve(): Method
                - will solve the puzzle

    print_container(): Method
                    - will show the puzzle
                    - finished or starting depending on if you have run solve()

    print_original_container(): Method
                    - will always show the original container
                    - even afte ryou have run solve()

    container: Attribute
                    - will hold puzzle
                    - less pretty than print_container()
    '''

    def __init__(self, container):
        self.original_container = deepcopy(container)
        self.container = container
        self.subtract_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def check_horizontal(self, row_num):
        '''
        Removes invalid values from possible outcomes in each row
        '''
        return self.subtract_set - set(self.container[row_num])

    def check_vertical(self, col_num):
        '''
        Removes invalid values from possible outcomes in each column
        '''
        ret_set = []
        for row_idx in range(9):
            ret_set.append(self.container[row_idx][col_num])
        return self.subtract_set - set(ret_set)

    def check_square(self, row_num, col_num):
        '''
        Removes invalid values from possible outcomes in each square
        '''
        first = [0, 1, 2]
        second = [3, 4, 5]
        third = [6, 7, 8]
        find_square = [first, second, third]
        for num_in_square in find_square:
            if row_num in num_in_square:
                row = num_in_square
            if col_num in num_in_square:
                col = num_in_square
        ret_set = []
        for row_val in row:
            for col_val in col:
                ret_set.append(self.container[row_val][col_val])
        return self.subtract_set - set(ret_set)

    def get_poss_vals(self, row_num, col_num):
        '''
        Uses checks for square, horizontal, and vertical to determine possible cell value
        '''
        poss_vals = list(
            self.check_square(
                row_num,
                col_num).intersection(
                self.check_horizontal(
                    row_num)).intersection(
                    self.check_vertical(
                        col_num)))
        return poss_vals

    def explicit_solver(self):
        '''
        Run through possible values and fill in missing values in sudoku puzzle
        '''
        stump_count = 1
        for row_idx in range(9):
            for col_idx in range(9):
                if self.container[row_idx][col_idx] == 0:
                    poss_vals = self.get_poss_vals(row_idx, col_idx)
                    if len(poss_vals) == 1:
                        self.container[row_idx][col_idx] = list(poss_vals)[0]
                        stump_count = 0
        return self.container, stump_count

    def implicit_solver(self, row_idx, col_idx):
        '''
        An internal function used in get_poss_vals that solves by looking
        at row, col, and 3x3 grid combos for possible solutions
        Args:
            row_idx (int): row value
            col_idx (int): col value
        Returns:
            self.puzzle (list): list of lists of sudoku puzzle
        '''
        if self.container[row_idx][col_idx] == 0:
            poss_vals = self.get_poss_vals(row_idx, col_idx)

            # check row
            row_poss = []
            for col_num in range(9):
                if col_num == col_idx:
                    continue
                if self.container[row_idx][col_num] == 0:
                    for val in self.get_poss_vals(row_idx, col_num):
                        row_poss.append(val)
            if len(set(poss_vals) - set(row_poss)) == 1:
                self.container[row_idx][col_idx] = list(
                    set(poss_vals) - set(row_poss))[0]

            # check column
            col_poss = []
            for row_num in range(9):
                if row_num == row_idx:
                    continue
                if self.container[row_num][col_idx] == 0:
                    for val in self.get_poss_vals(row_num, col_idx):
                        col_poss.append(val)
            if len(set(poss_vals) - set(col_poss)) == 1:
                self.container[row_idx][col_idx] = list(
                    set(poss_vals) - set(col_poss))[0]

            # check square
            first = [0, 1, 2]
            second = [3, 4, 5]
            third = [6, 7, 8]
            find_square = [first, second, third]
            for num_in_square in find_square:
                if row_idx in num_in_square:
                    row = num_in_square
                if col_idx in num_in_square:
                    col = num_in_square
            square_poss = []
            for row_val in row:
                for col_val in col:
                    if self.container[row_val][col_val] == 0:
                        for val in self.get_poss_vals(row_val, col_val):
                            square_poss.append(val)
            if len(set(poss_vals) - set(square_poss)) == 1:
                self.container[row_idx][col_idx] = list(
                    set(poss_vals) - set(square_poss))[0]
        return self.container

    def print_container(self):
        '''
        Print the puzzle
        '''
        print()
        print()
        for row_idx, row in enumerate(self.container):
            for val_idx, val in enumerate(row):
                if (val_idx) % 3 == 0 and val_idx < 8 and val_idx > 0:
                    print("|", end=' ')
                print(val, end=' ')
            print()
            if (row_idx - 2) % 3 == 0 and row_idx < 8:
                print("_____________________", end='')
                print()
            print()

    def print_original_container(self):
        '''
        Print the puzzle
        '''
        print()
        print()
        for row_idx, row in enumerate(self.original_container):
            for val_idx, val in enumerate(row):
                if (val_idx) % 3 == 0 and val_idx < 8 and val_idx > 0:
                    print("|", end=' ')
                print(val, end=' ')
            print()
            if (row_idx - 2) % 3 == 0 and row_idx < 8:
                print("_____________________", end='')
                print()
            print()

    def solve(self):
        '''
        Solve the puzzle!
        '''
        # using explicit solver
        zero_count = 0
        for row_vals in self.container:
            for val in row_vals:
                if val == 0:
                    zero_count += 1

        print()
        print('Solving puzzle')
        print(f'There are {zero_count} moves I have to make!')
        print('To see solution use the `print_container()` method')
        print('To see the original use the `print_original_container()` method')
        solving = True

        while solving:
            # Solver Portion
            self.container, stump_count = self.explicit_solver()

            # Loop-Breaking Portion
            zero_count = 0
            for row_vals in self.container:
                for val in row_vals:
                    if val == 0:
                        zero_count += 1
            if zero_count == 0:
                solving = False
            if stump_count > 0:
                for row_idx in range(9):
                    for col_idx in range(9):
                        self.container = self.implicit_solver(row_idx, col_idx)


def create_sudoku():
    '''
    Creates starter sudoku table
    '''
    container = []
    container.append([0, 0, 0, 0, 0, 8, 3, 0, 0])
    container.append([0, 0, 0, 0, 2, 4, 0, 9, 0])
    container.append([0, 0, 4, 0, 7, 0, 0, 0, 6])
    container.append([0, 0, 0, 0, 0, 3, 0, 7, 9])
    container.append([7, 5, 0, 0, 0, 0, 0, 8, 4])
    container.append([9, 2, 0, 5, 0, 0, 0, 0, 0])
    container.append([4, 0, 0, 0, 9, 0, 1, 0, 0])
    container.append([0, 3, 0, 4, 6, 0, 0, 0, 0])
    container.append([0, 0, 5, 8, 0, 0, 0, 0, 0])
    return container


if __name__ == "__main__":
    PUZZLE = create_sudoku()
    SUDOKU = SudokuSolver(PUZZLE)
    SUDOKU.print_container()
    SUDOKU.solve()
    SUDOKU.print_container()
