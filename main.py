import pygame
from actions import *
from numbers import *
from Snake_1vs1 import *
from Boss import *
import sys


class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.if_boss = True

        self.character_spritesheet = Spritesheet('img/character.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        self.text_spritesheet = Spritesheet('img/text.png')
        self.buttons_spritesheet = Spritesheet('img/buttons.png')

        self.camera_x = 0
        self.camera_y = 0

        self.game_state = "intro_game"
        self.dialouge = False

        self.new_image = self.buttons_spritesheet.get_sprite(0, 64, 6 * TILESIZE, 2 * TILESIZE)
        self.new_game_button = Button(250, 400, self.new_image, 2.2)
        self.exit_image = self.buttons_spritesheet.get_sprite(0, 128, 6 * TILESIZE, 2 * TILESIZE)
        self.exit_button = Button(850, 400, self.exit_image, 2.2)


    def createTilemap(self):
        x = 0
        k = 0
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)
                if column == 'P':
                    Player(self, j, i)
                if column == 'R':
                    River(self, j, i, x)
                    x = (x + 1) % 3
                if column == 'S':
                    Boss(self, j, i, k)
                    k += 1
                if column == 's':
                    Boss(self, j, i, k)
                    k += 1

    def get_player(self):

        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                return sprite
        return None

    def kill_boss(self, k):
        for sprite in self.all_sprites:
            if isinstance(sprite, Boss):
                if sprite.k == k:
                    self.all_sprites.remove(sprite)

    def new(self):

        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.boss = pygame.sprite.LayeredUpdates()
        self.text = pygame.sprite.LayeredUpdates()

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
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

    def update(self):
        pos = pygame.mouse.get_pos()
        print(pos)
        self.all_sprites.update()

        self.camera_x = self.player.rect.centerx - TOTAL_WIDTH // 2
        self.camera_y = self.player.rect.centery - TOTAL_HEIGHT // 2

    def draw(self):

        self.screen.fill(BLUE)

        for sprite in self.all_sprites:
            is_screen = (sprite.rect.left < self.player.rect.centerx + TOTAL_WIDTH // 2 + TILESIZE and
                         sprite.rect.right > self.player.rect.centerx - TOTAL_WIDTH // 2 - TILESIZE and
                         sprite.rect.bottom > self.player.rect.centery - TOTAL_HEIGHT // 2 - TILESIZE and
                         sprite.rect.top < self.player.rect.centery + TOTAL_HEIGHT // 2 + TILESIZE)
            if is_screen:
                sprite_on_screen_x = sprite.rect.x - self.camera_x
                sprite_on_screen_y = sprite.rect.y - self.camera_y
                self.screen.blit(sprite.image, (sprite_on_screen_x, sprite_on_screen_y))

        self.clock.tick(FPS)
        pygame.display.update()

    def snake_game(self):
        self.dialouge = True
        """
        self.snake_messages = ["To jest pierwsza wiadomość", "To jest druga wiadomość", "To jest trzecia wiadomość"
                               ,"To jest czwarta wiadomość"]
        """
        self.snake_messages = ["kys"]
        text = Text(self, self.snake_messages)

        while self.dialouge:
            text.write()
            pygame.display.update()
        self.snake = SnakeGame(self)
        self.snake.run()
        self.game_state = "main_game"

    def small_game(self):

        self.dialouge = True
        """
        self.small_messages = ["To jest pierwsza wiadomość", "To jest druga wiadomość", "To jest trzecia wiadomość"
                               ,"To jest czwarta wiadomość"]
        """
        self.small_messages = ["kys"]
        text = Text(self, self.small_messages)

        while self.dialouge:
            text.write()
            pygame.display.update()
        self.small = BossGame(self)
        self.small.run()
        self.game_state = "main_game"

    def main(self):
        while self.playing:
            if self.game_state == "main_game":
                self.events()
                self.update()
                self.draw()

            elif self.game_state == "snake_game":
                self.snake_game()

            elif self.game_state == "small_game":
                self.small_game()

            if self.game_state == "intro_game":
                self.intro_screen()

            self.running = False

    def game_over(self):
        game_over_font = pygame.font.Font(None, 36)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)

        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()

        pygame.time.wait(500)  # Oczekiwanie przez 0,5 sekundy
        self.playing = False

    def intro_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Lewy przycisk myszy
                    x, y = event.pos
                    if self.new_game_button.rect.collidepoint(x, y):
                        print('START')
                        self.game_state = "main_game"
                    elif self.exit_button.rect.collidepoint(x, y):
                        print('EXIT')
                        self.game_over()
        self.new_game_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        pygame.display.update()

g = Game()
g.new()
while g.running:
    g.main()
g.game_over()
pygame.quit()
sys.exit()