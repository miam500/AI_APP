import csv
from queue import PriorityQueue
from swiplserver import PrologMQI


class Tile:
    def __init__(self):
        self.pos = (0, 0)
        self.father = None
        self.h = 0
        self.g = 0


class Astar:
    def __init__(self, mazefile, start, goal):
        self.roadmap = []
        with open(mazefile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.roadmap.append(row)
        self.node_dict = {}
        self.start = start
        self.goal = goal
        self.openQ = PriorityQueue()
        self.closedQ = []
        self.populate_node(start, start)

    def find_path(self):
        while not self.expand_tree():
            pass
        return self.generate_path()

    def expand_tree(self):
        explored_node = self.node_dict[self.openQ.get()[1]]

        if explored_node.pos == self.goal:
            self.closedQ.append(explored_node)
            return True

        request_a = "actionsPossibles("
        request = self.prolog_parser(explored_node.pos)
        request_b = ", R)."
        request = request_a+request+request_b

        result = []
        with PrologMQI() as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("[prolog/planification].")
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

    def generate_path(self):
        path_node = self.closedQ.pop()
        father_node = self.node_dict[path_node.father]
        path = [path_node]
        while not father_node.pos == self.start:
            path_node = father_node
            father_node = self.node_dict[path_node.father]
            path = [path_node] + path
        coordinate_path = []
        for tile in path:
            coordinate_path.append(tile.pos)
        return coordinate_path

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


star = Astar('assets/mazeMedium_0', (0, 1), (15, 22))
path = star.find_path()
print(path)




