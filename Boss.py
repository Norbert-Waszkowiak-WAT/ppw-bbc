import sys
import pygame as pg
import time
from math import hypot, degrees, atan2, cos, sin
import random
from numbers import *


class BossGame:
    def __init__(self, main):
        self.main = main
        self.time = 0
        self.window_width = WIN_WIDTH
        self.window_height = WIN_HEIGHT
        self.player = Player1(725, 300, 24, 48)
        self.boss = Boss1(128, 128)
        self.game_state = "small_game"
        pg.init()
        self.window = pg.display.set_mode((self.window_width, self.window_height), pg.RESIZABLE)
        self.fps = pg.time.Clock()
        self.cooldown = 0
        self.all_sprites = [Sprites('damage', BORDER, BORDER, WIN_WIDTH - 2 * BORDER, WIN_HEIGHT - 2 * BORDER,
                                    '')]

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

    def victory(self):
        game_over_font = pg.font.Font(None, 36)
        game_over_text = game_over_font.render("Victory", True, (0, 255, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
        self.window.fill((0, 0, 0))
        self.window.blit(game_over_text, game_over_rect)
        pg.display.flip()
        pg.time.wait(1000)
        self.game_state = "main_game"

    def draw(self):
        self.window.fill((50, 50, 50))
        pg.draw.rect(self.window, (100, 100, 100), (BORDER, BORDER, WIN_WIDTH - BORDER * 2, WIN_HEIGHT - BORDER * 2))

        health_rect = pg.draw.rect(self.window, (255, 0, 0),
                                   (WIN_WIDTH / 2 - 250, WIN_HEIGHT - 20, self.boss.health / 2, 20))
        self.window.blit(pg.font.Font(None, 36).render("Boss Health", True, (255, 255, 255)), health_rect)
        health_cylc = pg.draw.circle(self.window, (255, 0, 0),
                                     (10, 10), 35)
        self.window.blit(pg.font.Font(None, 36).render(str(self.player.health), True, (255, 255, 255)), health_cylc)
        energy_cylc = pg.draw.circle(self.window, (255, 255, 0),
                                     (WIN_WIDTH - 10, 10), 35)
        self.window.blit(pg.font.Font(None, 36).render(str(int(self.player.energy)), True, (0, 0, 0)), energy_cylc)

        if self.time > 4:
            pg.draw.rect(self.window, (0, 100, 0),
                         (self.boss.x, self.boss.y, self.boss.size[0], self.boss.size[1]))
        else:
            pg.draw.rect(self.window, (100 - self.time * 25, 100, 100 - self.time * 25),
                         (self.boss.x, self.boss.y, self.boss.size[0], self.boss.size[1]))
        if self.player.blink <= 0:
            pg.draw.rect(self.window, (0, 0, 0),
                         (self.player.x, self.player.y, self.player.size[0], self.player.size[1]))
        else:
            pg.draw.rect(self.window, (75, 75, 75),
                         (self.player.x, self.player.y, self.player.size[0], self.player.size[1]))

        for sprite in self.all_sprites:
            if sprite.name != 'damage':
                pg.draw.rect(self.window, (255, 0, 255), sprite.rect)

    def update(self):
        if self.time > 4:
            self.boss.boss_update()
        self.player.player_update()
        self.functions()
        self.draw()
        self.colision()
        if self.player.health <= 0:
            self.game_over()
        if self.boss.health <= 0:
            self.victory()

        pg.display.update()
        self.time += 0.015625

    def functions(self):
        for sprite in self.all_sprites:
            if sprite.name == "attack":
                if pg.Rect(sprite.rect).colliderect(self.boss.boss_rect):
                    self.boss.health -= 1
                    self.all_sprites.remove(sprite)
                elif not sprite.attack1():
                    self.all_sprites.remove(sprite)

        if self.player.attack():
            self.all_sprites.append(Sprites('attack', self.player.x + self.player.size[0] / 2 - 5, self.player.y,
                                            10, 10, ''))

    def colision(self):
        if self.cooldown <= 0 and self.player.blink < 1:
            if self.boss.boss_rect.colliderect(self.player.player_rect):
                self.cooldown = 60
                self.player.health -= 1
        else:
            self.cooldown -= 1

    def handle_events(self):
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if keys[pg.K_x]:
                self.victory()
            if keys[pg.K_s]:
                self.boss.health -= 10

    def run(self):
        while self.game_state == "small_game":
            self.handle_events()
            self.update()
            self.fps.tick(64)


class Player1:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.size = [width, height]
        self.player_rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])
        self.x_vel = 0
        self.y_vel = 0
        self.energy = 100
        self.health = 2
        self.blink = 0

        """self.image = self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)"""

        self.air = False

    def update_pos(self):
        self.x += self.x_vel // 2
        self.y += self.y_vel // 4
        if self.blink > 0:
            self.blink -= 1
        self.player_rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])

    def movement(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.air and self.y > 350 - BORDER:
            self.y_vel -= (25 + self.y_vel / 5)
        elif self.y < WIN_HEIGHT - self.size[1] - BORDER:
            self.y_vel += 8
            self.air = False
        else:
            self.y_vel = 0
            self.y = WIN_HEIGHT - self.size[1] - BORDER
            self.air = True

        if keys[pg.K_a]:
            if self.x < BORDER:
                self.x = BORDER
                self.x_vel = 0
            else:
                if self.x_vel > 0:
                    self.x_vel -= (self.x_vel // 2) + 1
                elif self.x_vel > -40:
                    self.x_vel -= (abs(0.25 * self.x_vel)) // 1 + 1
        elif keys[pg.K_d]:
            if self.x > WIN_WIDTH - self.size[0] - BORDER:
                self.x = WIN_WIDTH - self.size[0] - BORDER
                self.x_vel = 0
            else:
                if self.x_vel < 0:
                    self.x_vel -= (self.x_vel // 2) - 1
                elif self.x_vel < 40:
                    self.x_vel += (0.25 * self.x_vel) // 1 + 1
        elif self.x_vel > 0:
            self.x_vel -= (self.x_vel // 2) + 1
            if self.x > WIN_WIDTH - self.size[0] - BORDER:
                self.x = WIN_WIDTH - self.size[0] - BORDER
                self.x_vel = 0
        elif self.x_vel < 0:
            if self.x < BORDER:
                self.x = BORDER
                self.x_vel = 0
            self.x_vel -= (self.x_vel // 2) - 1

        if keys[pg.K_LSHIFT] and self.energy >= 30 and self.blink <= 0:
            self.blink = 45
            self.energy -= 30

    def attack(self):
        mouse = pg.mouse.get_pressed()
        if mouse[0] and self.energy >= 1:
            self.energy -= 1
            return True

    def resources(self):
        if self.energy < 100:
            self.energy += 0.25

    def player_update(self):
        self.resources()
        self.update_pos()
        self.movement()


class Sprites:
    def __init__(self, name, x, y, width, height, img):
        self.name = name
        self.x = x
        self.y = y
        self.size = [width, height]
        self.rect = (self.x, self.y, self.size[0], self.size[1])
        self.target = self.direction()
        self.img = img

    def direction(self):
        d = pg.mouse.get_pos()
        direct = (d[0] - self.x, d[1] - self.y)
        lenght = hypot(*direct)
        if lenght == 0.0:
            direct = (0, -1)
        else:
            direct = (direct[0] / lenght, direct[1] / lenght)
        return direct

    def attack1(self):
        vel = 25
        if WIN_WIDTH - BORDER > self.x > BORDER and BORDER < self.y < WIN_HEIGHT - BORDER:
            self.x += vel * sin(self.target[0])
            self.y += vel * sin(self.target[1])
            self.rect = (self.x, self.y, self.size[0], self.size[1])
            return True
        else:
            return False


class Boss1:
    def __init__(self, width, height):
        self.x = WIN_WIDTH / 2 - (width / 2)
        self.y = WIN_HEIGHT / 3 - height
        self.health = 1000
        self.random_x = self.x
        self.random_y = self.y
        self.x_distance = 0
        self.y_distance = 0
        self.size = [width, height]
        self.boss_rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])

    def boss_update(self):
        if self.x + 2 > self.random_x > self.x - 2 and self.y + 2 > self.random_y > self.y - 2:
            self.random_x = random.randint(BORDER, WIN_WIDTH - self.size[0] - BORDER)
            self.random_y = random.randint(BORDER, WIN_HEIGHT - self.size[1] - BORDER - 75)
            while abs(self.random_x - self.x) > 400 or abs(self.random_y - self.y) > 400:
                self.random_x = random.randint(BORDER, WIN_WIDTH - self.size[0] - BORDER)
                self.random_y = random.randint(BORDER, WIN_HEIGHT - self.size[1] - BORDER - 75)
            self.x_distance = (self.random_x - self.x)
            self.y_distance = (self.random_y - self.y)
        else:
            self.random_pos()
        self.boss_rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])

    def random_pos(self):
        self.x += self.x_distance / 24
        self.y += self.y_distance / 24
