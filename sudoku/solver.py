from sudoku import *
from population import *

class Solver:
    def __init__(self, sudoku, nCandidate, nGeneration, nMutation):
        self.sudoku = sudoku
        self.nCandidate = nCandidate  # Number of candidates.
        self.nGeneration = nGeneration  # Number of generations.
        self.nMutation = nMutation  # Number of mutations.
    
    def initPopulation(self):
        self.population = Population(self.nCandidate, self.sudoku)
