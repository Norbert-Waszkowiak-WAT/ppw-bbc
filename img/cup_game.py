import pygame
from numbers import *
import time
import random
pygame.init()

class Spritesheet:

    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey((BLACK))
        return sprite


class Cup(pygame.sprite.Sprite):
    def __init__(self, x, y, state, ball):
        super().__init__()
        self.width = 96
        self.height = 192
        self.state = state
        self.ball = ball
        self.spritesheet = Spritesheet('img/cups.png')
        self.image = self.spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_x = x
        self.start_y = y

    def changestate(self, state):
        if state == "down":
            self.image = self.spritesheet.get_sprite(0, 0, self.width, self.height)
        elif state == "up":
            if self.ball:
                self.image = self.spritesheet.get_sprite(112, 0, self.width, self.height)
            else:
                self.image = self.spritesheet.get_sprite(224, 0, self.width, self.height)

class CupGame:
    def __init__(self, main):
        self.main = main
        self.game_state = "cup_game"
        self.done = False
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.cup1 = Cup(500, 250, "down", False)
        self.cup2 = Cup(700, 250, "down", True)
        self.cup3 = Cup(900, 250, "down", False)
        self.cups = pygame.sprite.Group(self.cup1, self.cup2, self.cup3)
        self.clicked = False
        self.win = False
        self.moving = False
        self.up = 50
        self.down = 450
        self.step = 25
        self.mix_1 = self.cup1
        self.mix_2 = self.cup3
        self.shufles = 0



    def events(self):
        if not self.clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click = pygame.mouse.get_pos()
                    if self.cup1.rect.collidepoint(click):
                        self.handle_cup_click(self.cup1)
                    elif self.cup2.rect.collidepoint(click):
                        self.handle_cup_click(self.cup2)
                    elif self.cup3.rect.collidepoint(click):
                        self.handle_cup_click(self.cup3)

    def handle_cup_click(self, cup):

        if not self.clicked:

            self.shufles = random.randint(4,9)
            self.clicked = True
            cup.changestate("up")
            self.draw()
            time.sleep(1)
            if cup.ball:
                self.victory()
            other_cups = [c for c in [self.cup1, self.cup2, self.cup3] if c != cup]
            for other_cup in other_cups:
                other_cup.changestate("up")
            self.draw()
            time.sleep(1)
            for cup in self.cups:
                cup.changestate("down")
            self.moving = True

    def victory(self):
        self.main.tokens = 1000
        pygame.mixer.stop()
        pygame.display.flip()

        time.sleep(3)
        self.game_state = "main_game"
        self.main.end_boss("cup_game")


    def draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(pygame.transform.scale(pygame.image.load('img/table.png'), (WIN_WIDTH, WIN_HEIGHT)), (0, 0))

        self.cups.draw(self.screen)
        pygame.display.flip()

    def mix(self):
        if self.moving:
            self.shufle_1(self.mix_1, self.mix_2)
        elif self.clicked:
            self.shufles -= 1
            if self.shufles > 0:
                self.moving = True
            else:
                self.clicked = False


    def shufle_1(self, cup1, cup2):

        if cup1.rect.x < cup2.start_x:
            if cup1.rect.y > self.up:
                cup1.rect.y -= self.step
            elif cup1.rect.x < cup2.start_x:
                cup1.rect.x += self.step
            else:
                cup1.rect.y = self.up

        elif cup1.rect.x > cup2.start_x:
            cup1.rect.x = cup2.start_x

        elif cup1.rect.y < cup2.start_y:
            cup1.rect.y += self.step

        else:
            cup1.rect.y = cup2.start_y

        if cup2.rect.x > cup1.start_x:
            if cup2.rect.y < self.down:
                cup2.rect.y += self.step
            elif cup2.rect.x > cup1.start_x:
                cup2.rect.x -= self.step
            else:
                cup2.rect.y = self.down
        elif cup2.rect.x < cup1.start_x:
            cup2.rect.x = cup1.start_x
        elif cup2.rect.y > cup1.start_y:
            cup2.rect.y -= self.step
        else:
            cup2.rect.y = cup1.start_y

        if cup1.rect.x == cup2.start_x and cup1.rect.y == cup2.start_y and cup2.rect.x == cup1.start_x and cup2.rect.y == cup1.start_y:

            tmpx = cup1.start_x
            tmpy = cup1.start_y
            cup1.start_x = cup2.start_x
            cup1.start_y = cup2.start_y
            cup2.start_x = tmpx
            cup2.start_y = tmpy

            self.moving = False

            cup1, cup2 = random.sample(self.cups.sprites(), 2)

            if cup1.rect.x > cup2.rect.x:
                self.mix_1 = cup2
                self.mix_2 = cup1
            else:
                self.mix_1 = cup1
                self.mix_2 = cup2




    def shufle_2(self):
        pass

    def shufle_3(self):
        pass

    def run(self):
        while self.game_state == "cup_game":
            self.update()
            self.draw()

    def update(self):
        self.events()
        self.mix()







