import numpy as np

from Maze import *
from Games2D import *

class Tile():
    def __init__(self, wall=False, monster=False, obst=False, coin=False, treasure=False, up=False, down=False, left=False, right=False, pos=(-1,-1), start=False, goal=False, ):
        self.wall = wall
        self.monster = monster
        self.block = obst
        self.coin = coin
        self.treasure = treasure
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.pos = pos
        self.start = start
        self.goal = goal
        self.father = Tile()
        self.h = 0
        self.g = 0


def look_map(mazefile):
    grid = []

    with open(mazefile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            grid.append(row)

    mat_tile = np.zeros( (len(grid), len(grid[0])), dtype=Tile )
    for i, l in enumerate(grid):
        for j, c in enumerate(l):
            print(c)
            if grid[i][j] == '1':
                mat_tile[i][j] = Tile(wall=True, pos=(i,j))
            elif grid[i][j] == 'S':
                up, down, left, right = look_around((i,j), grid)
                mat_tile[i][j] = Tile(start=True, up=up, down=down, left=left, right=right, pos=(i,j))
            elif grid[i][j] == '0':
                up, down, left, right = look_around((i,j), grid)
                mat_tile[i][j] = Tile(up=up, down=down, left=left, right=right, pos=(i,j))
            elif grid[i][j] == 'T':
                up, down, left, right = look_around((i,j), grid)
                mat_tile[i][j] = Tile(treasure=True, up=up, down=down, left=left, right=right, pos=(i,j))
            elif grid[i][j] == 'C':
                up, down, left, right = look_around((i,j), grid)
                mat_tile[i][j] = Tile(coin=True, up=up, down=down, left=left, right=right, pos=(i,j))
            elif grid[i][j] == 'M':
                up, down, left, right = look_around((i, j), grid)
                mat_tile[i][j] = Tile(monster=True, up=up, down=down, left=left, right=right, pos=(i, j))
            elif grid[i][j] == 'E':
                mat_tile[i][j] = Tile(goal=True, pos=(i,j))
    return mat_tile

def look_around(pos, grid):
    up, down, left, right = False, False, False, False
    if not grid[pos[0]][pos[1]-1] == '1':
        left = True
    if not grid[pos[0]][pos[1]+1] == '1':
        right = True
    if not grid[pos[0]-1][pos[1]] == '1':
        up = True
    if not grid[pos[0]+1][pos[1]] == '1':
        down = True
    return up, down, left, right

