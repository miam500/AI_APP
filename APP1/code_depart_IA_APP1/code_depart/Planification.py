import csv
from queue import PriorityQueue
from swiplserver import PrologMQI
import numpy as np


class Tile:
    def __init__(self):
        self.pos = (0, 0)
        self.father = None
        self.h = 0
        self.g = 0


class Astar:
    def __init__(self, roadmap, start, goal, tile_size):
        self.roadmap = roadmap
        self.node_dict = {}
        self.start = start
        self.goal = goal
        self.openQ = PriorityQueue()
        self.closedQ = []
        self.populate_node(start, start)
        self.tile_size = tile_size
        self.down = [(i, int(self.tile_size/2)) for i in range(self.tile_size)]
        self.up = [(i, int(self.tile_size / 2)) for i in range(self.tile_size, 0, -1)]
        self.right = [(int(self.tile_size/2), i) for i in range(self.tile_size)]
        self.left = [(int(self.tile_size / 2), i) for i in range(self.tile_size, 0, -1)]

    def find_path(self):
        with PrologMQI() as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("[prolog/planification].")
                while not self.expand_tree(prolog_thread):
                    pass
                return self.generate_tile_path()

    def expand_tree(self, prolog_thread):
        explored_node = self.node_dict[self.openQ.get()[1]]

        if explored_node.pos == self.goal:
            self.closedQ.append(explored_node)
            return True

        request_a = "actionsPossibles("
        request = self.prolog_parser(explored_node.pos)
        request_b = ", R)."
        request = request_a+request+request_b

        result = prolog_thread.query(request)

        for direction in result[0]['R']:
            if direction == "left" and not (explored_node.pos[0], explored_node.pos[1] - 1) == explored_node.father:
                self.populate_node((explored_node.pos[0], explored_node.pos[1]-1), explored_node.pos)
            if direction == "right" and not (explored_node.pos[0], explored_node.pos[1] + 1) == explored_node.father:
                self.populate_node((explored_node.pos[0], explored_node.pos[1] + 1), explored_node.pos)
            if direction == "up" and not (explored_node.pos[0] - 1, explored_node.pos[1]) == explored_node.father:
                self.populate_node((explored_node.pos[0] - 1, explored_node.pos[1]), explored_node.pos)
            if direction == "down" and not (explored_node.pos[0] + 1, explored_node.pos[1]) == explored_node.father:
                self.populate_node((explored_node.pos[0] + 1, explored_node.pos[1]), explored_node.pos)

        self.closedQ.append(explored_node)
        return False

    def populate_node(self, pos, father):
        new_node = Tile()
        new_node.pos = pos
        new_node.father = father
        self.node_dict[new_node.pos] = new_node
        self.openQ.put((self.calculate_cost(new_node), new_node.pos))

    def calculate_cost(self, node):
        if self.start == node.pos:
            node.g = 0
            node.h = abs(self.goal[0] - node.pos[0]) + abs(self.goal[1] - node.pos[1])
            return node.h + node.g

        else:
            node.g = self.node_dict[node.father].g + 1
            node.h = abs(self.goal[0] - node.pos[0]) + abs(self.goal[1] - node.pos[1])
            return node.g + node.h

    def generate_tile_path(self):
        path_node = self.closedQ.pop()
        father_node = self.node_dict[path_node.father]
        path = [path_node]
        while not father_node.pos == self.start:
            path_node = father_node
            father_node = self.node_dict[path_node.father]
            path = [path_node] + path
        coordinate_path = [(int(self.start[1] * self.tile_size + self.tile_size/2), int(self.start[0] * self.tile_size + self.tile_size/2))]
        for tile in path:
            coordinate_path.append((int(tile.pos[1] * self.tile_size + self.tile_size/2), int(tile.pos[0] * self.tile_size + self.tile_size/2)))

        return coordinate_path

    def generate_path(self):
        tile_path = self.generate_tile_path()
        tile_path_len = len(tile_path)
        pixel_path = []
        for idx in range(tile_path_len-1):
            if tile_path[idx][0] - tile_path[idx+1][0] == -1:
                pixel_path = np.append(pixel_path, [np.array(self.down) + (np.array(tile_path[idx]) * self.tile_size)])
            elif tile_path[idx][0] - tile_path[idx+1][0] == 1:
                pixel_path = np.append(pixel_path, [np.array(self.up) + (np.array(tile_path[idx]) * self.tile_size)])
            elif tile_path[idx][1] - tile_path[idx+1][1] == -1:
                pixel_path = np.append(pixel_path, [np.array(self.right) + (np.array(tile_path[idx]) * self.tile_size)])
            elif tile_path[idx][1] - tile_path[idx+1][1] == 1:
                pixel_path = np.append(pixel_path, [np.array(self.left) + (np.array(tile_path[idx]) * self.tile_size)])
        if tile_path[-2][0] - tile_path[-1][0] == -1:
            pixel_path = np.append(pixel_path, [np.array(self.down) + (np.array(tile_path[-1]) * self.tile_size)])
        elif tile_path[-2][0] - tile_path[-1][0] == 1:
            pixel_path = np.append(pixel_path, [np.array(self.up) + (np.array(tile_path[-1]) * self.tile_size)])
        elif tile_path[-2][1] - tile_path[-1][1] == -1:
            pixel_path = np.append(pixel_path, [np.array(self.right) + (np.array(tile_path[-1]) * self.tile_size)])
        elif tile_path[-2][1] - tile_path[-1][1] == 1:
            pixel_path = np.append(pixel_path, [np.array(self.left) + (np.array(tile_path[-1]) * self.tile_size)])

        return pixel_path

    def prolog_parser(self, pos):
        state_list = []
        if pos[1] > 0:
            type = self.predicate_transform(self.roadmap[pos[0]][pos[1]-1], "left")
            state_list.append(type)
        if pos[1] < 23:
            type = self.predicate_transform(self.roadmap[pos[0]][pos[1]+1], "right")
            state_list.append(type)
        if pos[0] > 0:
            type = self.predicate_transform(self.roadmap[pos[0]-1][pos[1]], "up")
            state_list.append(type)
        if pos[0] < 15:
            type = self.predicate_transform(self.roadmap[pos[0]+1][pos[1]], "down")
            state_list.append(type)

        symbol_state_list = "["
        for state in state_list:
            symbol_state_list = symbol_state_list+state+","
        symbol_state_list = symbol_state_list+"wall(fire)]"
        return symbol_state_list

    def predicate_transform(self, symbol, direction):
        if symbol == '1':
            return "wall("+direction+")"
        elif symbol == '0':
            return "empty("+direction+")"
        elif symbol == 'O':
            return "block("+direction+")"
        elif symbol == 'C':
            return "coin("+direction+")"
        elif symbol == 'T':
            return "treasure("+direction+")"
        elif symbol == 'M':
            return "monster("+direction+")"
        elif symbol == "E":
            return "goal("+direction+")"
        elif symbol == "S":
            return "start("+direction+")"

