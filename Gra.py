import math
import pygame as pg
import random
import random
import tkinter as tk
from tkinter import messagebox
import os

WHITE = (255, 255, 255)
BLUE = (0, 0, 225)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW= pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

VEL = 5 # velocity

RIVER_HEIGHT = 20
RIVER_WIDTH = 100
RIVER = pg.Rect(300, 300, RIVER_WIDTH, RIVER_HEIGHT)

BOSS_WIDTH = 80
BOSS_HEIGHT = 150
BOSS = pg.image.load(os.path.join('pliki', 'boss.png'))
BOSS = pg.transform.scale(BOSS, (BOSS_WIDTH, BOSS_HEIGHT))

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 150
PLAYER = pg.image.load(os.path.join('pliki', 'player.png'))
PLAYER = pg.transform.scale(PLAYER, (PLAYER_WIDTH, PLAYER_HEIGHT))

PLAYER_POSITION = pg.Rect(500, 50, PLAYER_WIDTH, PLAYER_HEIGHT)
BOSS_POSITION = pg.Rect(500, 50, BOSS_WIDTH, BOSS_HEIGHT)
def player_handle_movement(keys_pressed, PLAYER_POSITION):
    move_left = keys_pressed[pg.K_a] and PLAYER_POSITION.x - VEL > 0
    move_right = keys_pressed[pg.K_d] and PLAYER_POSITION.x + PLAYER_WIDTH + VEL < WINDOW_WIDTH
    move_down = keys_pressed[pg.K_s] and PLAYER_POSITION.y + PLAYER_HEIGHT + VEL < WINDOW_HEIGHT
    move_up = keys_pressed[pg.K_w] and PLAYER_POSITION.y - VEL > 0
    if_not_river_left = PLAYER_POSITION.x - VEL != RIVER.x + RIVER_WIDTH or (PLAYER_POSITION.y + PLAYER_HEIGHT < RIVER.y or PLAYER_POSITION.y > RIVER.y + RIVER_HEIGHT)
    if_not_river_right = PLAYER_POSITION.x + PLAYER_WIDTH + VEL != RIVER.x or (PLAYER_POSITION.y + PLAYER_HEIGHT < RIVER.y or PLAYER_POSITION.y > RIVER.y + RIVER_HEIGHT)
    if_not_river_bottom = PLAYER_POSITION.y + PLAYER_HEIGHT + VEL != RIVER.y or (PLAYER_POSITION.x + PLAYER_WIDTH < RIVER.x or PLAYER_POSITION.x > RIVER.x + RIVER_WIDTH)
    if_not_river_top = PLAYER_POSITION.y - VEL != RIVER.y + RIVER_HEIGHT or (PLAYER_POSITION.x + PLAYER_WIDTH < RIVER.x or PLAYER_POSITION.x > RIVER.x + RIVER_WIDTH)


    if move_left and if_not_river_left:
        PLAYER_POSITION.x -= VEL
    if move_right and if_not_river_right:
        PLAYER_POSITION.x += VEL
    if move_down and if_not_river_bottom:
        PLAYER_POSITION.y += VEL
    if move_up and if_not_river_top:
        PLAYER_POSITION.y -= VEL




def draw_window():
    WINDOW.fill(WHITE)
    pg.draw.rect(WINDOW, BLUE, RIVER)
    WINDOW.blit(BOSS, (BOSS_POSITION.x, BOSS_POSITION.y))
    WINDOW.blit(PLAYER, (PLAYER_POSITION.x, PLAYER_POSITION.y))
    pg.display.update()


class Player(object):
    def __init__(self, color, pos):
        pass


def main():


    game = True

    clock = pg.time.Clock()
    while game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game = False
        keys_pressed = pg.key.get_pressed()
        player_handle_movement(keys_pressed, PLAYER_POSITION)



        clock.tick(60) #ilość klatek na sekunde

        draw_window()
main()