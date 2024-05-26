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
        self.player = Player1((WIN_WIDTH - 16) / 2, 350, 32, 64)
        self.boss = Boss1(128, 128, self.player)
        self.game_state = "small_game"
        pg.init()
        pg.mixer.music.load("sounds/boss_game/boss_music.mp3")
        pg.mixer.music.play(100)
        self.window = pg.display.set_mode((self.window_width, self.window_height), pg.RESIZABLE)
        self.fps = pg.time.Clock()
        self.cooldown = 0
        self.dead = 0
        self.all_entity = [Sprites('boss', self.boss.x, self.boss.y, 128, 128, 'img/boss_game/Boss.png', 2, 4),
                           Sprites('player', 725, 300, 40, 80, 'img/boss_game/Boss_character.png', 4, 12),
                           Sprites('background', 0, 0, 1540, 795, 'img/boss_game/Boss_Background.png', 2, 2)]
        for i in range(self.player.health):
            self.all_entity.append(Sprites('heart', BORDER + 4 + i * 35, 5, 45, 45, 'img/boss_game/heart.png'))
        self.all_entity.append(Sprites('bar', WIN_WIDTH / 2 - 275, 0, 550, 45, 'img/boss_game/bossbar1.png'))
        self.all_entity.append(Sprites('bossbar', WIN_WIDTH / 2 - 275, 0, 550, 45, 'img/boss_game/bossbar2.png'))
        self.all_entity.append(Sprites('bar', WIN_WIDTH - 155 - BORDER, -7.5, 150, 55, 'img/boss_game/energybar1.png'))
        self.all_entity.append(
            Sprites('energybar', WIN_WIDTH - 155 - BORDER, -7.5, 150, 55, 'img/boss_game/energybar2.png'))

    def game_over(self):
        pg.mixer.music.stop()
        self.del_entities()
        self.player.x = (WIN_WIDTH - self.player.size[0]) / 2
        self.player.y = WIN_HEIGHT - self.player.size[1] - BORDER - 10
        self.boss.attack_id = None
        self.boss.vel = 32
        self.boss.random_x = (WIN_WIDTH - self.boss.size[0]) / 2
        self.boss.random_y = 2 * BORDER + self.boss.size[1]
        self.boss.x_distance = (self.boss.random_x - self.boss.x)
        self.boss.y_distance = (self.boss.random_y - self.boss.y)
        self.del_entities()
        self.time = 0
        while self.time < 5.5:
            self.handle_events()
            if self.time < 1:
                self.boss.go_to_pos()
            elif self.time == 2:
                pg.mixer.Sound('sounds/boss_game/scream.mp3').play()
            elif self.time > 1.5:
                self.player.y -= 1.75
            self.functions()
            self.draw()
            pg.display.update()
            self.time += 0.015625
        self.del_entities()
        pg.mixer.Sound('sounds/boss_game/player_death.mp3').play()
        for i in range(50):
            self.all_entity.append(Sprites('particle', self.player.x + self.player.size[0] / 2,
                                           self.player.y + random.randint(-15, 15), 8, 8,
                                           'img/boss_game/particle/gradient.png', 4, 4))
        self.dead = 1
        while self.time < 7:
            self.handle_events()
            for entity in self.all_entity:
                if entity.name == "particle" and not entity.particle():
                    self.all_entity.remove(entity)
            self.functions()
            self.draw()
            pg.display.update()
            self.time += 0.015625

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
        pg.mixer.music.stop()
        self.del_entities()
        self.boss.attack_id = None
        self.boss.vel = 32
        self.boss.random_x = (WIN_WIDTH - self.boss.size[0]) / 2
        self.boss.random_y = 2 * BORDER + self.boss.size[1]
        self.boss.x_distance = (self.boss.random_x - self.boss.x)
        self.boss.y_distance = (self.boss.random_y - self.boss.y)
        self.del_entities()
        self.time = 0
        while self.boss.health > 0:
            self.player.player_update()
            if self.time < 1:
                self.boss.go_to_pos()
            elif self.time == 1:
                self.boss.x_distance = 0
                pg.mixer.Sound("sounds/boss_game/finish-him.mp3").play()
                self.boss.boss_rect = pg.Rect(self.boss.x, self.boss.y, self.boss.size[0], self.boss.size[1])
                self.boss.health = 50
            else:
                if self.time % 0.02 > 0.01:
                    self.boss.x += 1.1
                    self.boss.y += 0.4
                    self.boss.x_distance += random.randint(0, 1)
                else:
                    self.boss.x -= 1.1
                    self.boss.y -= 0.4
                    self.boss.x_distance -= random.randint(0, 1)
                if self.time % 6 == 0:
                    pg.mixer.Sound("sounds/boss_game/finish-him.mp3").play()
            self.handle_events()
            self.functions()
            self.draw()
            pg.display.update()
            self.time += 0.015625
        pg.mixer.Sound('sounds/boss_game/boss_death.mp3').play()
        for i in range(100):
            self.all_entity.append(Sprites('particle', self.boss.x + self.boss.size[0] / 2 + random.randint(-50, 50),
                                           self.boss.y + random.randint(-25, 25), 10, 10,
                                           'img/boss_game/boss.png', 20, 20))
            self.all_entity.append(Sprites('particle', self.boss.x + self.boss.size[0] / 2 + random.randint(-30, 30),
                                           self.boss.y + random.randint(-10, 10), 8, 8,
                                           'img/boss_game/particle/gradient.png', 4, 4))
        self.dead = 2
        self.time = 0
        while self.time < 5:
            self.player.player_update()
            self.handle_events()
            self.functions()
            self.draw()
            pg.display.update()
            self.time += 0.015625

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
        self.window.blit(self.all_entity[2].get_sheet(0, 0), (self.all_entity[2].x, self.all_entity[2].y))

        for entity in self.all_entity:
            if entity.name in ['attack', 'particle', 'ult']:
                s = pg.transform.rotate(entity.get_sheet(random.randint(0, entity.img_x - 1),
                                                         random.randint(0, entity.img_y - 1)), random.randint(0, 360))
                self.window.blit(s, (entity.x, entity.y))
            elif entity.name == 'skull':
                s = pg.transform.rotate(entity.get_sheet(entity.rand,
                                                         random.randint(0, entity.img_y - 1)), entity.animate)
                self.window.blit(s, (entity.x, entity.y))
                entity.animate += 15
            elif entity.name == 'skeleton':
                self.window.blit(entity.get_sheet(int(entity.animate), entity.rand), (entity.x, entity.y))
                entity.animate = (entity.animate + 0.1) % entity.img_x
                if entity.health is not None:
                    pg.draw.rect(self.window, (255, 0, 0), (entity.x, entity.y - 10, entity.health * 2.5, 7.5))
            elif entity.name == 'boss' and self.dead != 2:
                frame = 0 if self.boss.x_distance >= 0 else 1
                self.window.blit(entity.get_sheet(int(entity.animate), frame), (entity.x, entity.y))
                entity.animate = (entity.animate + 0.1) % entity.img_x
            elif entity.name == 'player' and self.dead != 1:
                entity.x, entity.y = self.player.x, self.player.y
                if self.player.blink <= 0:
                    keys = pg.key.get_pressed()
                    mouse = pg.mouse.get_pressed()
                    if mouse[0]:
                        frame = 4 if keys[pg.K_d] else 3 if keys[pg.K_a] else 5
                    else:
                        frame = 1 if keys[pg.K_d] else 0 if keys[pg.K_a] else 2
                    self.window.blit(entity.get_sheet(int(entity.animate), frame), (entity.x, entity.y))
                    entity.animate = (entity.animate + 0.1) % entity.img_x
                else:
                    keys = pg.key.get_pressed()
                    mouse = pg.mouse.get_pressed()
                    if mouse[0]:
                        frame = 10 if keys[pg.K_d] else 9 if keys[pg.K_a] else 11
                    else:
                        frame = 7 if keys[pg.K_d] else 6 if keys[pg.K_a] else 8
                    self.window.blit(entity.get_sheet(int(entity.animate), frame), (entity.x, entity.y))
                    entity.animate = (entity.animate + 0.1) % entity.img_x
            elif entity.name == 'fireskull':
                self.window.blit(entity.get_sheet(entity.rand, 0), (entity.x, entity.y))
            elif entity.name in ['heart', 'bossbar', 'energybar', 'bar']:
                self.window.blit(entity.get_sheet(0, 0), (entity.x, entity.y))

    def update(self):
        if self.time > 2:
            self.boss.boss_update()
        self.player.player_update()
        self.functions()
        self.draw()
        self.colision()
        if self.player.health <= 0:
            self.game_over()
        if self.boss.health <= 100:
            self.victory()

        pg.display.update()
        self.time += 0.015625

    def functions(self):
        hp_counter = 0
        for entity in self.all_entity:
            if entity.name == "heart":
                hp_counter += 1
                if hp_counter > self.player.health:
                    self.all_entity.remove(entity)
            elif entity.name == "bossbar":
                entity.health_changer(self.boss.health)
            elif entity.name == "energybar":
                entity.energy_changer(self.player.energy)
            elif entity.name == "fireskull":
                if not entity.fireskull():
                    for i in range(30):
                        if entity.x < WIN_WIDTH / 2:
                            self.all_entity.append(Sprites('particle', entity.x + BORDER,
                                                           entity.y + BORDER + 10,
                                                           8, 8, 'img/boss_game/ult.png', 4, 4))
                        else:
                            self.all_entity.append(Sprites('particle', entity.x - BORDER,
                                                           entity.y + BORDER + 10,
                                                           8, 8, 'img/boss_game/ult.png', 4, 4))
                    self.all_entity.remove(entity)
            elif entity.name == "attack":
                if pg.Rect(entity.rect).colliderect(self.boss.boss_rect):
                    self.boss.health -= 1
                    for i in range(4):
                        self.all_entity.append(Sprites('particle', entity.x,
                                                       entity.y, 8, 8, 'img/boss_game/fireball.png', 10, 2))
                    self.all_entity.remove(entity)
                elif not entity.attack1():
                    self.all_entity.remove(entity)
                for entity2 in self.all_entity:
                    if pg.Rect(entity.rect).colliderect(entity2) and entity2.name == "skeleton":
                        if entity2.health is not None:
                            entity2.health -= 2
                        for i in range(4):
                            self.all_entity.append(Sprites('particle', entity.x,
                                                           entity.y, 8, 8, 'img/boss_game/fireball.png', 10, 2))
                        if entity in self.all_entity:
                            self.all_entity.remove(entity)
            elif entity.name == "ult":
                if pg.Rect(entity.rect).colliderect(self.boss.boss_rect):
                    self.boss.health -= 85
                    for i in range(40):
                        self.all_entity.append(Sprites('particle', entity.x + random.randint(-20, 20),
                                                       entity.y + random.randint(-40, 0),
                                                       8, 8, 'img/boss_game/ult.png', 4, 4))
                    self.all_entity.remove(entity)
                    pg.mixer.Sound("sounds/boss_game/ult2.mp3").play()
                elif not entity.attack2():
                    self.all_entity.remove(entity)
                    for i in range(40):
                        if entity.x < WIN_WIDTH / 2:
                            self.all_entity.append(Sprites('particle', entity.x + BORDER,
                                                           entity.y + BORDER + 10,
                                                           8, 8, 'img/boss_game/ult.png', 4, 4))
                        else:
                            self.all_entity.append(Sprites('particle', entity.x - BORDER,
                                                           entity.y + BORDER + 10,
                                                           8, 8, 'img/boss_game/ult.png', 4, 4))
                    pg.mixer.Sound("sounds/boss_game/ult2.mp3").play()
                for entity2 in self.all_entity:
                    if pg.Rect(entity.rect).colliderect(entity2) and entity2.name == "skeleton":
                        if entity2.health is not None:
                            entity2.health -= 85
                        for i in range(40):
                            self.all_entity.append(Sprites('particle', entity.x + random.randint(-20, 20),
                                                           entity.y + random.randint(-20, 20),
                                                           8, 8, 'img/boss_game/ult.png', 4, 4))
                        pg.mixer.Sound("sounds/boss_game/ult2.mp3").play()
                        if entity in self.all_entity:
                            self.all_entity.remove(entity)
            elif entity.name == "particle" and not entity.particle():
                self.all_entity.remove(entity)
            elif entity.name == "skull" and not entity.skull():
                self.all_entity.remove(entity)
                for i in range(5):
                    self.all_entity.append(Sprites('particle', entity.x,
                                                   entity.y - 5, 8, 8, 'img/boss_game/skulls.png', 16, 4))
            elif entity.name == "skeleton":
                if not entity.skeleton():
                    self.all_entity.remove(entity)
                    pg.mixer.Sound('sounds/boss_game/skeleton_die.mp3').play()
                    for i in range(20):
                        self.all_entity.append(Sprites('particle', entity.x,
                                                       entity.y - 5, 16, 16, 'img/boss_game/particle/skeleton.png', 2,
                                                       2))
                elif entity.x > self.player.x:
                    entity.rand = 0
                else:
                    entity.rand = 1

        if hp_counter < self.player.health:
            self.all_entity.append(Sprites('heart', BORDER + 4 + hp_counter * 35, 5, 45, 45, 'img/boss_game/heart.png'))

        self.all_entity[1].x = self.player.x
        self.all_entity[1].y = self.player.y
        self.all_entity[0].x = self.boss.x
        self.all_entity[0].y = self.boss.y

        if self.player.attack():
            self.all_entity.append(Sprites('attack', self.player.x + self.player.size[0] / 2 - 4, self.player.y + 20,
                                           16, 16, 'img/boss_game/fireball.png', 5, 1))
        if self.player.ult():
            self.all_entity.append(Sprites('ult', self.player.x + self.player.size[0] / 2 - 4, self.player.y + 25,
                                           32, 32, 'img/boss_game/ult.png'))
        if self.boss.attack_id == 1 and 300 > self.boss.attack_faze > 1:
            if random.randint(0, 3) == 0:
                self.all_entity.append(Sprites('skull', random.randint(BORDER, WIN_WIDTH - BORDER), -32,
                                               32, 32, 'img/boss_game/skulls.png', 1, 1, random.randint(0, 3)))
        elif self.boss.attack_id == 2 and self.boss.attack_faze == 30:
            self.all_entity.append(Sprites('skeleton', WIN_WIDTH - BORDER - 96, 0,
                                           64, 96, 'img/boss_game/skeleton.png', 28, 2, 0))
            self.all_entity.append(Sprites('skeleton', BORDER + 32, 0,
                                           64, 96, 'img/boss_game/skeleton.png', 28, 2, 0))
            self.all_entity.append(Sprites('skeleton', WIN_WIDTH // 2, 0,
                                           64, 96, 'img/boss_game/skeleton.png', 28, 2, 0))
        elif self.boss.attack_id == 3 and self.boss.attack_faze == 27:
            pg.mixer.Sound("sounds/boss_game/crash.mp3").play()
            if self.boss.x >= WIN_WIDTH / 2:
                self.all_entity.append(Sprites('fireskull', WIN_WIDTH,
                                               WIN_HEIGHT - BORDER - 170,
                                               196, 196, 'img/boss_game/fireattack.png', 2, 1, 0))
                for i in range(25):
                    self.all_entity.append(Sprites('particle', self.boss.x + self.boss.size[0] / 2 + 30,
                                                   self.boss.y + 20 + random.randint(-25, 25),
                                                   16, 16, 'img/boss_game/particle/wall.png', 2, 2))
            else:
                self.all_entity.append(Sprites('fireskull', -196,
                                               WIN_HEIGHT - BORDER - 170,
                                               196, 196, 'img/boss_game/fireattack.png', 2, 1, 1))
                for i in range(25):
                    self.all_entity.append(Sprites('particle', self.boss.x + self.boss.size[0] / 2 - 30,
                                                   self.boss.y + 20 + random.randint(-25, 25),
                                                   16, 16, 'img/boss_game/particle/wall.png', 2, 2))
        elif self.boss.attack_id == 4 and self.boss.attack_faze == 42:
            pg.mixer.Sound("sounds/boss_game/crash.mp3").play()
            for i in range(25):
                self.all_entity.append(Sprites('particle', self.boss.x + self.boss.size[0] / 2
                                               + random.choice([-1, 1]) * 20, self.boss.y + random.randint(30, 45),
                                               16, 16, 'img/boss_game/particle/floor.png', 2, 2))

    def colision(self):
        if self.cooldown <= 0 and self.player.blink < 1:
            if self.boss.boss_rect.colliderect(self.player.player_rect):
                self.cooldown = 60
                self.player.health -= 1
                pg.mixer.Sound('sounds/boss_game/hurt.mp3').play()
                for i in range(30):
                    self.all_entity.append(Sprites('particle', self.player.x, self.player.y + random.randint(-25, 25),
                                                   8, 8, 'img/boss_game/particle/gradient.png', 4, 4))
            for entity in self.all_entity:
                if entity.coli_rect.colliderect(self.player.player_rect):
                    if entity.name in ["skull", "skeleton", "fireskull"]:
                        self.cooldown = 60
                        self.player.health -= 1
                        pg.mixer.Sound('sounds/boss_game/hurt.mp3').play()
                        for i in range(30):
                            self.all_entity.append(
                                Sprites('particle', self.player.x, self.player.y + random.randint(-25, 25),
                                        8, 8, 'img/boss_game/particle/gradient.png', 4, 4))
        else:
            self.cooldown -= 1

        if self.cooldown <= 0 < self.player.blink:
            if self.boss.boss_rect.colliderect(self.player.player_rect):
                pg.mixer.Sound('sounds/boss_game/shield.mp3').play()
                self.cooldown = 20
                for i in range(15):
                    self.all_entity.append(
                        Sprites('particle', self.player.x + self.player.size[0] / 2,
                                self.player.y + 20 + random.randint(-25, 25),
                                8, 8, 'img/boss_game/particle/shield.png', 4, 4))
            for entity in self.all_entity:
                if entity.coli_rect.colliderect(self.player.player_rect):
                    if entity.name in ["skull", "skeleton", "fireskull"]:
                        pg.mixer.Sound('sounds/boss_game/shield.mp3').play()
                        self.cooldown = 20
                        for i in range(15):
                            self.all_entity.append(
                                Sprites('particle', self.player.x + self.player.size[0] / 2,
                                        self.player.y + 20 + random.randint(-25, 25),
                                        8, 8, 'img/boss_game/particle/shield.png', 4, 4))

    def handle_events(self):
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if keys[pg.K_s]:
                self.boss.health -= 10
            if keys[pg.K_z]:
                self.player.health = 5

    def run(self):
        while self.game_state == "small_game":
            self.handle_events()
            self.update()
            self.fps.tick(64)

    def del_entities(self):
        special_entities = ['boss', 'player', 'background', 'bar', 'bossbar', 'energybar', 'heart']
        for entity in self.all_entity:
            if entity.name not in special_entities:
                self.all_entity.remove(entity)


