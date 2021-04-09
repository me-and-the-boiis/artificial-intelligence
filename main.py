import collections
import numpy as np
from copy import *
import random


def update(index, new_index, state):
    new = deepcopy(state)
    new[index[0]][index[1]] = state[new_index[0]][new_index[1]]
    new[new_index[0]][new_index[1]] = state[index[0]][index[1]]
    return new

class Puzzle:
    def __init__(self, current, goal, size):
        self.current = current
        self.goal = goal
        self.size = size
        self.visited = []
        for i in range(size):
            for j in range(size):
                if current[i][j] == 0:
                    self.blank_index = (i, j)
                    return

    def up(self):
        # self.blank_index[0] -= 1
        new_index = (self.blank_index[0] - 1, self.blank_index[1])
        self.current = update(self.blank_index, new_index, self.current)
        self.blank_index = new_index
        print2d(self.current)

    def down(self):
        # self.blank_index[0] += 1
        new_index = (self.blank_index[0] + 1, self.blank_index[1])
        self.current = update(self.blank_index, new_index, self.current)
        self.blank_index = new_index
        print2d(self.current)

    def left(self):
        # self.blank_index[1] -= 1
        new_index = (self.blank_index[0], self.blank_index[1] - 1)
        self.current = update(self.blank_index, new_index, self.current)
        self.blank_index = new_index
        print2d(self.current)

    def right(self):
        # self.blank_index[1] += 1
        new_index = (self.blank_index[0], self.blank_index[1] + 1)
        self.current = update(self.blank_index, new_index, self.current)
        self.blank_index = new_index
        print2d(self.current)

    def dfs(self):
        # Check if current already visited
        for node in self.visited:
            if self.current == node:
                return
        if self.current == self.goal:
            return
        self.visited.append(self.current)
        # Generate new node(s) with move
        if self.blank_index[0] != 0:
            self.up()
            self.dfs()
        if self.blank_index[1] != 0:
            self.left()
            self.dfs()
        if self.blank_index[0] != self.size - 1:
            self.down()
            self.dfs()
        if self.blank_index[1] != self.size - 1:
            self.right()
            self.dfs()


def print2d(lst):
    for r in lst:
        for c in r:
            print(c, end="\t")
        print()
    print()


def randomme(n):
    oned = np.array(random.sample(range(n*n), n*n))
    return np.reshape(oned, (n, n))


def main():
    init = randomme(2)
    goal = randomme(2)
    print2d(init)
    print2d(goal)
    # solver = Puzzle(init, goal, len(init))
    # solver.dfs()


if __name__ == '__main__':
    main()
