from sudoku import *
import numpy
import random

random.seed()

class Candidate:
    def __init__(self):
        self.board = []
        self.score = 0
    
    def updateFitness(self):
        score = 81
        for i in range(ND):
            colCheck = [True for i in range(ND)]
            blockCheck = [True for i in range(ND)]
            for j in range(ND):
                score += colCheck[self.board[j][i]-1] + blockCheck[self.board[i-i%3+int(j/3)][(i%3)*3 + j%3 ]-1]
                colCheck[self.board[j][i]-1] = False
                blockCheck[self.board[i-i%3+int(j/3)][(i%3)*3 + j%3 ] -1] = False
        self.score = score

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

    def mutate(self, mutate_rate, sudoku):
        r = random.uniform(0, 1.1)
        while (r > 1):  # Outside [0, 1] boundary - choose another
            r = random.uniform(0, 1.1)

        success = False
        if (r < mutate_rate):  # Mutate.
            while (not success):
                row = random.randint(0, 8)
                # row2 = row1

                from_column = random.randint(0, 8)
                to_column = random.randint(0, 8)
                while from_column == to_column:
                    from_column = random.randint(0, 8)
                    to_column = random.randint(0, 8)
                if(sudoku.board[row][from_column] == 0 and sudoku.board[row][to_column] == 0):
                    # if (not self.is_column_duplicate(to_column, self.board[row1][from_column])
                    #     and not self.is_column_duplicate(from_column, self.board[row2][to_column])
                    #     and not self.is_block_duplicate(row2, to_column, self.board[row1][from_column])
                    #     and not self.is_block_duplicate(row1, from_column, self.board[row2][to_column])):
                        #Swap
                    temp = self.board[row][to_column]
                    self.board[row][to_column] = self.board[row][from_column]
                    self.board[row][from_column] = temp
                    success = True
        self.updateFitness()
        return success

    def is_row_duplicate(self, row, value):
        for column in range(0, 9):
            if (self.board[row][column] == value):
                return True
        return False

    def is_column_duplicate(self, col, value):
        for row in range(0, 9):
            if (self.board[row][col] == value):
                return True
        return False

    def is_block_duplicate(self, row, column, value):
        i = 3 * (int(row / 3))
        j = 3 * (int(column / 3))

        if    ((self.board[i][j] == value)
            or (self.board[i][j + 1] == value)
            or (self.board[i][j + 2] == value)
            or (self.board[i + 1][j] == value)
            or (self.board[i + 1][j + 1] == value)
            or (self.board[i + 1][j + 2] == value)
            or (self.board[i + 2][j] == value)
            or (self.board[i + 2][j + 1] == value)
            or (self.board[i + 2][j + 2] == value)):
            return True
        else:
            return False
        
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
        k = 1
        for i in range(ND):
            validAllRows.append(self.genValidRow(i))
        for i in range(self.size):
            cand = Candidate()
            for row in range(ND):
                cand.board.append(validAllRows[row][random.randint(0, len(validAllRows[row])-1)])

            self.candidates.append(cand)
        self.updateFitness()
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

    def updateFitness(self):
        for candidate in self.candidates:
            candidate.updateFitness()
        return

    def sort(self):
        """ Sort the population based on fitness. """
        self.candidates.sort(key=lambda x: x.score, reverse=True)
        return



