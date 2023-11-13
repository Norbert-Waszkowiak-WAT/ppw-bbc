import sys
import pygame as pg
import time
import random
from numbers import *


class BossGame:
    def __init__(self, main):
        self.main = main
        self.window_width = WIN_WIDTH
        self.window_height = WIN_HEIGHT
        self.player = Player1(725, 300, 25, 50)
        self.game_state = "small_game"
        pg.init()
        pg.display.set_caption('BOSS')
        self.window = pg.display.set_mode((self.window_width, self.window_height), pg.RESIZABLE)
        self.fps = pg.time.Clock()

    def update(self):
        self.window.fill((100, 100, 100))
        self.player.update_player()
        pg.draw.rect(self.window, (255, 0, 0),
                     (self.player.x, self.player.y, self.player.size[0], self.player.size[1]))
        pg.display.update()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                self.player.size[0] += 1
            if event.type == pg.QUIT:
                quit()

    def run(self):
        while self.game_state == "small_game":
            self.handle_events()
            self.update()
            self.fps.tick(60)


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

    def update_player(self):
        self.movement()
        self.update_pos()


"""class Boss1:
    def __init__(self):
        pass"""
