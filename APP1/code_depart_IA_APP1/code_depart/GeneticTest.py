#This is is a file to test our code

def genetic_test():
    #test the genetic algorithm
    import genetic
    import Maze
    #Init maze
    mazefile='assets/mazeLarge_3'
    maze = Maze.Maze(mazefile)
    maze.make_maze_item_lists()

    #Run test for every monster in it
    for monster in maze.monsterList:
        genetic.testGA(monster)




if __name__=='__main__':
    genetic_test()