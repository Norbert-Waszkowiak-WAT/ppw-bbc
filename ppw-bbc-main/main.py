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

        self.character_spritesheet = Spirtesheet('img/character.png')
        self.enemy_spritesheet = Spirtesheet('img/enemy.png')
        self.terrain_spritesheet = Spirtesheet('img/terrain.png')

        self.camera_x = 0
        self.camera_y = 0

    def createTilemap(self):

        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):

                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)
                if column == 'P':
                    Player(self, j, i)

    def get_player(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                return sprite
        return None

    def new(self):

        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()
        self.player = self.get_player()

    def events(self):

        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.player.movement()

        self.camera_x = self.player.rect.centerx - WIN_WIDTH // 2
        self.camera_y = self.player.rect.centery - WIN_HEIGHT // 2

        # Przesuń wszystkie sprite'y względem pozycji kamery
        for sprite in self.all_sprites:
            sprite.rect.x -= self.camera_x
            sprite.rect.y -= self.camera_y

    def draw(self):
        # game loop draw
        self.screen.fill(BLACK)

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect)

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