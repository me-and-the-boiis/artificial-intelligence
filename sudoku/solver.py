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
    def __init__(self):
        return

    def crossover(self, parent1, parent2, crossover_rate):
        """ Create two new child candidates by crossing over parent genes. """
        child1 = Candidate()
        child2 = Candidate()

        # Make a copy of the parent genes.
        child1.board = numpy.copy(parent1.board)
        child2.board = numpy.copy(parent2.board)

        r = random.uniform(0, 1.1)
        while (r > 1):  # Outside [0, 1] boundary. Choose another.
            r = random.uniform(0, 1.1)

        # Perform crossover.
        if (r < crossover_rate):
            # Pick a crossover point. Crossover must have at least 1 row (and at most Nd-1) rows.
            crossover_point1 = random.randint(0, 8)
            crossover_point2 = random.randint(1, 9)
            while (crossover_point1 == crossover_point2):
                crossover_point1 = random.randint(0, 8)
                crossover_point2 = random.randint(1, 9)

            if (crossover_point1 > crossover_point2):
                temp = crossover_point1
                crossover_point1 = crossover_point2
                crossover_point2 = temp

            for i in range(crossover_point1, crossover_point2):
                child1.board[i], child2.board[i] = self.crossover_rows(child1.board[i], child2.board[i])

        return child1, child2

    def crossover_rows(self, row1, row2):
        child_row1 = numpy.zeros(9)
        child_row2 = numpy.zeros(9)

        remaining = list(range(1, 10))
        cycle = 0

        while ((0 in child_row1) and (0 in child_row2)):  # While child rows not complete...
            if (cycle % 2 == 0):
                # Assign next unused value.
                index = self.find_unused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                child_row1[index] = row1[index]
                child_row2[index] = row2[index]
                next = row2[index]

                while (next != start):  # While cycle not done...
                    index = self.find_value(row1, next)
                    child_row1[index] = row1[index]
                    remaining.remove(row1[index])
                    child_row2[index] = row2[index]
                    next = row2[index]

                cycle += 1

            else:  # Odd cycle - flip board.
                index = self.find_unused(row1, remaining)
                start = row1[index]
                remaining.remove(row1[index])
                child_row1[index] = row2[index]
                child_row2[index] = row1[index]
                next = row2[index]

                while (next != start):  # While cycle not done...
                    index = self.find_value(row1, next)
                    child_row1[index] = row2[index]
                    remaining.remove(row1[index])
                    child_row2[index] = row1[index]
                    next = row2[index]

                cycle += 1

        return child_row1, child_row2

    def find_unused(self, parent_row, remaining):
        for i in range(0, len(parent_row)):
            if (parent_row[i] in remaining):
                return i

    def find_value(self, parent_row, value):
        for i in range(0, len(parent_row)):
            if (parent_row[i] == value):
                return i


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
                child1, child2 = cross.crossover(p1, p2, crossover_rate=1.0)
                child1.updateFitness()
                child2.updateFitness()

                preMutated = child1.score
                success = child1.mutate()
