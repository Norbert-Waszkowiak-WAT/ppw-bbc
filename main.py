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
        self.if_pause = False

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.rivers = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.bosses = pygame.sprite.LayeredUpdates()
        self.text = pygame.sprite.LayeredUpdates()
        self.buttons = pygame.sprite.LayeredUpdates()
        self.chests = pygame.sprite.LayeredUpdates()
        self.weapons = pygame.sprite.LayeredUpdates()

        self.i = 0


    def createTilemap(self):
        x = 0
        k = 0
        y = 1
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                elif column == 'E':
                    Enemy(self, j, i)
                elif column == 'P':
                    Player(self, j, i)
                elif column == 'R':
                    River(self, j, i, x)
                    x = (x + 1) % 3
                elif column == 'S':
                    Boss(self, j, i, k)
                    k += 1
                elif column == 's':
                    Boss(self, j, i, k)
                    k += 1
                elif column == 't':
                    Tree(self, j, i, 1)
                elif column == 'T':
                    Tree(self, j, i, 2)
                elif column == 'c':
                    Chest(self, j, i, y, 0)
                    y += 1
    def create_buttons(self):
        self.image = self.buttons_spritesheet.get_sprite(0, 64, 6 * TILESIZE, 2 * TILESIZE)
        self.new_game_button = Button(self, 500, 400, self.image, 3)
        self.image = self.buttons_spritesheet.get_sprite(0, 128, 6 * TILESIZE, 2 * TILESIZE)
        self.exit_button = Button(self, 500, 550, self.image, 3)
        self.image = self.buttons_spritesheet.get_sprite(0, 0, 6 * TILESIZE, 2 * TILESIZE)
        self.continue_button = Button(self, 500, 250, self.image, 3)
    def get_player(self):

        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                return sprite
        return None

    def kill_boss(self, k):
        for sprite in self.all_sprites:
            if isinstance(sprite, Boss):
                if sprite.k == k:
                    sprite.kill()
    def new(self):

        self.playing = True
        self.createTilemap()
        self.player = self.get_player()

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.chest():
                        pass
                    else:
                        self.player.attack()
                if event.key == pygame.K_ESCAPE:
                        self.if_pause = True
                        self.game_state = "pause_game"

    def restart(self):
        # Reset all game variables and state
        self.screen.fill(BLACK)

        self.camera_x = 0
        self.camera_y = 0
        self.game_state = "main_game"
        self.dialouge = False
        self.if_pause = False
        self.i = 0
        # Clear all sprites
        self.all_sprites.empty()
        self.blocks.empty()
        self.enemies.empty()
        self.attacks.empty()
        self.bosses.empty()
        self.text.empty()
        self.buttons.empty()
        self.chests.empty()
        self.weapons.empty()

        self.new_game_button.kill()
        self.exit_button.kill()
        self.continue_button.kill()




    def update(self):

        self.all_sprites.update()

        self.new_game_button.kill()
        self.exit_button.kill()
        self.continue_button.kill()

        self.camera_x = self.player.rect.centerx - WIN_WIDTH // 2
        self.camera_y = self.player.rect.centery - WIN_HEIGHT // 2

    def fade_sprites(self):

        for sprite in self.all_sprites:
            is_screen = (sprite.rect.left < self.player.rect.centerx + WIN_WIDTH // 2 + TILESIZE and
                         sprite.rect.right > self.player.rect.centerx - WIN_WIDTH // 2 - TILESIZE and
                         sprite.rect.bottom > self.player.rect.centery - WIN_HEIGHT // 2 - TILESIZE and
                         sprite.rect.top < self.player.rect.centery + WIN_HEIGHT // 2 + TILESIZE)
            if sprite not in self.buttons and is_screen:
                sprite.image.set_alpha(
                    128)  # Ustaw poziom przezroczystości (0 - całkowicie przezroczysty, 255 - nieprzezroczysty)

    def unfade_sprites(self):
        for sprite in self.all_sprites:
            is_screen = (sprite.rect.left < self.player.rect.centerx + WIN_WIDTH // 2 + TILESIZE and
                         sprite.rect.right > self.player.rect.centerx - WIN_WIDTH // 2 - TILESIZE and
                         sprite.rect.bottom > self.player.rect.centery - WIN_HEIGHT // 2 - TILESIZE and
                         sprite.rect.top < self.player.rect.centery + WIN_HEIGHT // 2 + TILESIZE)
            if sprite not in self.buttons and is_screen:
                sprite.image.set_alpha(
                    255)  # Ustaw poziom przezroczystości (0 - całkowicie przezroczysty, 255 - nieprzezroczysty)

    def draw(self):
        self.screen.fill(WHITE)
        for sprite in self.all_sprites:
            is_screen = (sprite.rect.left < self.player.rect.centerx + WIN_WIDTH // 2 + TILESIZE and
                         sprite.rect.right > self.player.rect.centerx - WIN_WIDTH // 2 - TILESIZE and
                         sprite.rect.bottom > self.player.rect.centery - WIN_HEIGHT // 2 - TILESIZE and
                         sprite.rect.top < self.player.rect.centery + WIN_HEIGHT // 2 + TILESIZE)
            if is_screen:
                sprite_on_screen_x = sprite.rect.x - self.camera_x
                sprite_on_screen_y = sprite.rect.y - self.camera_y
                if not isinstance(sprite, Weapon):
                    self.screen.blit(sprite.image, (sprite_on_screen_x, sprite_on_screen_y))
                elif self.i != 0:
                    self.screen.blit(sprite.scaled_image, (sprite_on_screen_x, sprite_on_screen_y))



        self.clock.tick(FPS)

        if self.game_state == "pause_game":
            self.new_game_button.draw(self.screen)
            self.exit_button.draw(self.screen)
            self.continue_button.draw(self.screen)
        pygame.display.update()

    def looting(self, k):
        for weapon in self.weapons:
            initial_y = weapon.rect.y

            for i in range(1, 301):
                self.i += 1
                scale_factor = i / 100.0

                weapon.scale_image(scale_factor)

                weapon.rect.y = initial_y - i

                pygame.time.wait(10)

                self.draw()
                self.all_sprites.move_to_front(weapon)

                pygame.display.update()

            weapon.state = 3

        pygame.time.wait(2500)
        self.all_sprites.get_top_sprite().kill()
        self.weapons.empty()
        for chest in self.chests:
            if chest.k == k:
                chest.state = 2

        self.game_state = "main_game"

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
            if self.if_pause == False:
                if self.game_state == "main_game":
                    self.events()
                    self.update()
                    self.draw()

                elif self.game_state == "snake_game":
                    self.snake_game()

                elif self.game_state == "small_game":
                    self.small_game()

                elif self.game_state == "intro_game":
                    self.intro_screen()
            else:
                if self.game_state == "pause_game":
                    self.pause()


        self.running = False

    def game_over(self):
        game_over_font = pygame.font.Font(None, 36)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)

        self.screen.fill(BLACK)
        self.screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()

        pygame.time.wait(500)  # Oczekiwanie przez 0,5 sekundy
        self.playing = False

    def intro_screen(self):
        self.create_buttons()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Lewy przycisk myszy
                    x, y = event.pos
                    if self.new_game_button.rect.collidepoint(x, y):
                        self.game_state = "main_game"
                    elif self.exit_button.rect.collidepoint(x, y):
                        self.game_over()

        self.new_game_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        pygame.display.update()

        self.new_game_button.kill()
        self.exit_button.kill()
        self.continue_button.kill()

    def pause(self):
        self.fade_sprites()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Lewy przycisk myszy
                    x, y = event.pos
                    if self.new_game_button.rect.collidepoint(x, y):
                        self.restart()
                        self.new()
                        self.main()
                    elif self.exit_button.rect.collidepoint(x, y):
                        self.game_over()
                    elif self.continue_button.rect.collidepoint(x, y):
                        self.unfade_sprites()
                        self.if_pause = False
                        self.game_state = "main_game"
        self.draw()

g = Game()
g.new()
while g.running:
    g.main()
g.game_over()
pygame.quit()
sys.exit()