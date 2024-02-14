import pygame as pg
import time
import random
from numbers import *


class SnakeGame:
    def __init__(self, main):
        self.main = main
        self.game_state = "snake_game"
        pg.init()
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.fps = pg.time.Clock()
        self.crash = None

        self.pixel = 25
        self.game_speed = 10
        self.knockdown = 0

        self.snake = Snake(self)
        self.bot = Bot(self)
        self.printer = Printer(self)

        self.fruit_position = [random.randrange(0, (WIN_WIDTH // self.pixel)) * self.pixel,
                               random.randrange(0, (WIN_HEIGHT // self.pixel)) * self.pixel]
        self.fruit_on_map = False

    def fruit(self):
        self.fruit_position = [random.randrange(0, (WIN_WIDTH // self.pixel)) * self.pixel,
                               random.randrange(0, (WIN_HEIGHT // self.pixel)) * self.pixel]
        self.fruit_on_map = True

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.snake.change_to = 'UP'
                elif event.key == pg.K_s:
                    self.snake.change_to = 'DOWN'
                elif event.key == pg.K_a:
                    self.snake.change_to = 'LEFT'
                elif event.key == pg.K_d:
                    self.snake.change_to = 'RIGHT'
                elif event.key == pg.K_x:
                    self.victory()
            elif event.type == pg.QUIT:
                quit()

    def game_over(self):
        pg.mixer.Sound('sounds/metal_pipe.mp3').play()
        my_font = pg.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render('Game over', True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (WIN_WIDTH / 2, WIN_HEIGHT / 4)

        self.screen.blit(game_over_surface, game_over_rect)
        pg.display.flip()

        time.sleep(2)
        self.game_state = "main_game"

    def victory(self):
        my_font = pg.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render('Wygrałeś!!!', True, (255, 255, 0))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (WIN_WIDTH / 2, WIN_HEIGHT / 4)

        self.screen.blit(game_over_surface, game_over_rect)
        pg.display.flip()

        time.sleep(5)
        self.game_state = "main_game"
        self.main.kill_boss(0)

    def run(self):
        while self.game_state == "snake_game":
            self.snake.move()
            if not self.fruit_on_map:
                self.fruit()
            self.handle_events()
            self.bot.brain()
            self.bot.move()
            self.printer.update_map()
            pg.display.update()
            if self.crash is not None:
                self.game_over()
            elif self.knockdown > 2:
                self.victory()
            self.fps.tick(self.game_speed)


class Snake:
    def __init__(self, game):
        self.game = game
        self.snake_position = [4 * self.game.pixel, 350]
        self.snake_body = [[4 * self.game.pixel, 350],
                           [3 * self.game.pixel, 350],
                           [2 * self.game.pixel, 350],
                           [self.game.pixel, 350]]
        self.change_to = 'RIGHT'
        self.direction = 'RIGHT'

    def move(self):
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        elif self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        elif self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        if self.direction == 'UP':
            self.snake_position[1] -= self.game.pixel
        elif self.direction == 'DOWN':
            self.snake_position[1] += self.game.pixel
        elif self.direction == 'LEFT':
            self.snake_position[0] -= self.game.pixel
        elif self.direction == 'RIGHT':
            self.snake_position[0] += self.game.pixel

        self.snake_body.insert(0, list(self.snake_position))
        if self.snake_position[0] == self.game.fruit_position[0] and self.snake_position[1] == self.game.fruit_position[
            1]:
            self.game.fruit_on_map = False
            pg.mixer.Sound('sounds/get_point.mp3').play()
        else:
            self.snake_body.pop()

        if self.snake_position[0] < 0 or self.snake_position[0] > WIN_WIDTH - self.game.pixel:
            self.game.crash = 1

        if self.snake_position[1] < 0 or self.snake_position[1] > WIN_HEIGHT - self.game.pixel:
            self.game.crash = 1

        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                self.game.crash = 1


class Bot(Snake):
    def __init__(self, game):
        super().__init__(game)
        self.bot_position = [50 * self.game.pixel, 350]
        self.bot_body = [[50 * self.game.pixel, 350],
                         [51 * self.game.pixel, 350],
                         [52 * self.game.pixel, 350],
                         [53 * self.game.pixel, 350]]
        self.bot_direction = 'LEFT'
        self.bot_change_to = 'LEFT'

    def count_around_me(self, x, y, d):
        wall = ''
        if (self.game.snake.snake_body.count([x, y - self.game.pixel]) == 1 or self.bot_body.count(
                [x, y - self.game.pixel]) == 1 or y - self.game.pixel < 0) and d != 'D':
            wall += 'U'
        if (self.game.snake.snake_body.count([x, y + self.game.pixel]) == 1 or self.bot_body.count(
                [x, y + self.game.pixel]) == 1 or y + self.game.pixel == WIN_HEIGHT) and d != 'U':
            wall += 'D'
        if (self.game.snake.snake_body.count([x - self.game.pixel, y]) == 1 or self.bot_body.count(
                [x - self.game.pixel, y]) == 1 or x - self.game.pixel < 0) and d != 'R':
            wall += 'L'
        if (self.game.snake.snake_body.count([x + self.game.pixel, y]) == 1 or self.bot_body.count(
                [x + self.game.pixel, y]) == 1 or x + self.game.pixel == WIN_WIDTH) and d != 'L':
            wall += 'R'
        return wall

    def brain(self):
        if self.count_around_me(self.bot_position[0], self.bot_position[1], self.bot_direction) != '':
            warning = self.count_around_me(self.bot_position[0], self.bot_position[1], self.bot_direction)
            if len(warning) == 3:
                if self.bot_direction != 'x':
                    self.game.knockdown += 1
                    pg.mixer.Sound('sounds/metal_pipe.mp3').play()
                self.bot_change_to = 'x'
                self.bot_direction = 'x'
            elif warning.count('U') != 1 and self.bot_direction != 'D':
                if warning.count('D') != 1 and self.bot_direction != 'U' and self.game.fruit_position[1] > \
                        self.bot_position[1]:
                    self.bot_change_to = 'D'
                else:
                    self.bot_change_to = 'U'
            elif warning.count('D') != 1 and self.bot_direction != 'U':
                self.bot_change_to = 'D'
            elif warning.count('R') != 1 and self.bot_direction != 'L':
                self.bot_change_to = 'R'
            elif warning.count('L') != 1 and self.bot_direction != 'R':
                self.bot_change_to = 'L'
        elif self.game.fruit_position[0] > self.bot_position[0]:
            if self.bot_direction != 'L':
                self.bot_change_to = 'R'
            else:
                if self.game.fruit_position[1] > self.bot_position[1]:
                    self.bot_change_to = 'D'
                else:
                    self.bot_change_to = 'U'
        elif self.game.fruit_position[0] < self.bot_position[0]:
            if self.bot_direction != 'R':
                self.bot_change_to = 'L'
            else:
                if self.game.fruit_position[1] > self.bot_position[1]:
                    self.bot_change_to = 'D'
                else:
                    self.bot_change_to = 'U'
        elif self.game.fruit_position[1] < self.bot_position[1]:
            if self.bot_direction != 'D':
                self.bot_change_to = 'U'
            else:
                if self.game.fruit_position[0] > self.bot_position[0]:
                    self.bot_change_to = 'R'
                else:
                    self.bot_change_to = 'L'
        elif self.game.fruit_position[1] > self.bot_position[1]:
            if self.bot_direction != 'U':
                self.bot_change_to = 'D'
            else:
                if self.game.fruit_position[0] > self.bot_position[0]:
                    self.bot_change_to = 'R'
                else:
                    self.bot_change_to = 'L'

    def move(self):
        if self.bot_change_to == 'U' and self.bot_direction != 'D':
            self.bot_direction = 'U'
        elif self.bot_change_to == 'D' and self.bot_direction != 'U':
            self.bot_direction = 'D'
        elif self.bot_change_to == 'L' and self.bot_direction != 'R':
            self.bot_direction = 'L'
        elif self.bot_change_to == 'R' and self.bot_direction != 'L':
            self.bot_direction = 'R'

        if self.bot_direction == 'U':
            self.bot_position[1] -= self.game.pixel
        elif self.bot_direction == 'D':
            self.bot_position[1] += self.game.pixel
        elif self.bot_direction == 'L':
            self.bot_position[0] -= self.game.pixel
        elif self.bot_direction == 'R':
            self.bot_position[0] += self.game.pixel

        self.bot_body.insert(0, list(self.bot_position))
        if self.bot_position[0] == self.game.fruit_position[0] and self.bot_position[1] == self.game.fruit_position[1]:
            self.game.fruit_on_map = False
            pg.mixer.Sound('sounds/get_point.mp3').play()
        else:
            self.bot_body.pop()

        for block in self.bot_body:
            if self.game.snake.snake_position[0] == block[0] and self.game.snake.snake_position[1] == block[1]:
                self.game.crash = 1


class Printer:
    def __init__(self, game):
        self.game = game

    def update_map(self):
        self.game.screen.fill((0, 0, 0))

        pg.draw.rect(self.game.screen, (255, 255, 0),
                     pg.Rect(self.game.fruit_position[0], self.game.fruit_position[1], self.game.pixel,
                             self.game.pixel))

        pg.draw.rect(self.game.screen, (0, 255, 0),
                     pg.Rect(self.game.snake.snake_body[0][0], self.game.snake.snake_body[0][1],
                             self.game.pixel, self.game.pixel))
        color = 255
        for pos in self.game.snake.snake_body[1:]:
            color -= 200 // len(self.game.snake.snake_body)
            pg.draw.rect(self.game.screen, (0, color, 0), pg.Rect(pos[0], pos[1], self.game.pixel, self.game.pixel))

        if self.game.bot.bot_direction == 'x':
            pg.draw.rect(self.game.screen, (255, 0, 255),
                         pg.Rect(self.game.bot.bot_body[0][0], self.game.bot.bot_body[0][1],
                                 self.game.pixel, self.game.pixel))
            color = 255
            for pos in self.game.bot.bot_body[1:]:
                color -= 200 // len(self.game.bot.bot_body)
                pg.draw.rect(self.game.screen, (255, 0, color),
                             pg.Rect(pos[0], pos[1], self.game.pixel, self.game.pixel))
        else:
            pg.draw.rect(self.game.screen, (255, 0, 0),
                         pg.Rect(self.game.bot.bot_body[0][0], self.game.bot.bot_body[0][1],
                                 self.game.pixel, self.game.pixel))
            color = 255
            for pos in self.game.bot.bot_body[1:]:
                color -= 200 // len(self.game.bot.bot_body)
                pg.draw.rect(self.game.screen, (color, 0, 0), pg.Rect(pos[0], pos[1], self.game.pixel, self.game.pixel))


