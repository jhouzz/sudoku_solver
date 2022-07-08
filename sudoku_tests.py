'''
There are two types of tests that are checked with this file

* We check that a puzzle is valid using `SudokuTests`
* We check that a SudokuSolver in sudoku.py returns a correct solution

If you run:
    ```bash
    $ python sudoku_tests.py
    ```

A successful run of this file should look like:

    ```bash
    Original Puzzle:

    0 0 0 | 0 0 8 | 3 0 0

    0 0 0 | 0 2 4 | 0 9 0

    0 0 4 | 0 7 0 | 0 0 6
    _____________________

    0 0 0 | 0 0 3 | 0 7 9

    7 5 0 | 0 0 0 | 0 8 4

    9 2 0 | 5 0 0 | 0 0 0
    _____________________

    4 0 0 | 0 9 0 | 1 0 0

    0 3 0 | 4 6 0 | 0 0 0

    0 0 5 | 8 0 0 | 0 0 0

    Your Puzzle Looks Valid.  Try to Solve It!

    Solving puzzle
    There are 40 moves I have to make!
    To see solution use the `print_container()` method
    To see the original use the `print_original_container()` method
    You passed test1 with the following table:
    ```

You can run these tests with your own solver by updating `sudoku.py` with your solver.

You can also test that your own puzzles are valid by updating the function:

    ```python
    def test1():
        container = []
        container.append([5, 1, 0, 9, 7, 0, 0, 0, 8])
        container.append([4, 0, 3, 0, 0, 8, 1, 0, 0])
        container.append([0, 0, 8, 0, 0, 5, 0, 4, 6])
        container.append([3, 8, 0, 7, 0, 1, 0, 6, 2])
        container.append([0, 0, 7, 0, 2, 0, 5, 0, 0])
        container.append([2, 9, 0, 4, 0, 6, 0, 7, 3])
        container.append([1, 3, 0, 6, 0, 0, 9, 0, 0])
        container.append([0, 0, 4, 3, 0, 0, 6, 0, 7])
        container.append([7, 0, 0, 0, 8, 2, 0, 1, 4])

        container_sol = []
        container_sol.append([5, 1, 6, 9, 7, 4, 2, 3, 8])
        container_sol.append([4, 7, 3, 2, 6, 8, 1, 5, 9])
        container_sol.append([9, 2, 8, 1, 3, 5, 7, 4, 6])
        container_sol.append([3, 8, 5, 7, 9, 1, 4, 6, 2])
        container_sol.append([6, 4, 7, 8, 2, 3, 5, 9, 1])
        container_sol.append([2, 9, 1, 4, 5, 6, 8, 7, 3])
        container_sol.append([1, 3, 2, 6, 4, 7, 9, 8, 5])
        container_sol.append([8, 5, 4, 3, 1, 9, 6, 2, 7])
        container_sol.append([7, 6, 9, 5, 8, 2, 3, 1, 4])

        return container, container_sol
    ```

with your own `container` and `container_sol`. Then simply add your own check similar to:

    ```python
    TEST_ORIGINAL, TEST_SOLUTION = test1()
    SUDOKU_TWO = SudokuSolver(TEST_ORIGINAL)
    SUDOKU_TWO.solve()
    MY_SOLUTION = SUDOKU_TWO.container
    if MY_SOLUTION == TEST_SOLUTION:
        print("You passed test1!")
    else:
        print("You failed test1!")
    ```
'''

import numpy as np


