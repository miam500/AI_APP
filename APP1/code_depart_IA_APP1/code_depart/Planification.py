
import csv
import numpy as np
from queue import PriorityQueue

class Tile:
    def __init__(self):
        self.pos = (0, 0)
        self.Wall = False
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.coin = False
        self.treasure = False
        self.monster = False
        self.block = False
        self.father = Tile()
        self.h = 0
        self.g = 0

class Astar:
    def __init__(self, roadmap, start, goal):
        self.roadmap = roadmap
        self.start = start
        self.goal = goal
        self.openQ = PriorityQueue()
        self.closedQ = []

        self.openQ.put(self.calculate_cost(self.roadmap[self.start[0]][self.start[1]]), self.roadmap[self.start[0]][self.start[1]])

    def find_path(self):
        while not self.expand_tree():
            pass
        return self.generate_path()

    def expand_tree(self):
        explored_node = self.openQ.get()

        if explored_node.pos == self.goal:
            self.closedQ = self.closedQ.append(explored_node)
            return True

        if explored_node.up and not explored_node.monster:
            new_node = self.roadmap[explored_node.pos[0]][explored_node.pos[1]-1]
            new_node.father = explored_node
            self.openQ.put(self.calculate_cost(new_node), new_node)
        if explored_node.down and not explored_node.monster:
            new_node = self.roadmap[explored_node.pos[0]][explored_node.pos[1]+1]
            new_node.father = explored_node
            self.openQ.put(self.calculate_cost(new_node), new_node)
        if explored_node.left and not explored_node.monster:
            new_node = self.roadmap[explored_node.pos[0]-1][explored_node.pos[1]]
            new_node.father = explored_node
            self.openQ.put(self.calculate_cost(new_node), new_node)
        if explored_node.right and not explored_node.monster:
            new_node = self.roadmap[explored_node.pos[0]+1][explored_node.pos[1]]
            new_node.father = explored_node
            self.openQ.put(self.calculate_cost(new_node), new_node)

        self.closedQ = self.closedQ.append(explored_node)
        return False

    def calculate_cost(self, node):
        if self.start == node.pos:
            node.g = 0
            node.h = abs(self.goal[0] - node.pos[0]) + abs(self.goal[1] - node.pos[1])
            return node.h + node.g

        else:
            node.g = node.father.g + 1
            node.h = abs(self.goal[0] - node.pos[0]) + abs(self.goal[1] - node.pos[1])
            return node.g + node.h

    def generate_path(self):
        path_node = self.closedQ.pop()
        father_node = path_node.father
        path = [path_node]
        while not father_node.pos == self.start:
            path_node = father_node
            father_node = path_node.father
            path = [path_node] + path

        return path
    