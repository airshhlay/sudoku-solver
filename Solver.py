# CS3243 Introduction to Artificial Intelligence
# Project 2

import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        # create the visited list (do not try out the same square again if it does not work)
        self.domains = {}
        

    def solve(self):
        # TODO: Write your code here
        initialise(self.puzzle, self.domains)
        recursiveSolver(self.ans, self.domains)
        # self.ans is a list of lists
        return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.
    
# this method does a rough initial inference by:
# Deducing the available values for each square, based on the initial unsolved puzzle
# in addition, it also initialise the not tried dictionary that keeps track of the values we have and have not tried
def initialise(puzzle, domains):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0: # if not assigned yet
                square = (i,j)

                domains[square] = set(i for i in range(1,10))
                
                # check the row
                for otherSquare in getOtherSquaresInRow(square):
                    val = puzzle[otherSquare[0]][otherSquare[1]]
                    if val in domains[square]:
                        domains[square].remove(val)
                
                # check the row
                for otherSquare in getOtherSquaresInCol(square):
                    val = puzzle[otherSquare[0]][otherSquare[1]]
                    if val in domains[square]:
                        domains[square].remove(val)

                # check the row
                for otherSquare in getOtherSquaresInBlock(square):
                    val = puzzle[otherSquare[0]][otherSquare[1]]
                    if val in domains[square]:
                        domains[square].remove(val)

# this function gets the next square (x,y) that has the minimum number of avail values in its domain
def getNextSquare(currAns, domains):
    smallestSize = None
    nextSquare = None
    for square in domains:
        row, col = square
        if currAns[row][col] == 0:
            if nextSquare == None or len(domains[square]) < smallestSize:
                smallestSize = len(domains[square])
                nextSquare = square
    return nextSquare

def recursiveSolver(currAns, domains):
    if goalTest(currAns):
        return True

    square = getNextSquare(currAns, domains) # get the next square to assign
    row, col = square

    domain = domains[square] # the vals this square can take
    
    for val in domain:
        # try this value for this square
        currAns[row][col] = val
        changedDomains = {} # domains affected by this assignment
        if eliminateValsForOtherSquares(currAns, domains, changedDomains, square, val): # other squares valid after this assignment
            tempHolder = domains.copy()
            domains.update(changedDomains) # update the domains
            if recursiveSolver(currAns, domains):
                return True
            # revert the domains to the old version
            domains = tempHolder 
        continue

    currAns[row][col] = 0
    return False # unable to assign anything, not success


def eliminateValsForOtherSquares(currAns, domains, changedDomains, square, val):
    for otherSquare in getOtherSquares(square):
       # print("-----")
        if not eliminateVal(currAns, domains, changedDomains, otherSquare, val): # this assignment violates constraint
           # print(str(otherSquare) + " will be invalid")
            return False
        #print(str(otherSquare) + " valid")

    return True
                

# eliminate the value that was just assigned from the other squares that will be affected
def eliminateVal(currAns, domains, changedDomains, otherSquare, val):
    if otherSquare not in domains: # this is a pre-filled square
        row, col = otherSquare
        if currAns[row][col] == val: # violates constraint
            return False
    else:
        if otherSquare in changedDomains: # if this square has had its domain changed before
            if val in changedDomains[otherSquare]:
                if len(changedDomains[otherSquare]) == 1:
                    return False
                changedDomains[otherSquare].remove(val)
        else:
            changedDomains[otherSquare] = set([domainVal for domainVal in domains[otherSquare]])
            if val in changedDomains[otherSquare]:
                if len(changedDomains[otherSquare]) == 1:
                    return False
                changedDomains[otherSquare].remove(val)
    return True


# helper method that gets all the other squares that will have to be checked when we assign a value to the given square
def getOtherSquares(square):
    otherSquares = set()
    otherSquares.update(getOtherSquaresInRow(square))
    otherSquares.update(getOtherSquaresInCol(square))
    otherSquares.update(getOtherSquaresInBlock(square))
    return otherSquares

# helper method that retrieves the other squares in the same row as the given square
def getOtherSquaresInRow(square):
    row, col = square
    squares = set()
    for j in range(9):
        if j != col:
            otherSquare = (row, j)
            squares.add(otherSquare)
    return squares

# helper method that retrieves the other squares in the same col as the given square
def getOtherSquaresInCol(square):
    row, col = square
    squares = set()
    for i in range(9):
        if i != row:
            otherSquare = (i, col)
            squares.add(otherSquare)
    return squares

# helper method that retrieves the other squares in the same block as the given square
def getOtherSquaresInBlock(square):
    row, col = square
    squares = set()
    rowIndexStart = row // 3 * 3 # use floor division to see which square from the left (0 - 2)
    colIndexStart = col // 3 * 3# use floor divison to see which square from the top (0 - 2)
    for i in range(rowIndexStart, rowIndexStart + 3):
        for j in range(colIndexStart, colIndexStart + 3):
            otherSquare = (i,j)
            if otherSquare != square:
                squares.add(otherSquare)
    return squares

def goalTest(currAns):
    for i in range(9):
        for j in range(9):
            if currAns[i][j] == 0:
                return False
    return True

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")