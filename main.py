import collections
import numpy as np
from copy import *
import random


class Board:
    def __init__(self, state, height):
        self.state = state
        self.height = height
        for x in range(len(init)):
            for y in range(len(init)):
                if init[x][y] == 0:
                    self.index = (x, y)

    def __eq__(self, other):
        # return (self.state == other.state).all() and self.index == other.index
        return self.state == other.state


def movement(index, new_index, node):
    new = Board(deepcopy(node.state), node.height + 1)
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
    visited = list([Board(root, 0)])
    stack = list([Board(root, 0)])
    correct_path = []
    while stack:
        node = stack.pop()
        if node.height > len(correct_path):
            correct_path.append(node)
        elif node.height < len(correct_path):
            correct_path.pop()
        # if (node.state == goal).all():
        if node.state == goal:
            return correct_path
        # Generate possible paths
        possible_paths = reversed(generate(node))
        for path in possible_paths:
            if path not in visited:
                stack.append(path)
                visited.append(path)


def randomme(n):
    oned = np.array(random.sample(range(n*n), n*n))
    return np.reshape(oned, (n, n))


# init = randomme(2)
# goal = randomme(2)
init = [[1, 2, 5],
        [3, 4, 0],
        [6, 7, 8]]
# goal = [[0, 1, 2],
#         [3, 4, 5],
#         [6, 7, 8]]
goal = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]
# init = [[2, 1],
#         [0, 3]]
# goal = [[1, 0],
#         [2, 3]]
# print(init)
# print(goal)


def main():
    solver = dfs(init)
    print(init, end="")
    for i in range(len(solver)):
        print(" -> ", solver[i].state, end="")


if __name__ == '__main__':
    main()
