import math
from pygame.locals import *
import pygame as pg
import random
import random
import tkinter as tk
from tkinter import messagebox
import os


BLUE = (0, 0, 225)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

class Object:
    def __init__(self, x, y, width, height, parent_screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.parent_screen = parent_screen

class Player:
    VEL = 5

    def __init__(self, parent_screen, parent_screen_width, parent_screen_height, objects):
        self.parent_screen = parent_screen
        self.parent_screen_width = parent_screen_width
        self.parent_screen_height = parent_screen_height
        self.objects = objects
        self.x = 500
        self.y = 50
        self.width = 80
        self.height = 150
        self.body = pg.image.load(os.path.join('pliki', 'player.png'))
        self.body = pg.transform.scale(self.body, (self.width, self.height))
        self.pos = pg.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys_pressed):
        old_x = self.x
        old_y = self.y

        move_left = keys_pressed[pg.K_a] and self.x - self.VEL > 0
        move_right = keys_pressed[pg.K_d] and self.x + self.width + self.VEL < self.parent_screen_width
        move_down = keys_pressed[pg.K_s] and self.y + self.height + self.VEL < self.parent_screen_height
        move_up = keys_pressed[pg.K_w] and self.y - self.VEL > 0

        if move_left and self.check_collision(old_x - self.VEL, old_y):
            self.x -= self.VEL
        if move_right and self.check_collision(old_x + self.VEL, old_y):
            self.x += self.VEL
        if move_down and self.check_collision(old_x, old_y + self.VEL):
            self.y += self.VEL
        if move_up and self.check_collision(old_x, old_y - self.VEL):
            self.y -= self.VEL

        self.draw()

    def check_collision(self, new_x, new_y):
        new_pos = pg.Rect(new_x, new_y, self.width, self.height)
        for obj in self.objects:
            if isinstance(obj, pg.Rect) and new_pos.colliderect(obj):
                return False
        return True

    def draw(self):
        self.parent_screen.blit(self.body, (self.x, self.y))
class Game:
    def __init__(self):
        pg.init()
        self.objects = []
        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.Player = Player(self.window, WINDOW_WIDTH, WINDOW_HEIGHT, self.objects)
        self.Player.draw()
        self.add_objects()

    def run(self):
        game = True
        clock = pg.time.Clock()
        while game:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game = False
            keys_pressed = pg.key.get_pressed()
            if keys_pressed[pg.K_a] or keys_pressed[pg.K_d] or keys_pressed[pg.K_s] or keys_pressed[pg.K_w]:
                self.Player.move(keys_pressed)
            clock.tick(60)  # fps
            self.draw_objects()

    def draw_objects(self):
        self.window.fill((255, 255, 255))
        for obj in self.objects:
            if isinstance(obj, pg.Rect):
                pg.draw.rect(self.window, GREY, obj)
        self.Player.draw()
        pg.display.update()

    def add_objects(self):
        obj1 = pg.Rect(200, 200, 50, 50)
        obj2 = pg.Rect(600, 400, 50, 50)
        self.objects.append(obj1)
        self.objects.append(obj2)
        self.draw_objects()

def main():
    game = Game()
    game.run()

main()