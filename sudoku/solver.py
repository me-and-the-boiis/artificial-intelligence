from sudoku import *
from population import *

class Solver:
    def __init__(self, sudoku, nCandidate, nGeneration, nMutation):
        self.sudoku = sudoku
        self.nCandidate = nCandidate  # Number of candidates.
        self.nGeneration = nGeneration  # Number of generations.
        self.nMutation = nMutation  # Number of mutations.
        self.nElites = int(0.05*self.nCandidate)    # Number of Elite candidates
        self.phi = 0
        self.sigma = 0
        self.mutation_rate = 0.06
    
    def initPopulation(self):
        self.population = Population(self.nCandidate, self.sudoku)
