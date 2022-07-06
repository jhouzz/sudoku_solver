import time
import numpy as np

class SudokuSolver():
    def __init__(self, container):
        self.container = container
        self.subtract_set = {1,2,3,4,5,6,7,8,9}

    def check_horizontal(self, i, j):
        return self.subtract_set - set(self.container[i])

    def check_vertical(self, i, j):
        ret_set = []
        for x in range(9):
            ret_set.append(self.container[x][j])
        return self.subtract_set - set(ret_set)

    def check_square(self, i, j):
        first = [0,1,2]
        second = [3,4,5]
        third = [6,7,8]
        find_square = [first, second, third]
        for l in find_square:
            if i in l:
                row = l
            if j in l:
                col = l
        ret_set = []
        for x in row:
            for y in col:
                ret_set.append(self.container[x][y])
        return self.subtract_set - set(ret_set)

    def get_poss_vals(self, i, j):
        poss_vals = list(self.check_square(i,j).intersection(self.check_horizontal(i,j)).intersection(self.check_vertical(i,j)))
        return poss_vals

    def explicit_solver(self):
        stump_count = 1
        for i in range(9):
            for j in range(9):
                if self.container[i][j] == 0:
                    poss_vals = self.get_poss_vals(i,j)
                    if len(poss_vals) == 1:
                        self.container[i][j] = list(poss_vals)[0]
                        self.print_container()
                        stump_count = 0
        return self.container, stump_count

    def implicit_solver(self, i, j):
        if self.container[i][j] == 0:
            poss_vals = self.get_poss_vals(i,j)

            #check row
            row_poss = []
            for y in range(9):
                if y == j:
                    continue
                if self.container[i][y] == 0:
                    for val in self.get_poss_vals(i,y):
                        row_poss.append(val)
            if len(set(poss_vals)-set(row_poss)) == 1:
                self.container[i][j] = list(set(poss_vals)-set(row_poss))[0]
                self.print_container()

            #check column
            col_poss = []
            for x in range(9):
                if x == i:
                    continue
                if self.container[x][j] == 0:
                    for val in self.get_poss_vals(x,j):
                        col_poss.append(val)
            if len(set(poss_vals)-set(col_poss)) == 1:
                self.container[i][j] = list(set(poss_vals)-set(col_poss))[0]
                self.print_container()

            #check square
            first = [0,1,2]
            second = [3,4,5]
            third = [6,7,8]
            find_square = [first, second, third]
            for l in find_square:
                if i in l:
                    row = l
                if j in l:
                    col = l
            square_poss = []
            for x in row:
                for y in col:
                    if self.container[x][y] == 0:
                        for val in self.get_poss_vals(x,y):
                            square_poss.append(val)
            if len(set(poss_vals)-set(square_poss)) == 1:
                self.container[i][j] = list(set(poss_vals)-set(square_poss))[0]
                self.print_container()
        return self.container

    def print_container(self):
        for i, row in enumerate(self.container):
            for j, val in enumerate(row):
                if (j)%3 == 0 and j<8 and j>0:
                    print("|",end=' ')
                print(val,end=' ')
            print()
            if (i-2)%3 == 0 and i<8:
                print("_____________________", end='')
                print()
            print()
        print()
        print("||||||||||||||||||||||")
        print()

    def solve(self):
        # using explicit solver
        start = time.time()
        zero_count = 0
        for l in self.container:
            for v in l:
                if v == 0:
                    zero_count += 1

        print(f'There are {zero_count} moves I have to make!')
        print()

        self.print_container()
        print()
        solving = True

        while solving:
            #Solver Portion
            self.container, stump_count = self.explicit_solver()

            #Loop-Breaking Portion
            zero_count = 0
            for l in self.container:
                for v in l:
                    if v == 0:
                        zero_count += 1
            if zero_count==0:
                solving=False
            if stump_count > 0:
                for i in range(9):
                    for j in range(9):
                        self.container = self.implicit_solver(i, j)
        print()
        print('That took', time.time()-start, 'seconds!')

if __name__ == "__main__":
    # create container
    container = []
    container.append([0,0,0,0,0,8,3,0,0])
    container.append([0,0,0,0,2,4,0,9,0])
    container.append([0,0,4,0,7,0,0,0,6])
    container.append([0,0,0,0,0,3,0,7,9])
    container.append([7,5,0,0,0,0,0,8,4])
    container.append([9,2,0,5,0,0,0,0,0])
    container.append([4,0,0,0,9,0,1,0,0])
    container.append([0,3,0,4,6,0,0,0,0])
    container.append([0,0,5,8,0,0,0,0,0])

    #print container
    print(container)

    # run test and print results
    test_puzzle = SudokuSolver(container)
    test_puzzle.solve()
    test_puzzle.print_container()
