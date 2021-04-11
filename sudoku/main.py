from sudoku import *
from solver import *
def main():
    # print("Hello World!")
    sudoku = Sudoku(Level.EASY)
    nCandidate = 500
    nGeneration = 10
    nMutation = 2

    solver = Solver(sudoku, nCandidate, nGeneration, nMutation)
    solver.initPopulation()
    solver.solve()
    # solver.population.sort()
if __name__ == "__main__":
    main()