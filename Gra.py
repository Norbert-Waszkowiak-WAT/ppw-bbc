import math
import pygame as pg
import random
import random
import tkinter as tk
from tkinter import messagebox
import os

WHITE = (255, 255, 255)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

VEL = 5 # velocity
BOSS_WIDTH = 80
BOSS_HEIGHT = 150
BOSS = pg.image.load(os.path.join('pliki', 'boss.png'))
BOSS = pg.transform.scale(BOSS, (BOSS_WIDTH, BOSS_HEIGHT))

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 150
PLAYER = pg.image.load(os.path.join('pliki', 'player.png'))
PLAYER = pg.transform.scale(PLAYER, (PLAYER_WIDTH, PLAYER_HEIGHT))

def draw_window(PLAYER_POSITION, BOSS_POSITION):
    window.fill(WHITE)
    window.blit(BOSS, (BOSS_POSITION.x, BOSS_POSITION.y))
    window.blit(PLAYER, (PLAYER_POSITION.x, PLAYER_POSITION.y))
    pg.display.update()


class Player(object):
    def __init__(self, color, pos):
        pass


def main():
    PLAYER_POSITION = pg.Rect(500, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
    BOSS_POSITION = pg.Rect(500, 50, BOSS_WIDTH, BOSS_HEIGHT)






    game = True

    clock = pg.time.Clock()
    while game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game = False
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_a]:
            PLAYER_POSITION.x -= VEL
        if keys_pressed[pg.K_d]:
            PLAYER_POSITION.x += VEL
        if keys_pressed[pg.K_s]:
            PLAYER_POSITION.y += VEL
        if keys_pressed[pg.K_w]:
            PLAYER_POSITION.y -= VEL



        clock.tick(60) #ilość klatek na sekunde

        draw_window(PLAYER_POSITION, BOSS_POSITION)
main()