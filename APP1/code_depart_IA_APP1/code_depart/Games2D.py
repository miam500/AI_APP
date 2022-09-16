from pygame.locals import *
import pygame

from Player import *
from Maze import *
from Constants import *
from Planification import Planner
import FuzzyLogic as fuzzy



class App:
    windowWidth = WIDTH
    windowHeight = HEIGHT
    player = 0

    item_value = 2

    def __init__(self, mazefile, fuzz_ctrl, tile_size):
        self._running = True
        self._win = False
        self._dead = False
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self._clock = None
        self.level = 0
        self.score = 0
        self.timer = 0.0
        self.player = Player()
        self.maze = Maze(mazefile)
        self.fuzz = fuzz_ctrl
        self.tile_size = tile_size
        self.mazefile = mazefile
        self.fuzz = fuzzy.createFuzzyController()
        self.planner = Planner(self.mazefile, self.tile_size, 'greedy')
        self.path = []


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self._clock = pygame.time.Clock()
        pygame.display.set_caption("Dungeon Crawler")
        pygame.time.set_timer(pygame.USEREVENT, 10)
        self._running = True
        self.maze.make_maze_wall_list()
        self.maze.make_maze_item_lists()
        self._image_surf = pygame.image.load("assets/kickboxeuse.png")
        self.player.set_position(1.5 * self.maze.tile_size_x, 0.5 * self.maze.tile_size_y)
        self.player.set_size(PLAYER_SIZE*self.maze.tile_size_x, PLAYER_SIZE*self.maze.tile_size_x)
        self._image_surf = pygame.transform.scale(self._image_surf, self.player.get_size())
        self._block_surf = pygame.image.load("assets/wall.png")
        # do generation thing
        self.path = self.planner.create_plan()

    def on_keyboard_input(self, keys):
        if keys[K_RIGHT] or keys[K_d]:
            self.move_player_right()

        if keys[K_LEFT] or keys[K_a]:
            self.move_player_left()

        if keys[K_UP] or keys[K_w]:
            self.move_player_up()

        if keys[K_DOWN] or keys[K_s]:
            self.move_player_down()

        # Utility functions for AI
        if keys[K_p]:
            self.maze.make_perception_list(self.player, self._display_surf)
            print(self.player.get_position())
            # returns a list of 4 lists of pygame.rect inside the perception radius
            # the 4 lists are [wall_list, obstacle_list, item_list, monster_list]
            # item_list includes coins and treasure

        if keys[K_m]:
            for monster in self.maze.monsterList:
                print(monster.mock_fight(self.player))
            # returns the number of rounds you win against the monster
            # you need to win all four rounds to beat it
        if keys[K_t]:
            # self.fuzz.input['direction'] = -0.25 #up: -0.75,down -0.25, left 0.25, right 0.75
            # self.fuzz.input['y_ob'] = 0.0

            pass

        if (keys[K_ESCAPE]):
            self._running = False


    # FONCTION À Ajuster selon votre format d'instruction
    def on_AI_input(self, instruction, direction):
        instruction = round(instruction+0.5)
        if direction == 'DOWN' or 'UP':
            if instruction < 0:
                self.move_player_left()
            else:
                self.move_player_right()
        if direction == 'left' or 'right':
            if instruction < 0:
                self.move_player_up()
            else:
                self.move_player_down()

    def move_player_right(self):
        self.player.moveRight()
        if self.on_wall_collision() or self.on_obstacle_collision():
            self.player.moveLeft()

    def move_player_left(self):
        self.player.moveLeft()
        if self.on_wall_collision() or self.on_obstacle_collision():
            self.player.moveRight()

    def move_player_up(self):
        self.player.moveUp()
        if self.on_wall_collision() or self.on_obstacle_collision():
            self.player.moveDown()

    def move_player_down(self):
        self.player.moveDown()
        if self.on_wall_collision() or self.on_obstacle_collision():
            self.player.moveUp()

    def on_wall_collision(self):
        collide_index = self.player.get_rect().collidelist(self.maze.wallList)
        if not collide_index == -1:
            # print("Collision Detected!")
            return True
        return False

    def on_obstacle_collision(self):
        collide_index = self.player.get_rect().collidelist(self.maze.obstacleList)
        if not collide_index == -1:
            # print("Collision Detected!")
            return True
        return False

    def on_coin_collision(self):
        collide_index = self.player.get_rect().collidelist(self.maze.coinList)
        if not collide_index == -1:
            self.maze.coinList.pop(collide_index)
            return True
        else:
            return False

    def on_treasure_collision(self):
        collide_index = self.player.get_rect().collidelist(self.maze.treasureList)
        if not collide_index == -1:
            self.maze.treasureList.pop(collide_index)
            return True
        else:
            return False

    def on_monster_collision(self):
        for monster in self.maze.monsterList:
            if self.player.get_rect().colliderect(monster.rect):
                return monster
        return False

    def on_exit(self):
        return self.player.get_rect().colliderect(self.maze.exit)

    def maze_render(self):
        self._display_surf.fill((0, 0, 0))
        self.maze.draw(self._display_surf, self._block_surf)
        font = pygame.font.SysFont(None, 32)
        text = font.render("Coins: " + str(self.score), True, BLACK)
        self._display_surf.blit(text, (WIDTH - 120, 10))
        text = font.render("Time: " + format(self.timer, ".2f"), True, BLACK)
        self._display_surf.blit(text, (WIDTH - 300, 10))

    def on_render(self):
        self.maze_render()
        self._display_surf.blit(self._image_surf, (self.player.x, self.player.y))
        pygame.display.flip()

    def on_win_render(self):
        self.maze_render()
        font = pygame.font.SysFont(None, 120)
        text = font.render("CONGRATULATIONS!", True, GREEN)
        self._display_surf.blit(text, (0.1 * self.windowWidth, 0.4 * self.windowHeight))
        pygame.display.flip()

    def on_death_render(self):
        self.maze_render()
        font = pygame.font.SysFont(None, 120)
        text = font.render("YOU DIED!", True, RED)
        self._display_surf.blit(text, (0.1 * self.windowWidth, 0.4 * self.windowHeight))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()
        print('hello')
        step = 0
        while self._running:
            self._clock.tick(GAME_CLOCK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.USEREVENT:
                    self.timer += 0.01
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            self.on_keyboard_input(keys)
            # self.on_AI_input(instruction)
            if self.on_coin_collision():
                self.score += 1
            if self.on_treasure_collision():
                self.score += 10
            monster = self.on_monster_collision()
            if monster:
                if monster.fight(self.player):
                    self.maze.monsterList.remove(monster)
                else:
                    self._running = False
                    self._dead = True
            if self.on_exit():
                self._running = False
                self._win = True
            self.on_render()
            if self.path[step+1][0] - self.path[step][0] < 0:
                self.deplacement(self.path[step], "LEFT")
                if self.player.get_position()[0] < self.path[step+1][0]:
                    step += 1
            if self.path[step+1][0] - self.path[step][0] > 0:
                self.deplacement(self.path[step], "RIGHT")
                if self.player.get_position()[0] > self.path[step+1][0]:
                    step += 1
            if self.path[step+1][1] - self.path[step][1] < 0:
                self.deplacement(self.path[step], "UP")
                if self.player.get_position()[1] < self.path[step+1][1]:
                    step += 1
            if self.path[step+1][1] - self.path[step][1] > 0:
                self.deplacement(self.path[step], "DOWN")
                if self.player.get_position()[1] > self.path[step+1][1]:
                    print("going down")
                    step += 1
            # do genetic thing


        while self._win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._win = False
            self.on_win_render()

        while self._dead:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._dead = False
            self.on_death_render()

        self.on_cleanup()


    def deplacement(self, imaginary_line, direction):

        wall, obstacle, item, monstre = self.maze.make_perception_list(self.player, self._display_surf)
        position_x, position_y = self.player.get_position()
        obs_x = -30
        obs_y = -30
        it_x = -30
        it_y = -30
        o_in_my_way = []
        i_in_my_way = []
        # imaginary_line = (60, 60)
        # direction = 'LEFT'
        if direction == 'DOWN':
            # ---- direction objectif ----
            self.move_player_down()
            self.move_player_down()
            # -- determine les inputs ------------------------
            position_x = imaginary_line[0] - (position_x + 10)
            # ---- selection obstacle
            for o in obstacle:
                if position_y <= o[1]:
                    o_in_my_way.append(o)
            if o_in_my_way:
                obs_x = o_in_my_way[min((abs(o[1]), j) for j, o in enumerate(o_in_my_way))[1]][0]
                obs_x = imaginary_line[0] - (obs_x + 5)
            # ---- selection item
            for it in item:
                if position_y <= it[1]:
                    i_in_my_way.append(it)
            if i_in_my_way:
                it_x = i_in_my_way[min((abs(it[1]), j) for j, it in enumerate(i_in_my_way))[1]][0]
                it_x = imaginary_line[0] - (it_x + 5)

            # --- send les inputs ---------------------
            #print(it_x, obs_x, position_x)
            # ---- input obst
            self.fuzz.input['obst'] = obs_x
            # ---- input personnage
            self.fuzz.input['pos'] = position_x
            # ---- input item
            self.fuzz.input['item'] = it_x

            self.fuzz.compute()

        elif direction == 'UP':
            # ---- direction objectif ----
            self.move_player_up()
            self.move_player_up()
            # -- determine les inputs ------------------------
            position_x = imaginary_line[0] - (position_x + 10)
            # ---- selection obstacle
            for o in obstacle:
                if position_y + 20 >= o[1]:
                    o_in_my_way.append(o)
            if o_in_my_way:
                obs_x = o_in_my_way[max((abs(o[1]), j) for j, o in enumerate(o_in_my_way))[1]][0]
                obs_x = imaginary_line[0] - (obs_x + 5)
            # ---- selection item
            for it in item:
                if position_y + 20 >= it[1]:
                    i_in_my_way.append(it)
            if i_in_my_way:
                it_x = i_in_my_way[max((abs(it[1]), j) for j, it in enumerate(i_in_my_way))[1]][0]
                it_x = imaginary_line[0] - (it_x + 5)

            # --- send les inputs ---------------------
            #print(it_x, obs_x, position_x)
            # ---- input obst
            self.fuzz.input['obst'] = obs_x
            # ---- input personnage
            self.fuzz.input['pos'] = position_x
            # ---- input item
            self.fuzz.input['item'] = it_x

            self.fuzz.compute()

        elif direction == 'LEFT':
            # ---- direction objectif ----
            self.move_player_left()
            self.move_player_left()
            self.move_player_left()
            # -- determine les inputs ------------------------
            position_y = imaginary_line[1] - (position_y + 10)
            # ---- selection obstacle ----
            for o in obstacle:
                if position_x >= o[0]:
                    o_in_my_way.append(o)
            if o_in_my_way:
                obs_y = o_in_my_way[max((abs(o[1]), j) for j, o in enumerate(o_in_my_way))[1]][1]
                obs_y = imaginary_line[1] - (obs_y + 5)
            # ---- selection item ----
            for it in item:
                if position_x >= it[0]:
                    i_in_my_way.append(it)
            if i_in_my_way:
                it_y = i_in_my_way[max((abs(it[1]), j) for j, it in enumerate(i_in_my_way))[1]][1]
                it_y = imaginary_line[1] - (it_y + 5)

            # --- send inputs
            #print(it_y, obs_y, position_y)
            # ---- input obst
            self.fuzz.input['obst'] = obs_y
            # ---- input personnage
            self.fuzz.input['pos'] = position_y
            # ---- input item
            self.fuzz.input['item'] = it_y

            self.fuzz.compute()

        elif direction == 'RIGHT':
            # ---- direction objectif ----
            self.move_player_right()
            self.move_player_right()
            # -- determine les inputs ------------------------
            position_y = imaginary_line[1] - (position_y + 10)
            # ---- selection obstacle ----
            o_in_my_way = []
            for o in obstacle:
                if position_x <= o[0]:
                    o_in_my_way.append(o)
            if o_in_my_way:
                obs_y = o_in_my_way[max((abs(o[1]), j) for j, o in enumerate(o_in_my_way))[1]][1]
                obs_y = imaginary_line[1] - (obs_y + 5)
            # ---- selection item ----
            for it in item:
                if position_x <= it[0]:
                    i_in_my_way.append(it)
            if i_in_my_way:
                it_y = i_in_my_way[max((abs(it[1]), j) for j, it in enumerate(i_in_my_way))[1]][1]
                it_y = imaginary_line[1] - (it_y + 5)
            # --- faire les inputs

            #print(obs_y + 5, position_y + 10)
            # ---- input obst
            self.fuzz.input['obst'] = obs_y
            # ---- input personnage
            self.fuzz.input['pos'] = position_y
            # ---- input item
            self.fuzz.input['item'] = it_y

            self.fuzz.compute()

        # get the output from the fuzzy system
        move = self.fuzz.output['move']
        print(move)

        self.on_AI_input(move, direction)
        # self.on_AI_input(movey, 'y')
        self.on_render()