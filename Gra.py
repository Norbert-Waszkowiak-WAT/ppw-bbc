import math
from pygame.locals import *
import pygame as pg
import random
import tkinter as tk
from tkinter import messagebox
import os

kupa = 3

BLUE = [0, 0, 225]
GREY = [128, 128, 128]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

class Object:

    def __init__(self, x, y, width, height, parent_screen, collision):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.parent_screen = parent_screen
        self.colision = collision
        self.rect = pg.Rect(x, y, width, height)

    def draw_objects(self):

        if self.colision == True:
            pg.draw.rect(self.parent_screen, GREY, self.rect)
        elif self.colision == False:
            pg.draw.rect(self.parent_screen, GREEN, self.rect)

class Player:

    VEL = 1
    def __init__(self, parent_screen, parent_screen_width, parent_screen_height, objects):

        self.parent_screen = parent_screen
        self.parent_screen_width = parent_screen_width
        self.parent_screen_height = parent_screen_height
        self.objects = objects
        self.x = 500
        self.y = 100
        self.width = 80
        self.height = 150
        self.body = pg.image.load(os.path.join('pliki', 'player.png'))
        self.body = pg.transform.scale(self.body, (self.width, self.height))
        self.pos = pg.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys_pressed):

        move_left = keys_pressed[pg.K_a] and self.x - self.VEL > 0
        move_right = keys_pressed[pg.K_d] and self.x + self.width + self.VEL < self.parent_screen_width
        move_down = keys_pressed[pg.K_s] and self.y + self.height + self.VEL < self.parent_screen_height
        move_up = keys_pressed[pg.K_w] and self.y - self.VEL > 0

        if move_left:
            new_x = self.x - self.VEL
            if self.check_collision(new_x, self.y):
                self.x = new_x
        if move_right:
            new_x = self.x + self.VEL
            if self.check_collision(new_x, self.y):
                self.x = new_x
        if move_down:
            new_y = self.y + self.VEL
            if self.check_collision(self.x, new_y):
                self.y = new_y
        if move_up:
            new_y = self.y - self.VEL
            if self.check_collision(self.x, new_y):
                self.y = new_y

        self.draw()

    def check_collision(self, new_x, new_y):

        new_rect = pg.Rect(new_x, new_y, self.width, self.height)

        for obj in self.objects:

            if isinstance(obj, Object) and new_rect.colliderect(obj.rect) and obj.colision == True: #czy obiekt ma wszystkie parametry
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
        self.add_objects()

    def run(self):

        game = True
        clock = pg.time.Clock()
        frame = 0

        while game:

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    game = False

            keys_pressed = pg.key.get_pressed()

            if keys_pressed[pg.K_a] or keys_pressed[pg.K_d] or keys_pressed[pg.K_s] or keys_pressed[pg.K_w]:
                self.Player.move(keys_pressed)

            clock.tick(0)  # fps

            self.draw_objects()

    def draw_objects(self):

        self.window.fill((255, 255, 255))

        for obj in self.objects:

            if isinstance(obj, Object):
                obj.draw_objects()

        self.Player.draw()
        pg.display.update()

    def add_objects(self):

        for y in range(0, WINDOW_HEIGHT, 50): #rzeczy po których możesz chodzić

            for x in range(0, WINDOW_WIDTH, 50):

                obj = Object(x, y, 50, 50, self.window, False)
                self.objects.append(obj)

        for i in range(10): #przeszkody

            x = random.randint(0, WINDOW_WIDTH - 50)
            y = random.randint(0, WINDOW_HEIGHT - 50)

            if (x > 580 or x < 500) and (y < 100 or y > 250):
                obj = Object(x, y, 50, 50, self.window, True)
                self.objects.append(obj)

def main():

    game = Game()
    game.run()

main()