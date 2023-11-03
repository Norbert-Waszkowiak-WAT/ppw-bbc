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
        self.attack_spritesheet = Spirtesheet('img/attack.png')

        self.camera_x = 0
        self.camera_y = 0

    def createTilemap(self):
        x = 0
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)
                if column == 'P':
                    Player(self, j, i)
                if column == "R":
                    River(self, j, i, x)
                    x = (x + 1) % 3

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.attack()
                    """if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)"""



    def update(self):

        self.all_sprites.update()

        self.camera_x = self.player.rect.centerx - WIN_WIDTH // 2
        self.camera_y = self.player.rect.centery - WIN_HEIGHT // 2

    def draw(self):

        self.screen.fill(BLACK)

        for sprite in self.all_sprites:
            is_screen = (sprite.rect.left < self.player.rect.centerx + WIN_WIDTH // 2 + TILESIZE and
                            sprite.rect.right > self.player.rect.centerx - WIN_WIDTH // 2 - TILESIZE and
                            sprite.rect.bottom > self.player.rect.centery - WIN_HEIGHT // 2 - TILESIZE and
                            sprite.rect.top < self.player.rect.centery + WIN_HEIGHT // 2 + TILESIZE)
            if is_screen:
                sprite_on_screen_x = sprite.rect.x - self.camera_x
                sprite_on_screen_y = sprite.rect.y - self.camera_y
                self.screen.blit(sprite.image, (sprite_on_screen_x, sprite_on_screen_y))

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):

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