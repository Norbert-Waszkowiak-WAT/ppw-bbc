import pygame
from actions import *
from numbers import *
import sys

class Game:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

    def createTilemap(self):

        """i = 0
        j = 0
        for row in tilemap:
            for column in row:
                if column == 'B':
                    Block(self, i, j)
                if column == 'P':
                    Player(self, i, j)
                    j += 1
            i += 1"""
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == 'B':
                    Block(self, i, j)
                if column == 'P':
                    Player(self, i, j)


    def new(self):

        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.createTilemap()

    def events(self):

        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):

        #gmae loop updates
        self.all_sprites.update()

    def draw(self):

        #game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):

        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass


g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()