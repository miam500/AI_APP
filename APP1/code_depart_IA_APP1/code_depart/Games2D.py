from pygame.locals import *
import pygame

from Player import *
from Maze import *
from Constants import *


class App:
    windowWidth = WIDTH
    windowHeight = HEIGHT
    player = 0

    item_value = 2

    def __init__(self, mazefile):
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
            self.fuzz.input['direction'] = -0.25  # up: -0.75, -0.25, 0.25, 0.75
            self.fuzz.input['x_ob'] = 0.0
            # self.fuzz.input['y_ob'] = 0.0
            for i in range(100):
                wall, obstacle, item, monster = self.maze.make_perception_list(self.player, self._display_surf)
                position = self.player.get_position()
                obstruction = 0
                if wall:
                    for w in wall:
                        ob_vector = ((w[0] - position[0]) ** 2 + (w[1] - position[1]) ** 2) ** (1 / 2)
                        if (w[0] - position[0]) < 0:
                            ob_angle = degrees(atan2(w[0] - position[0], position[1] - w[1]))
                            v1_theta = atan2(position[1], position[0])
                            v2_theta = atan2(w[1], w[0])
                            r = (v2_theta - v1_theta) * (180.0 / math.pi)
                            #if r < 0:
                            #    r % 360
                            #print
                            #r
                        else:
                            ob_angle = atan2(w[0] - position[0], w[1] - position[1])
                        # obstruction = obstruction +
                if obstacle:
                    self.fuzz.input['x_ob'] = obstacle[0][0] - position[0]
                    # self.fuzz.input['y_ob'] = obstacle[0][1] - position[1]
                # elif item:
                #    self.fuzz.input['x_'] = item[0]
                #    self.fuzz.input['y_item'] = item[1]
                #
                # elif wall:
                # self.fuzz.input['item'] = None
                # self.fuzz.input['x_item'] = None
                # self.fuzz.input['y_item'] = None
                # self.fuzz.input['direction'] =
                self.fuzz.compute()
                # TODO: get the output from the fuzzy system
                movex = self.fuzz.output['move_x'] * 10
                movey = self.fuzz.output['move_y'] * 10
                print(position)
                self.on_AI_input(movex, 'x')
                self.on_AI_input(movey, 'y')
                self.on_render()

        if (keys[K_ESCAPE]):
            self._running = False

        if (keys[K_l]):
            scores = self.perception()
            print(scores)

    # FONCTION À Ajuster selon votre format d'instruction
    def on_AI_input(self, instruction):
        if instruction == 'RIGHT':
            self.move_player_right()

        if instruction == 'LEFT':
            self.move_player_left()

        if instruction == 'UP':
            self.move_player_up()

        if instruction == 'DOWN':
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

    def perception(self):
        perception_list = self.maze.make_perception_list(self.player, self._display_surf)
        position = self.player.get_position()
        up_perception = self.directional_perception(perception_list, position, "up")
        down_perception = self.directional_perception(perception_list, position, "down")
        left_perception = self.directional_perception(perception_list, position, "left")
        right_perception = self.directional_perception(perception_list, position, "right")
        return [up_perception, down_perception, left_perception, right_perception]

    def directional_perception(self, perception_list, position, direction):
        score = 1000

        if direction == "up":

            for wall in perception_list[0]:
                if wall[0] < position[0] + 20 and wall[1] < position[1] and wall[0] + 50 > position[0]:
                    if wall[0] > position[0]:
                        score = score - (20 - (wall[0] - position[0])) * (50 + (wall[1] + 50 - position[1])) / 2
                    elif position[0] <= wall[0] + 30:
                        score = score - 20 * (50 + (wall[1] + 50 - position[1])) / 2
                    elif position[0] < wall[0] + 50:
                        score = score - (wall[0] + 50 - position[0]) * (50 + (wall[1] + 50 - position[1])) / 2
            for obstacle in perception_list[1]:
                if obstacle[0] + 10 > position[0] > obstacle[0] - 20 and obstacle[1] < position[1]:
                    if obstacle[0] < position[0]:
                        score = score - 1.5 * (obstacle[0] + 10 - position[0]) * (50 + (obstacle[1] + 10 - position[1]))
                    elif obstacle[0] > position[0] > obstacle[0] - 10:
                        score = score - 15 * (50 + (obstacle[1] + 10 - position[1]))
                    else:
                        score = score - 1.5 * (position[0] + 20 - obstacle[0]) * (50 + (obstacle[1] + 10 - position[1]))
                elif obstacle[1] < position[1] + 5:
                    score -= 100
                elif obstacle[1] > position[1] + 5:
                    score += 100

            for item in perception_list[2]:
                if item[0] + 10 > position[0] > item[0] - 20 and item[1] < position[1]:
                    if item[0] < position[0]:
                        score = score + 2 * (item[0] + 10 - position[0]) * (50 - (item[1] + 10 - position[1]))
                    elif item[0] > position[0] > item[0] - 10:
                        score = score + 20 * (50 - (item[1] + 10 - position[1]))
                    else:
                        score = score + 2 * (position[0] + 20 - item[0]) * (50 - (item[1] + 10 - position[1]))
                if item[1] < position[1] + 5:
                    score += 100
                if item[1] > position[1] +5:
                    score -= 100

        elif direction == "down":

            for wall in perception_list[0]:
                if wall[0] < position[0] + 20 and wall[1] > position[1] and wall[0] + 50 > position[0]:
                    if wall[0] > position[0]:
                        score = score - (20 - (wall[0] - position[0])) * (50 + (position[1] + 20 - wall[1])) / 2
                    elif position[0] <= wall[0] + 30:
                        score = score - 20 * (50 + (position[1] + 20 - wall[1])) / 2
                    elif position[0] < wall[0] + 50:
                        score = score - (wall[0] + 50 - position[0]) * (50 + (position[1] + 20 - wall[1])) / 2
            for obstacle in perception_list[1]:
                if obstacle[0] + 10 > position[0] > obstacle[0] - 20 and obstacle[1] > position[1]:
                    if obstacle[0] < position[0]:
                        score = score - 1.5 * (obstacle[0] + 10 - position[0]) * (50 + (position[1] + 20 - obstacle[1]))
                    elif obstacle[0] > position[0] > obstacle[0] - 10:
                        score = score - 15 * (50 + (position[1] + 20 - obstacle[1]))
                    else:
                        score = score - 1.5 * (position[0] + 20 - obstacle[0]) * (50 + (position[1] + 20 - obstacle[1]))
                elif obstacle[1] > position[1] + 5:
                    score -= 100
                elif obstacle[1] < position[1] + 5:
                    score += 100

            for item in perception_list[2]:
                if item[0] + 10 > position[0] > item[0] - 20 and item[1] > position[1]:
                    if item[0] < position[0]:
                        score = score + 2 * (item[0] + 10 - position[0]) * (50 - (position[1] + 20 - item[1]))
                    elif item[0] > position[0] > item[0] - 10:
                        score = score + 20 * (50 - (position[1] + 20 - item[1]))
                    else:
                        score = score + 2 * (position[0] + 20 - item[0]) * (50 - (position[1] + 20 - item[1]))
                if item[1] > position[1] + 5:
                    score += 100
                if item[1] < position[1] + 5:
                    score -= 100

        elif direction == "left":

            for wall in perception_list[0]:
                if wall[1] < position[1] + 20 and wall[0] < position[0] and wall[1] + 50 > position[1]:
                    if wall[1] > position[1]:
                        score = score - (20 - (wall[1] - position[1])) * (50 + (wall[0] + 50 - position[0])) / 2
                    elif position[1] <= wall[1] + 30:
                        score = score - 20 * (50 + (wall[0] + 50 - position[0])) / 2
                    elif position[1] < wall[1] + 50:
                        score = score - (wall[1] + 50 - position[1]) * (50 + (wall[0] + 50 - position[0])) / 2
            for obstacle in perception_list[1]:
                if obstacle[1] + 10 > position[1] > obstacle[1] - 20 and position[0] > obstacle[0]:
                    if obstacle[1] < position[1]:
                        score = score - 1.5 * (obstacle[1] + 10 - position[1]) * (50 + (obstacle[0] - position[0] + 10))
                    elif obstacle[1] > position[1] > obstacle[1] - 10:
                        score = score - 15 * (50 + (obstacle[0] - position[0] + 10))
                    else:
                        score = score - 1.5 * (position[1] + 20 - obstacle[1]) * (50 + (obstacle[0] - position[0] + 10))
                elif obstacle[0] < position[0] + 5:
                    score -= 100
                elif obstacle[0] > position[0] + 5:
                    score += 100

            for item in perception_list[2]:
                if item[1] + 10 > position[1] > item[1] - 20 and position[0] > item[0]:
                    if item[1] < position[1]:
                        score = score + 2 * (item[1] + 10 - position[1]) * (50 - (item[0] - position[0] + 10))
                    elif item[1] > position[1] > item[1] - 10:
                        score = score + 20 * (50 - (item[0] - position[0] + 10))
                    else:
                        score = score + 2 *(position[1] + 20 - item[1]) * (50 - (item[0] - position[0] + 10))
                elif item[0] < position[0] + 5:
                    score += 100
                elif item[0] > position[0] + 5:
                    score -= 100

        elif direction == "right":

            for wall in perception_list[0]:
                if wall[1] < position[1] + 20 and wall[0] > position[0] and wall[1] + 50 > position[1]:
                    if wall[1] > position[1]:
                        score = score - (20 - (wall[1] - position[1])) * (50 + (position[0] + 20 - wall[0])) / 2
                    elif position[1] <= wall[1] + 30:
                        score = score - 20 * (50 + (position[0] + 20 - wall[0])) / 2
                    elif position[1] < wall[1] + 50:
                        score = score - (wall[1] + 50 - position[1]) * (50 + (position[0] + 20 - wall[0])) / 2
            for obstacle in perception_list[1]:
                if obstacle[1] + 10 > position[1] > obstacle[1] - 20 and position[0] < obstacle[0]:
                    if obstacle[1] < position[1]:
                        score = score - 1.5 * (obstacle[1] + 10 - position[1]) * (50 + (position[0] + 20 - obstacle[0]))
                    elif obstacle[1] > position[1] > obstacle[1] - 10:
                        score = score - 15 * (50 + (position[0] - obstacle[0] + 10))
                    else:
                        score = score - 1.5 * (position[1] + 20 - obstacle[1]) * (50 + (position[0] + 20 - obstacle[0]))
                elif obstacle[1] > position[1] + 5:
                    score -= 100
                elif obstacle[1] < position[1] + 5:
                    score += 100

            for item in perception_list[2]:
                if item[1] + 10 > position[1] > item[1] - 20 and position[0] < item[0]:
                    if item[1] < position[1]:
                        score = score + 2 * (item[1] + 10 - position[1]) * (50 - (position[0] + 20 - item[0]))
                    elif item[1] > position[1] > item[1] - 10:
                        score = score + 20 * (50 - (position[0] + 20 - item[0]))
                    else:
                        score = score + 2 * (position[1] + 20 - item[1]) * (50 - (position[0] + 20 - item[0]))
                elif item[0] > position[0] + 5:
                    score += 100
                elif item[0] < position[0] + 5:
                    score -= 100

        if score < 0:
            score = 0
        return int(score/20)
