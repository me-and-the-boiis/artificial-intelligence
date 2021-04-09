import collections
import numpy as np
from copy import *
import random


class Board:
    def __init__(self, state):
        self.state = state
        for x in range(len(init)):
            for y in range(len(init)):
                if init[x][y] == 0:
                    self.index = (x, y)


def movement(index, new_index, node):
    new = Board(deepcopy(node.state))
    new.state[index[0]][index[1]] = node.state[new_index[0]][new_index[1]]
    new.state[new_index[0]][new_index[1]] = node.state[index[0]][index[1]]
    new.index = new_index
    return new


def generate(node):
    nodes = []
    # Up
    if node.index[0] != 0:
        new_index = (node.index[0] - 1, node.index[1])
        nodes.append(movement(node.index, new_index, node))
    # Down
    if node.index[0] != len(init) - 1:
        new_index = (node.index[0] + 1, node.index[1])
        nodes.append(movement(node.index, new_index, node))
    # Left
    if node.index[1] != 0:
        new_index = (node.index[0], node.index[1] - 1)
        nodes.append(movement(node.index, new_index, node))
    # Right
    if node.index[1] != len(init) - 1:
        new_index = (node.index[0], node.index[1] + 1)
        nodes.append(movement(node.index, new_index, node))
    return nodes


def dfs(root):
    visited = set()
    stack = list([Board(root)])
    while stack:
        node = stack.pop()
        for i in visited:
            if node == i:
                continue
        visited.add(node)
        if node.state == goal:
            return stack
        # Generate possible paths
        possible_paths = generate(node)
        for path in possible_paths:
            if path not in visited:
                stack.append(path)
                visited.add(path)


def randomme(n):
    oned = np.array(random.sample(range(n*n), n*n))
    return np.reshape(oned, (n, n))


init = randomme(2)
goal = randomme(2)
# init = [[0, 1],
#         [2, 3]]
# goal = [[1, 0],
#         [2, 3]]
print(init)
print(goal)


def main():
    dfs(init)


if __name__ == '__main__':
    main()
