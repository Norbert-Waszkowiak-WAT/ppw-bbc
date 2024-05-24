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
        self.player = Player1((WIN_WIDTH - 16) / 2, 300, 32, 64)
        self.boss = Boss1(128, 128)
        self.game_state = "small_game"
        pg.init()
        self.window = pg.display.set_mode((self.window_width, self.window_height), pg.RESIZABLE)
        self.fps = pg.time.Clock()
        self.cooldown = 0
        self.all_entity = [Sprites('boss', self.boss.x, self.boss.y, 128, 128, 'img/Boss.png', 2, 2),
                           Sprites('player', 725, 300, 32, 64, 'img/Boss_character.png', 4, 8),
                           Sprites('background', 0, 0, 1536, 780, 'img/Boss_Background.png')]

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
        pg.mixer.stop()
        game_over_font = pg.font.Font(None, 36)
        game_over_text = game_over_font.render("Victory", True, (0, 255, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
        self.window.fill((0, 0, 0))
        self.window.blit(game_over_text, game_over_rect)
        pg.display.flip()
        pg.time.wait(1000)
        self.game_state = "main_game"
        self.main.end_boss("small_game")
        # self.main.playing = False

    def draw(self):
        def render_text(window, text, font_size, color, pos):
            font = pg.font.Font(None, font_size)
            text_surface = font.render(text, True, color)
            window.blit(text_surface, pos)

        self.window.blit(self.all_entity[2].get_sheet(0, 0), (self.all_entity[2].x, self.all_entity[2].y))

        # Draw health bar
        health_rect = pg.draw.rect(self.window, (255, 0, 0),
                                   (WIN_WIDTH / 2 - 250, 0, self.boss.health / 2, 20))
        render_text(self.window, "Boss Health", 36, (255, 255, 255), (health_rect.x, health_rect.y))

        # Draw player health circle
        health_circle_pos = (10, 10)
        pg.draw.circle(self.window, (255, 0, 0), health_circle_pos, 35)
        render_text(self.window, str(self.player.health), 36, (255, 255, 255),
                    (health_circle_pos[0] - 10, health_circle_pos[1] - 5))

        # Draw player energy circle
        energy_circle_pos = (WIN_WIDTH - 10, 10)
        pg.draw.circle(self.window, (255, 255, 0), energy_circle_pos, 35)
        render_text(self.window, str(int(self.player.energy)), 36, (0, 0, 0),
                    (energy_circle_pos[0] - 30, energy_circle_pos[1] - 5))

        for sprite in self.all_entity:
            if sprite.name in ['attack', 'particle']:
                s = pg.transform.rotate(sprite.get_sheet(random.randint(0, sprite.img_x - 1),
                                                         random.randint(0, sprite.img_y - 1)), random.randint(0, 360))
                self.window.blit(s, (sprite.x, sprite.y))
            elif sprite.name == 'skull':
                s = pg.transform.rotate(sprite.get_sheet(sprite.rand,
                                                         random.randint(0, sprite.img_y - 1)), sprite.animate)
                self.window.blit(s, (sprite.x, sprite.y))
                sprite.animate += 15
            elif sprite.name == 'skeleton':
                self.window.blit(sprite.get_sheet(int(sprite.animate), sprite.rand), (sprite.x, sprite.y))
                sprite.animate = (sprite.animate + 0.1) % sprite.img_x
                if sprite.health is not None:
                    pg.draw.rect(self.window, (255, 0, 0), (sprite.x, sprite.y - 10, sprite.health * 2.5, 7.5))
            elif sprite.name == 'boss':
                frame = 0 if self.boss.x_distance >= 0 else 1
                self.window.blit(sprite.get_sheet(int(sprite.animate), frame), (sprite.x, sprite.y))
                sprite.animate = (sprite.animate + 0.1) % sprite.img_x
            elif sprite.name == 'player':
                sprite.x, sprite.y = self.player.x, self.player.y
                if self.player.blink <= 0:
                    keys = pg.key.get_pressed()
                    mouse = pg.mouse.get_pressed()
                    if mouse[0]:
                        frame = 4 if keys[pg.K_d] else 3 if keys[pg.K_a] else 5
                    else:
                        frame = 1 if keys[pg.K_d] else 0 if keys[pg.K_a] else 2
                    self.window.blit(sprite.get_sheet(int(sprite.animate), frame), (sprite.x, sprite.y))
                    sprite.animate = (sprite.animate + 0.1) % sprite.img_x
                else:
                    pg.draw.rect(self.window, (75, 75, 75),
                                 (self.player.x, self.player.y, self.player.size[0], self.player.size[1]))

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
        for sprite in self.all_entity:
            if sprite.name == "attack":
                if pg.Rect(sprite.rect).colliderect(self.boss.boss_rect):
                    self.boss.health -= 1
                    for i in range(4):
                        self.all_entity.append(Sprites('particle', sprite.x,
                                                       sprite.y, 8, 8, 'img/fireball.png', 10, 2))
                    self.all_entity.remove(sprite)
                elif not sprite.attack1():
                    self.all_entity.remove(sprite)
                for sprite2 in self.all_entity:
                    if pg.Rect(sprite.rect).colliderect(sprite2) and sprite2.name == "skeleton":
                        if sprite2.health is not None:
                            sprite2.health -= 2
                        for i in range(4):
                            self.all_entity.append(Sprites('particle', sprite.x,
                                                           sprite.y, 8, 8, 'img/fireball.png', 10, 2))
                        if sprite in self.all_entity:
                            self.all_entity.remove(sprite)
            elif sprite.name == "particle" and not sprite.particle():
                self.all_entity.remove(sprite)
            elif sprite.name == "skull" and not sprite.skull():
                self.all_entity.remove(sprite)
                for i in range(5):
                    self.all_entity.append(Sprites('particle', sprite.x,
                                                   sprite.y - 5, 8, 8, 'img/skulls.png', 16, 4))
            elif sprite.name == "skeleton":
                if not sprite.skeleton():
                    self.all_entity.remove(sprite)
                    for i in range(15):
                        self.all_entity.append(Sprites('particle', sprite.x,
                                                       sprite.y - 5, 8, 8, 'img/skeleton.png', 16, 4))
                elif sprite.x > self.player.x:
                    sprite.rand = 0
                else:
                    sprite.rand = 1

        self.all_entity[1].x = self.player.x
        self.all_entity[1].y = self.player.y
        self.all_entity[0].x = self.boss.x
        self.all_entity[0].y = self.boss.y

        if self.player.attack():
            self.all_entity.append(Sprites('attack', self.player.x, self.player.y + 20,
                                           16, 16, 'img/fireball.png', 5, 1))
        if self.boss.attack_id == 1 and 300 > self.boss.attack_faze > 1:
            if random.randint(0, 3) == 0:
                self.all_entity.append(Sprites('skull', random.randint(BORDER, WIN_WIDTH - BORDER), -32,
                                               32, 32, 'img/skulls.png', 1, 1, random.randint(0, 3)))
        elif self.boss.attack_id == 2 and self.boss.attack_faze == 30:
            self.all_entity.append(Sprites('skeleton', WIN_WIDTH - BORDER - 96, WIN_HEIGHT - BORDER - 96,
                                           64, 96, 'img/skeleton.png', 28, 2, 0))
            self.all_entity.append(Sprites('skeleton', BORDER + 32, WIN_HEIGHT - BORDER - 96,
                                           64, 96, 'img/skeleton.png', 28, 2, 0))
            self.all_entity.append(Sprites('skeleton', WIN_WIDTH // 2, WIN_HEIGHT - BORDER - 96,
                                           64, 96, 'img/skeleton.png', 28, 2, 0))

    def colision(self):
        if self.cooldown <= 0 and self.player.blink < 1:
            if self.boss.boss_rect.colliderect(self.player.player_rect):
                self.cooldown = 60
                self.player.health -= 1
                pg.mixer.Sound('sounds/metal_pipe.mp3').play()
                for i in range(30):
                    self.all_entity.append(Sprites('particle', self.player.x, self.player.y + random.randint(-25, 25),
                                                   8, 8, 'img/gradient.png', 4, 4))
            for sprite in self.all_entity:
                if sprite.coli_rect.colliderect(self.player.player_rect):
                    if sprite.name == "skull":
                        self.cooldown = 60
                        self.player.health -= 1
                        pg.mixer.Sound('sounds/metal_pipe.mp3').play()
                        for i in range(30):
                            self.all_entity.append(
                                Sprites('particle', self.player.x, self.player.y + random.randint(-25, 25),
                                        8, 8, 'img/gradient.png', 4, 4))
                    if sprite.name == "skeleton":
                        self.cooldown = 50
                        self.player.health -= 1
                        pg.mixer.Sound('sounds/metal_pipe.mp3').play()
                        for i in range(30):
                            self.all_entity.append(
                                Sprites('particle', self.player.x, self.player.y + 20 + random.randint(-25, 25),
                                        8, 8, 'img/gradient.png', 4, 4))

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
        self.health = 10
        self.blink = 0
        self.cooldown = 0
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

        if keys[pg.K_LSHIFT] and self.energy >= 1:
            if self.blink == 0 and self.energy >= 15:
                self.blink = 2
                self.energy -= 15
            elif self.blink > 0:
                self.blink = 2
                self.energy -= 1
            else:
                self.blink = 0
        else:
            self.blink = 0

    def attack(self):
        mouse = pg.mouse.get_pressed()
        if mouse[0] and self.cooldown == 0:
            # pg.mixer.Sound('sounds/shot' + str(random.randint(1, 1)) + '.mp3').play()
            self.cooldown = 6
            return True

    def resources(self):
        if self.energy < 100:
            self.energy += 0.25
        if self.cooldown > 0:
            self.cooldown -= 1

    def player_update(self):
        self.resources()
        self.update_pos()
        self.movement()


class Sprites:
    def __init__(self, name, x, y, width, height, img, img_x=1, img_y=1, rand=None):
        self.name = name
        self.x = x
        self.y = y
        self.size = [width, height]
        self.rect = (self.x, self.y, self.size[0], self.size[1])
        self.coli_rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])
        self.target = self.direction()
        self.sheet = pg.image.load(img)
        if img_x == img_y == 1 and rand is None:
            self.sheet = pg.transform.scale(self.sheet, (self.size[0], self.size[1]))
        self.img_x = img_x
        self.img_y = img_y
        self.animate = 0
        self.vel_x = None
        self.vel_y = None
        self.rand = rand
        self.health = None

    def get_sheet(self, x, y):
        sprite = pg.Surface([self.size[0], self.size[1]])
        sprite.blit(self.sheet, (0, 0), (x * self.size[0], y * self.size[1], self.size[0], self.size[1]))
        sprite.set_colorkey(BLACK)
        return sprite

    def direction(self):
        d = pg.mouse.get_pos()
        direct = (d[0] - self.x - 8, d[1] - self.y - 8)
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

    def particle(self):
        if self.vel_x == self.vel_y is None:
            self.vel_y = random.randint(1, 7) / -2
            self.vel_x = random.randint(-75, 75) / 5
        if WIN_WIDTH - BORDER > self.x > BORDER and BORDER < self.y < WIN_HEIGHT - BORDER:
            self.x += self.vel_x
            self.y += self.vel_y
            self.vel_x -= self.vel_x / 4
            if self.vel_y < 20:
                self.vel_y += self.vel_y / 4 + 1
            return True
        else:
            return False

    def skull(self):
        if self.vel_y is None:
            self.vel_y = 3
            return True
        elif self.y < WIN_HEIGHT - BORDER - self.size[1]:
            self.y += self.vel_y
            self.coli_rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])
            if self.vel_y < 20:
                self.vel_y += self.vel_y / 20
            return True
        else:
            return False

    def skeleton(self):
        if self.vel_x is None:
            self.vel_x = 0
            self.health = 30
        if self.health > 0:
            self.rect = (self.x, self.y, self.size[0], self.size[1])
            if 7 > self.animate > 6 or 21 > self.animate >= 20:
                if self.rand == 0:
                    self.vel_x -= 0.45
                else:
                    self.vel_x += 0.45
            elif 8 > self.animate > 7 or 22 > self.animate > 21:
                if self.rand == 0:
                    self.vel_x += 0.45
                else:
                    self.vel_x -= 0.45
            elif self.animate > 22 or 20 > self.animate > 8 or 6 > self.animate:
                self.vel_x = 0
            self.x += self.vel_x
            return True
        else:
            return False


