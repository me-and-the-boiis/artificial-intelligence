import numpy
import random
from sudoku import *
random.seed()

class Candidate:
    def __init__(self):
        self.board = []
        self.fitness = None
    
    def updateFitness(self):
        pass

    def __str__(self):
        line = "+-----------------------+"
        result = line
        for i in range(len(self.board)):
            row = "\n| "
            for j in range(len(self.board)):
                row += str(self.board[i][j]) + " "
                if j%3 == 2:
                    row += "| "
            if i%3 == 2:
                row += '\n' + line
            result+=row
        return result

def permutation(array, check = [False for i in range(10)], cur = []):
    if not array:
        return [cur.copy()]
    result = []
    for i in array[0]:
        if check[i]:
            continue
        cur.append(i)
        check[i] = True
        result += permutation(array[1:], check, cur)
        cur.pop()
        check[i] = False
    return result

class Population:
    """ A set of candidate solutions to the Sudoku """
    def __init__(self, size, sudoku):
        self.candidates = []
        self.size = size
        self.sudoku = sudoku
        self.genCandidate()
    
    def genCandidate(self):
        print("Generating candidate")
        sudoku = self.sudoku
        self.candidates = []

        self.helper = [[sudoku.getValidNumbers(i,j) for j in range(0, ND)] for i in range(0, ND)]
        # print("Hepler:")
        # print(self.helper)
        validAllRows = []
        k = 1;
        for i in range(ND):
            validAllRows.append(self.genValidRow(i))
        for i in range(self.size):
            cand = Candidate()
            for row in range(ND):
                cand.board.append(validAllRows[row][random.randint(0, len(validAllRows[row])-1)])

            self.candidates.append(cand)
        print("Generate candidate completed")

    def genValidRow(self, row):
        helper = self.helper
        sudoku = self.sudoku

        validRows = []

        currentRow = []
        currentRowIndex = []
        for i in range(ND):
            if helper[row][i]:
                currentRow.append(helper[row][i])
                currentRowIndex.append(i)
        
        permutations = permutation(currentRow)

        for child in permutations:
            tmp = sudoku.board[row].copy()
            for i in range(len(currentRowIndex)):
                tmp[currentRowIndex[i]] = child[i]
            validRows.append(tmp) 
        return validRows