class Player1:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.size = [width, height]
        self.player_rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])
        self.x_vel = 0
        self.y_vel = 0
        self.energy = 100
        self.health = 5
        self.blink = 0
        self.cooldown = 0
        self.air = False
        self.sound_cooldown = 0

    def update_pos(self):
        self.x += self.x_vel // 2
        self.y += self.y_vel // 4
        if self.blink > 0:
            self.blink -= 1
        self.player_rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])

    def movement(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.air and self.y > 450 - BORDER:
            self.y_vel -= (25 + self.y_vel / 5)
        elif self.y < WIN_HEIGHT - self.size[1] - BORDER - 10:
            self.y_vel += 8
            self.air = False
        else:
            self.y_vel = 0
            self.y = WIN_HEIGHT - self.size[1] - BORDER - 10
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
            if self.blink == 0 and self.energy >= 20:
                self.blink = 2
                self.energy -= 20
            elif self.blink > 0:
                self.blink = 2
                self.energy -= 1
            else:
                if self.sound_cooldown == 0:
                    pg.mixer.Sound("sounds/boss_game/wrong.mp3").play()
                    self.sound_cooldown = 30
                self.blink = 0
        else:
            self.blink = 0

    def attack(self):
        mouse = pg.mouse.get_pressed()
        if mouse[0] and self.cooldown == 0:
            self.cooldown = 6
            return True

    def ult(self):
        mouse = pg.mouse.get_pressed()
        if mouse[2] and self.energy >= 85:
            self.cooldown = 6
            self.sound_cooldown = 5
            self.energy -= 85
            pg.mixer.Sound("sounds/boss_game/ult1.mp3").play()
            return True
        elif mouse[2] and self.sound_cooldown == 0:
            pg.mixer.Sound("sounds/boss_game/wrong.mp3").play()
            self.sound_cooldown = 30

    def resources(self):
        if self.energy < 100:
            self.energy += 0.25
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.sound_cooldown > 0:
            self.sound_cooldown -= 1

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
        entity = pg.Surface([self.size[0], self.size[1]])
        entity.blit(self.sheet, (0, 0), (x * self.size[0], y * self.size[1], self.size[0], self.size[1]))
        entity.set_colorkey(BLACK)
        return entity

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

    def attack2(self):
        vel = 50
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
            self.vel_y = 0
            self.health = 30
        if self.health > 0:
            self.coli_rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])
            if self.y < WIN_HEIGHT - BORDER - 96:
                self.vel_y += self.vel_y / 12 + 0.08
                self.y += self.vel_y
                self.rect = (self.x, self.y, self.size[0], self.size[1])
            else:
                self.vel_y = 0
                self.y = WIN_HEIGHT - BORDER - 96
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

    def fireskull(self):
        if self.rand == 1:
            if self.x < WIN_WIDTH:
                self.x += 65
                self.coli_rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])
                return True
            return False
        else:
            if self.x > 0:
                self.x -= 65
                self.coli_rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])
                return True
            return False

    def health_changer(self, boss_health):
        if boss_health > 0:
            self.size[0] = boss_health / 2

    def energy_changer(self, energy):
        self.size[0] = energy * 1.5


