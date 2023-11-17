import sys
import pygame as pg
import time
from math import atan2, degrees, pi
import random
from numbers import *


class BossGame:
    def __init__(self, main):
        self.main = main
        self.time = 0
        self.window_width = WIN_WIDTH
        self.window_height = WIN_HEIGHT
        self.player = Player1(725, 300, 25, 50)
        self.boss = Boss1(128, 128)
        self.game_state = "small_game"
        pg.init()
        pg.display.set_caption('BOSS')
        self.window = pg.display.set_mode((self.window_width, self.window_height), pg.RESIZABLE)
        self.fps = pg.time.Clock()

    def update(self):
        self.window.fill((100, 100, 100))
        if self.time > 4:
            self.boss.boss_update()
            pg.draw.rect(self.window, (0, 100, 0),
                         (self.boss.x, self.boss.y, self.boss.size[0], self.boss.size[1]))
        else:
            pg.draw.rect(self.window, (100 - self.time * 25, 100, 100 - self.time * 25),
                         (self.boss.x, self.boss.y, self.boss.size[0], self.boss.size[1]))
        self.player.player_update()
        pg.draw.rect(self.window, (255, 0, 0),
                     (self.player.x, self.player.y, self.player.size[0], self.player.size[1]))
        pg.display.update()
        self.time += 0.015625

    def game_over(self):
        game_over_font = pg.font.Font(None, 36)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
        self.window.fill((0, 0, 0))
        self.window.blit(game_over_text, game_over_rect)
        pg.display.flip()
        pg.time.wait(1000)
        self.game_state = "main_game"

    def colision(self):
        if self.boss.x - self.player.size[0] <= self.player.x <= self.boss.x + self.boss.size[0]:
            if self.boss.y + self.boss.size[1] >= self.player.y >= self.boss.y - self.player.size[1]:
                self.game_over()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

    def run(self):
        while self.game_state == "small_game":
            self.handle_events()
            self.update()
            self.colision()
            self.fps.tick(64)


class Player1:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.size = [width, height]
        self.x_vel = 0
        self.y_vel = 0

        """self.image = self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y"""

        self.air = False

    def update_pos(self):
        self.x += self.x_vel // 2
        self.y += self.y_vel // 4

    def movement(self):
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()
        if mouse[0]:
            pass
        if keys[pg.K_w] and self.air and self.y > 350:
            self.y_vel -= (10 + self.y_vel / 20)
        elif self.y < WIN_HEIGHT - self.size[1]:
            self.y_vel += 8
            self.air = False
        else:
            self.y_vel = 0
            self.y = WIN_HEIGHT - self.size[1]
            self.air = True

        if keys[pg.K_a]:
            if self.x < 0:
                self.x = 0
                self.x_vel = 0
            else:
                if self.x_vel > 0:
                    self.x_vel -= (self.x_vel // 2) + 1
                elif self.x_vel > -40:
                    self.x_vel -= (abs(0.25 * self.x_vel)) // 1 + 1
        elif keys[pg.K_d]:
            if self.x > WIN_WIDTH - self.size[0]:
                self.x = WIN_WIDTH - self.size[0]
                self.x_vel = 0
            else:
                if self.x_vel < 0:
                    self.x_vel -= (self.x_vel // 2) - 1
                elif self.x_vel < 40:
                    self.x_vel += (0.25 * self.x_vel) // 1 + 1
        elif self.x_vel > 0:
            self.x_vel -= (self.x_vel // 2) + 1
        elif self.x_vel < 0:
            self.x_vel -= (self.x_vel // 2) - 1

    def player_update(self):
        self.movement()
        self.update_pos()


class Sprites:
    def __init__(self, x, y, width, height, player):
        self.x = x
        self.y = y
        self.size = [width, height]
        self.player = player

    def direction(self):
        d = pg.mouse.get_pos()
        dx = d[0] - self.x
        dy = d[1] - self.y
        rads = atan2(-dy, dx)
        rads %= 2 * pi
        return degrees(rads)

    def pos(self):
        self.x = self.player.x + 25
        self.y = self.player.y + 10


class Boss1:
    def __init__(self, width, height):
        self.x = WIN_WIDTH / 2 - (width / 2)
        self.y = WIN_HEIGHT / 3 - height
        self.random_x = self.x
        self.random_y = self.y
        self.x_distance = 0
        self.y_distance = 0
        self.size = [width, height]

    def boss_update(self):
        if self.x + 5 > self.random_x > self.x - 5 and self.y + 5 > self.random_y > self.y - 5:
            self.random_x = random.randint(0, WIN_WIDTH - self.size[0])
            self.random_y = random.randint(0, WIN_HEIGHT - self.size[1] - 75)
            while abs(self.random_x - self.x) > 400 or abs(self.random_y - self.y) > 400:
                self.random_x = random.randint(0, WIN_WIDTH - self.size[0])
                self.random_y = random.randint(0, WIN_HEIGHT - self.size[1] - 75)
            self.x_distance = (self.random_x - self.x)
            self.y_distance = (self.random_y - self.y)
        else:
            self.random_pos()

    def random_pos(self):
        self.x += self.x_distance / 24
        self.y += self.y_distance / 24
