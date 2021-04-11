import numpy as np
from copy import *
import random
import time
random.seed()


class Board:
    def __init__(self, state, height, move):
        self.state = state
        self.height = height
        self.move = move
        for x in range(len(state)):
            for y in range(len(state)):
                if state[x][y] == 0:
                    self.index = (x, y)

    def __eq__(self, other):
        # return (self.state == other.state).all() and self.index == other.index
        return self.state == other.state


def movement(index, new_index, node, mv):
    new = Board(deepcopy(node.state), node.height + 1, mv)
    new.state[index[0]][index[1]] = node.state[new_index[0]][new_index[1]]
    new.state[new_index[0]][new_index[1]] = node.state[index[0]][index[1]]
    new.index = new_index
    return new


def generate(node):
    nodes = []
    # Up
    if node.index[0] != 0:
        new_index = (node.index[0] - 1, node.index[1])
        nodes.append(movement(node.index, new_index, node, "UP"))
    # Down
    if node.index[0] != len(node.state) - 1:
        new_index = (node.index[0] + 1, node.index[1])
        nodes.append(movement(node.index, new_index, node, "DOWN"))
    # Left
    if node.index[1] != 0:
        new_index = (node.index[0], node.index[1] - 1)
        nodes.append(movement(node.index, new_index, node, "LEFT"))
    # Right
    if node.index[1] != len(node.state) - 1:
        new_index = (node.index[0], node.index[1] + 1)
        nodes.append(movement(node.index, new_index, node, "RIGHT"))
    return nodes


def state2number(state):
    idx = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            idx |= (i*3+j) << (val * 3)
    return idx


def dfs(root):
    # visited = list([Board(root, 0)])
    visited = list([state2number(root)])
    stack = list([Board(root, 0, "INIT")])
    correct_path = []
    while stack:
        # print(len(visited))
        node = stack.pop()
        if node.height > len(correct_path) - 1:
            correct_path.append(node)
        else:
            while node.height < len(correct_path):
                correct_path.pop()
            correct_path.append(node)
        # if (node.state == goal).all():
        if node.state == goal:
            return correct_path
        # Generate possible paths, if height of node exceeds expected result height, change path
        if node.height < 20:
            possible_paths = reversed(generate(node))
            for path in possible_paths:
                ha = state2number(path.state)
                if ha not in visited:
                    stack.append(path)
                    visited.append(ha)
    return []


def randomme(n):
    oned = np.array(random.sample(range(n*n), n*n))
    return np.reshape(oned, (n, n))


goal = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]


def initInit(goal, count):
    def move(init, i, j, si,  sj):
        tmp = init[i][j]
        init[i][j] = init[i+si][j+sj]
        init[i + si][j + sj] = tmp
        return (i+si, j+sj)

    for i in range(len(goal)):
        for j in range(len(goal[i])):
            if goal[i][j] == 0:
                break
        if goal[i][j] == 0:
            break
    i = 0
    j = 0
    init = deepcopy(goal)
    for n in range(count):
        r = random.randint(1,4)
        i, j = (move(init, i, j, 1, 0) if r == 1 and i<len(goal)-1
                else move(init, i, j, -1, 0) if r == 2 and i>0
                else move(init, i, j, 0, 1) if r == 3 and j<len(goal)-1
                else move(init, i, j, 0, -1) if r == 4 and j>0
                else (i, j)
                )
    return init


def main():
    init = initInit(goal, 20)
    solver = dfs(init)
    print(init, end="")
    for i in range(len(solver)):
        print(" -> ", solver[i].state, end="")
    print()
    for i in range(len(solver)):
        print(solver[i].move, end=" -> ")
    print("DONE")


start_time = time.time()
main()
print("\nExecution time: %s seconds\n" % (time.time() - start_time))