class Boss1:
    def __init__(self, width, height, player):
        self.x = (WIN_WIDTH - width) / 2
        self.y = WIN_HEIGHT / 2.5 - height
        self.health = 1000
        self.player = player
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
        self.tmp = 0

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
                    self.attack_id = random.randint(0, 4)
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
        if self.attack_id == 0:
            if self.attack_faze == 0 or self.attack_faze == 50:  # LG 1 4
                self.vel = 6
                self.random_x = BORDER
                self.random_y = BORDER
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 20 or self.attack_faze == 80 or self.attack_faze == 125:  # LD 2 6 11
                self.vel = 6
                self.random_x = BORDER
                self.random_y = WIN_HEIGHT - self.size[1] - BORDER
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 35 or self.attack_faze == 90 or self.attack_faze == 135:  # PD 3 7 12
                self.vel = 6
                self.random_x = WIN_WIDTH - self.size[0] - BORDER
                self.random_y = WIN_HEIGHT - self.size[1] - BORDER
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 65 or self.attack_faze == 105:  # PG 5 8
                self.vel = 6
                self.random_x = WIN_WIDTH - self.size[0] - BORDER
                self.random_y = BORDER
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 115:  # GS 9
                self.vel = 6
                self.random_x = (WIN_WIDTH - self.size[0]) / 2
                self.random_y = BORDER
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 120:  # DS 10
                self.vel = 6
                self.random_x = (WIN_WIDTH - self.size[0]) / 2
                self.random_y = WIN_HEIGHT - self.size[1] - BORDER
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 140:
                self.vel = 12
                self.attack_id = None
            if self.attack_faze == 0:
                self.vel = 10
            self.attack_faze += 1
        elif self.attack_id == 1:  # New Attack
            if self.attack_faze % 20 == 0 and self.attack_faze % 40 != 0:
                self.vel = 16
                self.random_x = (WIN_WIDTH - self.size[0]) / 2 - 300
                self.random_y = 2 * BORDER + self.size[1]
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze % 40 == 0 or self.attack_faze == 0:
                self.vel = 16
                self.random_x = (WIN_WIDTH - self.size[0]) / 2 + 300
                self.random_y = 2 * BORDER + self.size[1]
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 201:
                self.vel = 12
                self.attack_id = None
            self.attack_faze += 1
        elif self.attack_id == 2:  # New Attack
            if self.attack_faze == 0:
                self.vel = 18
                self.random_x = (WIN_WIDTH - self.size[0]) / 2
                self.random_y = 2 * BORDER + self.size[1]
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 120:
                self.vel = 12
                self.attack_id = None
            self.attack_faze += 1
        elif self.attack_id == 3:  # New Attack
            if self.tmp == 0:
                self.tmp = 3
            if self.attack_faze == 0:
                self.vel = 6
                self.random_x = (WIN_WIDTH - self.size[0]) / 2
                self.random_y = BORDER
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 20:
                self.vel = 6
                self.random_x = (WIN_WIDTH - self.size[0]) / 2
                self.random_y = random.randint(WIN_HEIGHT - self.size[0] - BORDER - 512,
                                               WIN_HEIGHT - self.size[0] - BORDER - 100)
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 25:
                self.vel = 6
                self.random_x = random.randint(0, 1) * (WIN_WIDTH - self.size[0] - 2 * BORDER) + BORDER
                self.random_y = self.y
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 29:
                if self.tmp > 1:
                    self.attack_faze = -1
                    self.tmp -= 1
            elif self.attack_faze == 30:
                self.vel = 12
                self.tmp = 0
                self.attack_id = None
            self.attack_faze += 1
        elif self.attack_id == 4:  # New Attack
            if self.tmp == 0:
                self.tmp = 5
            if self.attack_faze == 0:
                self.vel = 12
                self.random_x = (WIN_WIDTH - self.size[0]) / 2
                self.random_y = 3 * BORDER
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 15:
                self.vel = 12
                self.random_x = self.x
                self.random_y = -self.size[1]
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 20:
                self.vel = 6
                self.random_x = random.randint(BORDER, WIN_WIDTH - BORDER - self.size[0])
                self.random_y = -self.size[1]
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
                pg.mixer.Sound("sounds/boss_game/scream2.mp3").play()
            elif self.attack_faze == 40:
                self.vel = 6
                self.random_x = self.player.x
                self.random_y = WIN_HEIGHT - BORDER - self.size[1]
                self.x_distance = (self.random_x - self.x)
                self.y_distance = (self.random_y - self.y)
            elif self.attack_faze == 43:
                if self.tmp > 1:
                    self.attack_faze = -1
                    self.tmp -= 1
            elif self.attack_faze == 45:
                self.vel = 12
                self.tmp = 0
                self.attack_id = None
            self.attack_faze += 1
