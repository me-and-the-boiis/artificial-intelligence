from enum import Enum
import random
random.seed()

ND = 9

class Level(Enum):
    EASY = 36
    MEDIUM = 32
    HARD = 28
    EXPERT = 24

def swap2R(arr, r1, r2):
    tmp = arr[r1]
    arr[r1] = arr[r2]
    arr[r2] = tmp   

def swap2C(arr, r1, r2):
    for j in range(ND):
        tmpr = arr[j][r1]
        arr[j][r1] = arr[j][r2]
        arr[j][r2] = tmpr

class Sudoku:
    def __init__(self, level):
        self.board = None
        self.level = level
        self.generate(self.level)

    def generate(self, level):        
        print("Creating sudoku board")
        self.board = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 1, 2, 3], 
            [7, 8, 9, 1, 2, 3, 4, 5, 6], 
            [2, 3, 4, 5, 6, 7, 8, 9, 1], 
            [5, 6, 7, 8, 9, 1, 2, 3, 4], 
            [8, 9, 1, 2, 3, 4, 5, 6, 7], 
            [3, 4, 5, 6, 7, 8, 9, 1, 2], 
            [6, 7, 8, 9, 1, 2, 3, 4, 5], 
            [9, 1, 2, 3, 4, 5, 6, 7, 8]
        ]
        for i in range(500):
            r1 = random.randint(0,8)
            r2 = r1+random.randint(1,2)
            r2 = r2-((int(r2/3)-int(r1/3))*3 if r1 else 0)
            swap2C(self.board, r1, r2)
            swap2R(self.board, r1, r2)
            r1 = r1%3
            r2 = r2%3
            for j in range(3):
                swap2C(self.board, r1*3+j, r2*3+j)
            for j in range(3):
                swap2R(self.board, r1*3+j, r2*3+j)
        count = [[9 for j in range(ND)] for i in range(3)]
        cutoffs = 81 - self.level.value
        while cutoffs:
            i = 0
            j = 0
            k = random.randint(1, cutoffs+self.level.value-1)
            # print(k)
            while k:                
                i += 1
                if i == 9:
                    i = 0
                    j += 1
                    if j == 9:
                        j = 0
                if self.board[i][j]:
                    k -= 1
            min = int(self.level.value/10)
            if count[0][i] == min or count[1][j] == min or count[2][int(i/3)*3+int(j/3)] == min:
                continue
            count[0][i] -= 1
            count[1][j] -= 1
            count[2][int(i/3)*3+int(j/3)] -= 1
            self.board[i][j] = 0
            cutoffs -= 1
        print(self)

    def getValidNumbers(self, row, column):
        if self.board[row][column] != 0:
            return []
        validNumbers = [i+1 for i in range(ND)]
        blockIndex = (row-row%3, column-column%3)
        
        inValidNumbers = []
        for i in range(ND):
            inValidNumbers.append(self.board[row][i])
            inValidNumbers.append(self.board[i][column])
            inValidNumbers.append(self.board[blockIndex[0]+int(i/3)][blockIndex[1]+int(i%3)])
        
        for i in inValidNumbers:
            if (i in validNumbers):
                validNumbers.remove(i)
        return validNumbers

    def isRowDup(self, row, value):
        pass

    def isColumnDup(self, column, value):
        pass

    def isBlockDup(self, index, value):
        pass

    def __str__(self):
        line = "+-----------------------+"
        result = line
        for i in range(ND):
            row = "\n| "
            for j in range(ND):
                row += (str(self.board[i][j]) if self.board[i][j] else " ") + " "
                if j%3 == 2:
                    row += "| "
            if i%3 == 2:
                row += '\n' + line
            result+=row
        return result

    def getScore(self):
        score = 0
        for i in range(ND):
            rowCheck = [True for i in range(ND)]
            colCheck = [True for i in range(ND)]
            blockCheck = [True for i in range(ND)]
            for j in range(ND):
                score += rowCheck[self.board[i][j]-1] + colCheck[self.board[j][i]-1] + blockCheck[self.board[i-i%3+int(j/3)][(i%3)*3 + j%3 ]-1]
                colCheck[self.board[j][i]-1] = False
                blockCheck[self.board[i-i%3+int(j/3)][(i%3)*3 + j%3 ] -1] = False
                rowCheck[self.board[i][j]-1] = False
        return score

# sudoku = Sudoku(Level.EASY)