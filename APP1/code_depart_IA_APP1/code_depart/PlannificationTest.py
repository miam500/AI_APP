from Planification import *

mazepath = 'assets/mazeMedium_2'
good_start_goal = [(0, 1), (15, 22)]
bad_start_goal = [(0, 1), (15, 23)]
invalid_start = [(0, 0), (15, 22)]
tile_size = 50
valid_path = [(75, 25), (75, 75), (75, 125), (75, 175), (75, 225), (75, 275), (75, 325), (75, 375), (125, 375),
              (175, 375), (225, 375), (225, 425), (225, 475), (275, 475), (325, 475), (375, 475), (425, 475),
              (475, 475), (475, 525), (475, 575), (525, 575), (575, 575), (625, 575), (675, 575), (675, 625),
              (675, 675), (725, 675), (775, 675), (825, 675), (875, 675), (875, 725), (925, 725), (975, 725),
              (1025, 725), (1075, 725), (1125, 725), (1125, 775)]


def all_success_test():
    planner = Planner(mazepath, tile_size)
    path = planner.create_plan()
    try:
        assert(path == valid_path)
    except:
        print("Test 1 Failed")
        return
    print("Test 1 Passed")


def bad_start_goal_test():
    roadmap = []
    with open(mazepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            roadmap.append(row)
    astar = Astar(roadmap, bad_start_goal[0], bad_start_goal[1], tile_size)
    try:
        astar.find_path()
    except:
        print("Test 2 Passed")
        return
    print("Test 2 Failed")

#This test should produce an assertion error wich stops the code after the first 2 tests
def invalid_start_test():
    roadmap = []
    with open(mazepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            roadmap.append(row)
    astar = Astar(roadmap, invalid_start[0], invalid_start[1], tile_size)
    astar.find_path()



all_success_test()
bad_start_goal_test()
invalid_start_test()