class SudokuTests():
    '''
    Input:
        puzzle (list):
            - puzzle you want to check is valid
            - should be in the below format:
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

    You can then check that you have a valid `puzzle` in the following way:

        TEST = SudokuTests(puzzle)
        print(TEST.check_valid())

    Valid puzzle should have the following properties:
     - not empty
     - no duplicate values in a row
     - no duplicate values in a column
     - no duplicate values in a square
    '''

    def __init__(self, puzzle):
        '''
        Input:
            puzzle (list):
                - puzzle you want to check is valid
                - should be in the below format:
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
        '''
        self.puzzle = puzzle

    def valid_helper(self, hlder):
        '''
        Helper function used in `check_valid` method
             - Check there are no duplicates in `hlder`
        '''
        hlder = np.array(hlder)
        if len(set(hlder[hlder > 0])) != len(hlder[hlder > 0]):
            return True
        return False

    def check_valid(self):
        '''
        Check puzzle is valid
             - not empty
             - no duplicate values in a row
             - no duplicate values in a column
             - no duplicate values in a square
        '''
        # check container is not empty
        if np.sum(self.puzzle) == 0:
            return "Cannot solve. Multiple possible solutions"

        # check rows and columns
        con = np.array(self.puzzle)
        for val in range(9):
            if len(set(con[val, :][con[val, :] > 0])) != len(
                    con[val, :][con[val, :] > 0]):
                return "Cannot solve. Start Board Has Impossibility."

            if len(set(con[:, val][con[:, val] > 0])) != len(
                    con[:, val][con[:, val] > 0]):
                return "Cannot solve. Start Board Has Impossibility."

        # check 3x3 squares - do for all combos of `:3`, `3:6`, and `6:` for
        # rows and columns
        hlder = []
        for row in con[:3, :3]:
            hlder.extend(row)
        if self.valid_helper(hlder):
            return "Cannot solve. Start Board Has Impossibility."

        # in solution code, there are more cases like the above...
        # they would go here

        # check max and min within bounds
        if np.max(con) > 9 or np.min(con) < 0:
            return "Cannot solve. Input Value Out of Bounds."

        return "Your Puzzle Looks Valid.  Try to Solve It!"


def test1():
    '''
    Test to ensure sudoku solver returns a correct answer for this puzzle
    '''
    container = []
    container.append([5, 1, 0, 9, 7, 0, 0, 0, 8])
    container.append([4, 0, 3, 0, 0, 8, 1, 0, 0])
    container.append([0, 0, 8, 0, 0, 5, 0, 4, 6])
    container.append([3, 8, 0, 7, 0, 1, 0, 6, 2])
    container.append([0, 0, 7, 0, 2, 0, 5, 0, 0])
    container.append([2, 9, 0, 4, 0, 6, 0, 7, 3])
    container.append([1, 3, 0, 6, 0, 0, 9, 0, 0])
    container.append([0, 0, 4, 3, 0, 0, 6, 0, 7])
    container.append([7, 0, 0, 0, 8, 2, 0, 1, 4])

    container_sol = []
    container_sol.append([5, 1, 6, 9, 7, 4, 2, 3, 8])
    container_sol.append([4, 7, 3, 2, 6, 8, 1, 5, 9])
    container_sol.append([9, 2, 8, 1, 3, 5, 7, 4, 6])
    container_sol.append([3, 8, 5, 7, 9, 1, 4, 6, 2])
    container_sol.append([6, 4, 7, 8, 2, 3, 5, 9, 1])
    container_sol.append([2, 9, 1, 4, 5, 6, 8, 7, 3])
    container_sol.append([1, 3, 2, 6, 4, 7, 9, 8, 5])
    container_sol.append([8, 5, 4, 3, 1, 9, 6, 2, 7])
    container_sol.append([7, 6, 9, 5, 8, 2, 3, 1, 4])

    return container, container_sol


if __name__ == "__main__":
    from sudoku import SudokuSolver, create_sudoku

    # check that original puzzle is valid
    PUZZLE = create_sudoku()
    SUDOKU = SudokuSolver(PUZZLE)
    SUDOKU.print_container()  # print puzzle
    TEST = SudokuTests(PUZZLE)  # instantiate tests
    print(TEST.check_valid())  # print if the puzzle is a valid sudoku puzzle

    # check that sudoku solver works correctly
    TEST_ORIGINAL, TEST_SOLUTION = test1()
    SUDOKU_TWO = SudokuSolver(TEST_ORIGINAL)
    SUDOKU_TWO.solve()
    MY_SOLUTION = SUDOKU_TWO.container
    if MY_SOLUTION == TEST_SOLUTION:
        print("You passed test1!")
    else:
        print("You failed test1!")
