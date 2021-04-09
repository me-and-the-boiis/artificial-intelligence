from enum import Enum

class Level(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4

ND = 9
class Sudoku:
    def __init__(self, level):
        self.board = None
        self.level = level
        self.generate(self.level)

    def generate(self, level):
        self.board = [
            [0, 3, 0, 0, 7, 0, 0, 5, 0], 
            [5, 0, 0, 1, 0, 6, 0, 0, 9], 
            [0, 0, 1, 0, 0, 0, 4, 0, 0], 
            [0, 9, 0, 0, 5, 0, 0, 6, 0], 
            [6, 0, 0, 4, 0, 2, 0, 0, 7], 
            [0, 4, 0, 0, 1, 0, 0, 3, 0], 
            [0, 0, 2, 0, 0, 0, 8, 0, 0], 
            [9, 0, 0, 3, 0, 5, 0, 0, 2], 
            [0, 1, 0, 0, 2, 0, 0, 7, 0]
        ]

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
