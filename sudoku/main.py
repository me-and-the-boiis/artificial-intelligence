from sudoku import *
from solver import *
def main():
    # print("Hello World!")
    sudoku = Sudoku(Level.EASY)
    nCandidate = 10
    nGeneration = 2
    nMutation = 2

    solver = Solver(sudoku, nCandidate, nGeneration, nMutation)
    solver.initPopulation()
    solver.solve()
    print(solver.population.candidates[0])
    # solver.population.sort()
if __name__ == "__main__":
    main()