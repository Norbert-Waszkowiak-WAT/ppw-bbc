import math
import pygame as pg
import random
import random
import tkinter as tk
from tkinter import messagebox


def draw_grid(w, rows, surface):
    size_between = w // rows
    x = 0
    y = 0
    for i in range(rows):
        x += size_between
        y += size_between
        pg.draw.line(surface, (225, 225, 225), (x, 0), (x, w))
        pg.draw.line(surface, (225, 225, 225), (0, y), (w, y))


def show_screen(surface):
    draw_grid(size, rows, surface)
    pg.display.update()


class Player(object):
    def __init__(self, color, pos):
        pass


def main():
    global size, rows
    size = 700 #size of screen
    rows = 20

    window = pg.display.set_mode((size, size))

    p = Player((0, 0, 0), (10, 10))

    game = True

    clock = pg.time.Clock()
    while game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game = False

        pg.time.delay(50) #opóźnienie w miliseundach

        clock.tick(10) #ilość klatek na sekunde

        show_screen(window)
main()