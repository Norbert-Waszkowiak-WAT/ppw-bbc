import pygame as pg
import time
import random
from numbers import *

class SnakeGame:

    def __init__(self, main):
        self.main = main
        self.pg = pg
        self.pixel = 25
        self.snake_speed = 250 // self.pixel
        self.window_width = WIN_WIDTH
        self.window_height = WIN_HEIGHT
        self.knockdown = 0

        self.pg.init()
        self.pg.display.set_caption('Snake')
        self.window = self.pg.display.set_mode((self.window_width, self.window_height), pg.RESIZABLE)
        self.fps = self.pg.time.Clock()

        self.bot_position = [50 * self.pixel, 350]
        self.snake_position = [4 * self.pixel, 350]

        self.bot_body = [[50 * self.pixel, 350],
                        [51 * self.pixel, 350],
                        [52 * self.pixel, 350],
                        [53 * self.pixel, 350]]
        self.snake_body = [[4 * self.pixel, 350],
                          [3 * self.pixel, 350],
                          [2 * self.pixel, 350],
                          [1 * self.pixel, 350]]

        self.fruit_position = [random.randrange(0, (self.window_width // self.pixel)) * self.pixel,
                              random.randrange(0, (self.window_height // self.pixel)) * self.pixel]
        self.fruit_spawn = True

        self.bot_direction = 'L'
        self.bot_change_to = self.bot_direction
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0

        self.game_state = "snake_game"

    def count_around_me(self, x, y, d):
        wall = ''
        if (self.snake_body.count([x, y - self.pixel]) == 1 or self.bot_body.count([x, y - self.pixel]) == 1 or y - self.pixel < 0) and d != 'D':
            wall += 'U'
        if (self.snake_body.count([x, y + self.pixel]) == 1 or self.bot_body.count([x, y + self.pixel]) == 1 or y + self.pixel == self.window_height) and d != 'U':
            wall += 'D'
        if (self.snake_body.count([x - self.pixel, y]) == 1 or self.bot_body.count([x - self.pixel, y]) == 1 or x - self.pixel < 0) and d != 'R':
            wall += 'L'
        if (self.snake_body.count([x + self.pixel, y]) == 1 or self.bot_body.count([x + self.pixel, y]) == 1 or x + self.pixel == self.window_width) and d != 'L':
            wall += 'R'
        return wall

    def show_score(self, color, font, size):
        score_font = self.pg.font.SysFont(font, size)
        score_surface = score_font.render('Punkty: ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        self.window.blit(score_surface, score_rect)

    def game_over(self):
        my_font = self.pg.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render('Zdobyłeś ' + str(self.score) + ' punktów!!!', True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_width / 2, self.window_height / 4)

        self.window.blit(game_over_surface, game_over_rect)
        self.pg.display.flip()

        time.sleep(2)
        self.game_state = "main_game"

    def victory(self):
        my_font = self.pg.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render('Wygrałeś!!!', True, (255, 255, 0))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_width / 2, self.window_height / 4)

        self.window.blit(game_over_surface, game_over_rect)
        self.pg.display.flip()

        time.sleep(5)
        self.game_state = "main_game"
        self.main.kill_boss(0)

    def handle_events(self):
        for event in self.pg.event.get():
            if event.type == self.pg.KEYDOWN:
                if event.key == self.pg.K_w:
                    self.change_to = 'UP'
                if event.key == self.pg.K_s:
                    self.change_to = 'DOWN'
                if event.key == self.pg.K_a:
                    self.change_to = 'LEFT'
                if event.key == self.pg.K_d:
                    self.change_to = 'RIGHT'
                if event.key == self.pg.K_x:
                    self.victory()
            if event.type == self.pg.QUIT:
                quit()

    def run(self):
        while self.game_state == "snake_game":
            self.handle_events()

            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

            if self.direction == 'UP':
                self.snake_position[1] -= self.pixel
            if self.direction == 'DOWN':
                self.snake_position[1] += self.pixel
            if self.direction == 'LEFT':
                self.snake_position[0] -= self.pixel
            if self.direction == 'RIGHT':
                self.snake_position[0] += self.pixel

            self.snake_body.insert(0, list(self.snake_position))
            if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
                self.score += 1
                self.fruit_spawn = False
            else:
                self.snake_body.pop()

            if not self.fruit_spawn:
                self.fruit_position = [random.randrange(1, (self.window_width // self.pixel)) * self.pixel,
                                      random.randrange(1, (self.window_height // self.pixel)) * self.pixel]

            self.fruit_spawn = True
            self.window.fill((0, 0, 0))

            self.pg.draw.rect(self.window, (0, 255, 0), self.pg.Rect(self.snake_body[0][0], self.snake_body[0][1], self.pixel, self.pixel))
            color = 255
            for pos in self.snake_body[1:]:
                color -= 200 // len(self.snake_body)
                self.pg.draw.rect(self.window, (0, color, 0), self.pg.Rect(pos[0], pos[1], self.pixel, self.pixel))

            if self.bot_direction == 'x':
                self.pg.draw.rect(self.window, (255, 0, 255), self.pg.Rect(self.bot_body[0][0], self.bot_body[0][1], self.pixel, self.pixel))
                color = 255
                for pos in self.bot_body[1:]:
                    color -= 200 // len(self.bot_body)
                    self.pg.draw.rect(self.window, (255, 0, color), self.pg.Rect(pos[0], pos[1], self.pixel, self.pixel))
            else:
                self.pg.draw.rect(self.window, (255, 0, 0), self.pg.Rect(self.bot_body[0][0], self.bot_body[0][1], self.pixel, self.pixel))
                color = 255
                for pos in self.bot_body[1:]:
                    color -= 200 // len(self.bot_body)
                    self.pg.draw.rect(self.window, (color, 0, 0), self.pg.Rect(pos[0], pos[1], self.pixel, self.pixel))

            self.pg.draw.rect(self.window, (255, 255, 0), self.pg.Rect(self.fruit_position[0], self.fruit_position[1], self.pixel, self.pixel))

            if self.snake_position[0] < 0 or self.snake_position[0] > self.window_width - self.pixel:
                self.game_over()

            if self.snake_position[1] < 0 or self.snake_position[1] > self.window_height - self.pixel:
                self.game_over()

            for block in self.snake_body[1:]:
                if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                    self.game_over()

            ###################################################################

            if self.count_around_me(self.bot_position[0], self.bot_position[1], self.bot_direction) != '':
                warning = self.count_around_me(self.bot_position[0], self.bot_position[1], self.bot_direction)
                if len(warning) == 3:
                    if self.bot_direction != 'x':
                        self.knockdown += 1
                    self.bot_change_to = 'x'
                    self.bot_direction = 'x'
                elif warning.count('U') != 1 and self.bot_direction != 'D':
                    if warning.count('D') != 1 and self.bot_direction != 'U' and self.fruit_position[1] > self.bot_position[1]:
                        self.bot_change_to = 'D'
                    else:
                        self.bot_change_to = 'U'
                elif warning.count('D') != 1 and self.bot_direction != 'U':
                    self.bot_change_to = 'D'
                elif warning.count('R') != 1 and self.bot_direction != 'L':
                    self.bot_change_to = 'R'
                elif warning.count('L') != 1 and self.bot_direction != 'R':
                    self.bot_change_to = 'L'
            elif self.fruit_position[0] > self.bot_position[0]:
                if self.bot_direction != 'L':
                    self.bot_change_to = 'R'
                else:
                    if self.fruit_position[1] > self.bot_position[1]:
                        self.bot_change_to = 'D'
                    else:
                        self.bot_change_to = 'U'
            elif self.fruit_position[0] < self.bot_position[0]:
                if self.bot_direction != 'R':
                    self.bot_change_to = 'L'
                else:
                    if self.fruit_position[1] > self.bot_position[1]:
                        self.bot_change_to = 'D'
                    else:
                        self.bot_change_to = 'U'
            elif self.fruit_position[1] < self.bot_position[1]:
                if self.bot_direction != 'D':
                    self.bot_change_to = 'U'
                else:
                    if self.fruit_position[0] > self.bot_position[0]:
                        self.bot_change_to = 'R'
                    else:
                        self.bot_change_to = 'L'
            elif self.fruit_position[1] > self.bot_position[1]:
                if self.bot_direction != 'U':
                    self.bot_change_to = 'D'
                else:
                    if self.fruit_position[0] > self.bot_position[0]:
                        self.bot_change_to = 'R'
                    else:
                        self.bot_change_to = 'L'

            if self.bot_change_to == 'U' and self.bot_direction != 'D':
                self.bot_direction = 'U'
            if self.bot_change_to == 'D' and self.bot_direction != 'U':
                self.bot_direction = 'D'
            if self.bot_change_to == 'L' and self.bot_direction != 'R':
                self.bot_direction = 'L'
            if self.bot_change_to == 'R' and self.bot_direction != 'L':
                self.bot_direction = 'R'

            if self.bot_direction == 'U':
                self.bot_position[1] -= self.pixel
            if self.bot_direction == 'D':
                self.bot_position[1] += self.pixel
            if self.bot_direction == 'L':
                self.bot_position[0] -= self.pixel
            if self.bot_direction == 'R':
                self.bot_position[0] += self.pixel

            self.bot_body.insert(0, list(self.bot_position))
            if self.bot_position[0] == self.fruit_position[0] and self.bot_position[1] == self.fruit_position[1]:
                self.fruit_spawn = False
            else:
                self.bot_body.pop()

            for block in self.bot_body:
                if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                    self.game_over()

            self.show_score((255, 255, 255), 'times new roman', 30)
            self.pg.display.update()
            if self.knockdown > 2:
                self.victory()
            self.fps.tick(self.snake_speed)