class Boss1:
    def __init__(self, width, height):
        self.x = (WIN_WIDTH - width / 2) / 2
        self.y = WIN_HEIGHT / 3 - height
        self.health = 1000
        self.random_x = self.x
        self.random_y = self.y
        self.x_distance = 0
        self.y_distance = 0
        self.size = [width, height]
        self.boss_rect = pg.Rect(self.x + 16, self.y + 16, self.size[0] - 32, self.size[1] - 32)
        self.attack_id = None
        self.attack_faze = None
        self.wait = 5
        self.vel = 12

    def boss_update(self):
        if self.x + 2 > self.random_x > self.x - 2 and self.y + 2 > self.random_y > self.y - 2:
            if self.attack_id is not None:
                self.attacking()
            else:
                self.random_x = random.randint(BORDER, WIN_WIDTH - self.size[0] - BORDER)
                self.random_y = random.randint(BORDER, WIN_HEIGHT - self.size[1] - BORDER - 75)
                while abs(self.random_x - self.x) > 400 or abs(self.random_y - self.y) > 400:
                    self.random_x = random.randint(BORDER, WIN_WIDTH - self.size[0] - BORDER)
                    self.random_y = random.randint(BORDER, WIN_HEIGHT - self.size[1] - BORDER - 75)
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
                if self.wait < 1:
                    self.attack_id = random.randint(0, 2)
                    self.attack_faze = 0
                    self.wait = random.randint(4, 8)
                else:
                    self.wait -= 1
        else:
            self.go_to_pos()
        self.boss_rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])

    def go_to_pos(self):
        self.x += self.x_distance / (self.vel * 2)
        self.y += self.y_distance / (self.vel * 2)

    def attacking(self):
        if self.attack_id == 0:  # New Attack
            if self.attack_faze == 0 or self.attack_faze == 60:
                self.vel = 10
                self.random_x = BORDER
                self.random_y = WIN_HEIGHT - self.size[1] - BORDER
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 20:
                self.vel = 10
                self.random_x = WIN_WIDTH - self.size[0] - BORDER
                self.random_y = WIN_HEIGHT - self.size[1] - BORDER
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 65:
                self.vel = 12
                self.attack_id = None
            if self.attack_faze == 0:
                self.vel = 24
            self.attack_faze += 1
        elif self.attack_id == 1:  # New Attack
            if self.attack_faze == 0:
                self.vel = 18
                self.random_x = (WIN_WIDTH - self.size[0] / 2) / 2
                self.random_y = BORDER + self.size[1] / 2
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 360:
                self.vel = 12
                self.attack_id = None
            self.attack_faze += 1
        elif self.attack_id == 2:  # New Attack
            if self.attack_faze == 0:
                self.vel = 18
                self.random_x = (WIN_WIDTH - self.size[0] / 2) / 2
                self.random_y = BORDER + self.size[1] / 2
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 360:
                self.vel = 12
                self.attack_id = None
            self.attack_faze += 1