class Planner:
    def __init__(self, mazefile, tile_size, strategy='finnish'):
        self.mazefile = mazefile
        self.roadmap = []
        with open(mazefile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.roadmap.append(row)
        self.strategy = strategy
        self.tile_size = tile_size

    def obtain_objectives(self):
        objective_pairs = []
        if self.strategy == 'greedy':
            start = (0, 0)
            goal = (0, 0)
            treasure = []
            for row, values in enumerate(self.roadmap):
                for column, value in enumerate(values):
                    if value == 'S':
                        start = (row, column)
                    elif value == 'E':
                        goal = (row, column)
                    elif value == 'C' or value == 'T':
                        treasure = np.append(treasure, (row, column))
            #dist = np.array([abs(treasure[0][0] - start[0]) + abs(treasure[0][1] - start[1])])
            #for idx in range(len(treasure)-1):
            #    dist = np.append(abs(treasure[idx+1][0] - treasure[idx][0]) + abs(treasure[idx+1][1] - treasure[idx][1]))
            objective_pairs = np.array([(start, treasure[0])])
            for idx in range(int(len(treasure)/2)):
                objective_pairs = np.append(objective_pairs, (treasure[2*idx], treasure[idx+1]))
            objective_pairs = np.append(treasure[-1], goal)

        else:
            start = (0, 0)
            goal = (0, 0)
            for row, values in enumerate(self.roadmap):
                for column, value in enumerate(values):
                    if value == 'S':
                        start = (row, column)
                    elif value == 'E':
                        goal = (row, column)
            objective_pairs = (start, goal)

        return objective_pairs

    def create_plan(self):
        objective_pairs = self.obtain_objectives()
        paths = []
        for idx in range(len(objective_pairs)-1):
            print(objective_pairs[idx], objective_pairs[idx+1])
            aStar = Astar(self.roadmap, objective_pairs[idx], objective_pairs[idx+1], self.tile_size)
            paths = np.append(paths, aStar.find_path())
        path = []
        for idx in range(int(len(paths)/2)):
            path.append((int(paths[2*idx]), int(paths[2*idx+1])))
        return path

planner = Planner('assets/mazeMedium_0', 50)
path = planner.create_plan()
print(path)
# small maze 50
# large maze 40