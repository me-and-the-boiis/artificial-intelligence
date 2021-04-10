from sudoku import *
from population import *

class Tournament(object):
    def __init__(self):
        return

    def compete(self, candidates):
        c1 = candidates[random.randint(0, len(candidates) - 1)]
        c2 = candidates[random.randint(0, len(candidates) - 1)]
        f1 = c1.score
        f2 = c2.score

        if (f1 > f2):
            fittest = c1
            weakest = c2
        else:
            fittest = c2
            weakest = c1

        selection_rate = 0.85
        r = random.uniform(0, 1.1)
        while (r > 1):
            r = random.uniform(0, 1.1)
        if (r < selection_rate):
            return fittest
        else:
            return weakest

class CrossOver(object):
    pass

class Solver:
    def __init__(self, sudoku, nCandidate, nGeneration, nMutation):
        self.sudoku = sudoku
        self.nCandidate = nCandidate  # Number of candidates.
        self.nGeneration = nGeneration  # Number of generations.
        self.nMutation = nMutation  # Number of mutations.
        self.nElites = int(0.2*self.nCandidate)    # Number of Elite candidates
        self.phi = 0
        self.sigma = 0
        self.mutation_rate = 0.06

    def initPopulation(self):
        self.population = Population(self.nCandidate, self.sudoku)

    def solve(self):
        for generation in range(0, self.nGeneration):
            best_fitness = 0
            print("Generation %d" % generation)
            for c in range(0, self.nCandidate):
                fitness = self.population.candidates[c].score
                print(fitness)
                if fitness == 243:
                    print("Solution found at generation %d" % generation)
                    print(self.population.candidates[c])
                    return self.population.candidates[c]

                if fitness > best_fitness:
                    best_fitness = fitness

            print("Best: %d" % best_fitness)
            # next_gen = []
            self.population.sort()
            elites = []
            for i in range(0, self.nElites):
                elite = Candidate()
                elite.board = numpy.copy(self.population.candidates[i].board)
                elites.append(elite)
            for i in range(self.nElites, self.nCandidate, 2):
                #pick parents
                t = Tournament()
                p1 = t.compete(self.population.candidates)
                p2 = t.compete(self.population.candidates)

                cross = CrossOver()
