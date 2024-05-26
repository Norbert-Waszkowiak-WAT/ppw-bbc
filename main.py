import pygame
from actions import *
from numbers import *
from Snake_1vs1 import *
from Boss import *
from shoter import *
from jetpack import *
from cup_game import *
import sys
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
win = 0
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
        self.heads_spritesheet = Spritesheet('img/heads.png')

        self.camera_x = 0
        self.camera_y = 0

        self.game_state = "intro_game"
        self.dialouge = False
        self.if_pause = False

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.rivers = pygame.sprite.LayeredUpdates()
        self.bridges = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.bosses = pygame.sprite.LayeredUpdates()
        self.text = pygame.sprite.LayeredUpdates()
        self.buttons = pygame.sprite.LayeredUpdates()
        self.chests = pygame.sprite.LayeredUpdates()
        self.weapons = pygame.sprite.LayeredUpdates()
        self.grounds = pygame.sprite.LayeredUpdates()


        self.i = 0
        self.faded_sprites = []
        self.score = 0
        self.tokens = 0

        self.player_head = pygame.transform.scale(self.heads_spritesheet.get_sprite(0, 0, 48, 48), (290, 290))
        self.bar_head = pygame.transform.scale(self.heads_spritesheet.get_sprite(0, 48, 64, 64), (290, 290))


    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column != 'W':
                    Floor(self, j, i, column)
                if column == 'P':
                    Player(self, j, i)
                if column == 'b':
                    Floor(self, j, i, column)
                elif column == 'W':
                    Ground(self, j, i)
                elif column == "B":
                    Block(self, j, i)
                elif column == "D":
                    Door(self, j, i, 200)
                elif column == "d":
                    Door(self, j, i, 500)
                elif column == 'S':
                    Boss(self, j, i, "snake_game", 200)
                elif column == 'J':
                    Boss(self, j, i, "jetpack_game", 100)
                elif column == 's':
                    Boss(self, j, i, "small_game", 0)
                elif column == 'I':
                    Boss(self, j, i, "shooter_game", 100)
                elif column == 'c':
                    Boss(self, j, i, "cup_game", 0)

    def create_buttons(self):
        self.image = self.buttons_spritesheet.get_sprite(0, 64, 3 * TILESIZE, TILESIZE)
        self.new_game_button = Button(self, 500, 400, self.image, 3)
        self.image = self.buttons_spritesheet.get_sprite(0, 128, 3 * TILESIZE, TILESIZE)
        self.exit_button = Button(self, 500, 600, self.image, 3)
        self.image = self.buttons_spritesheet.get_sprite(0, 0, 3 * TILESIZE, TILESIZE)
        self.continue_button = Button(self, 500, 200, self.image, 3)
    def get_player(self):

        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                return sprite
        return None

    def end_boss(self, which_game):
        for sprite in self.all_sprites:
            if isinstance(sprite, Boss):
                if sprite.which_game == which_game :
                    self.score += sprite.score
                if which_game == "small_game":
                    self.victory()
        for door in self.doors:
            if door.health <= self.score:
                door.kill()





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
        # zmienne
        self.screen.fill(BLACK)

        self.camera_x = 0
        self.camera_y = 0
        self.game_state = "main_game"
        self.dialouge = False
        self.if_pause = False
        self.score = 0
        self.i = 0
        # sprites
        self.all_sprites.empty()
        self.blocks.empty()
        self.enemies.empty()
        self.attacks.empty()
        self.bosses.empty()
        self.text.empty()
        self.buttons.empty()
        self.chests.empty()
        self.weapons.empty()
        self.doors.empty()


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

        font = pygame.font.SysFont("Arial", 65)
        self.screen.blit(pygame.transform.scale(pygame.image.load('img/tokens.png'), (300, 100)), (0, 0))
        self.screen.blit(pygame.transform.scale(pygame.image.load('img/tickets.png'), (300, 100)), (1235, 0))
        score_text = font.render(str(self.score), True, WHITE)
        screen.blit(score_text, (1335, 10))
        tokens = font.render(str(self.tokens), True, WHITE)
        screen.blit(tokens, (100, 10))



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

    def no_tokens(self):
        pass

    def snake_game(self):
        self.dialouge = True
        """
        self.snake_messages = ["Hej głupi głupku!", "Musisz udowdnić że władasz lepiej swoim pythonem ode mnie", "Zagrajmy. Musisz 3 razy ogłuszyć karpia. Grałeś w slither.io? Coś w tym stylu. Obyś zdechł <3" ,"Jeśli jesteś słabiutki i nie jesteś w stanie pokonać hipermaszyny stworzonej przez największe mózgi tego świata. Naciśnij x"]
        """
        self.snake_messages = ["Zagrajmy"]
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
        self.small_messages = ["Zagrajmy"]
        text = Text(self, self.small_messages)

        while self.dialouge:
            text.write()
            pygame.display.update()
        self.small = BossGame(self)
        self.small.run()
        self.game_state = "main_game"
    def shooter_game(self):
        self.dialouge = True
        """
        self.small_messages = ["To jest pierwsza wiadomość", "To jest druga wiadomość", "To jest trzecia wiadomość"
                               ,"To jest czwarta wiadomość"]
        """
        self.small_messages = ["Zagrajmy"]
        text = Text(self, self.small_messages)

        while self.dialouge:
            text.write()
            pygame.display.update()
        self.shooter = ShooterGame(self)
        self.shooter.run()
        self.game_state = "main_game"
    def jetpack_game(self):
        self.dialouge = True
        """
        self.small_messages = ["To jest pierwsza wiadomość", "To jest druga wiadomość", "To jest trzecia wiadomość"
                               ,"To jest czwarta wiadomość"]
        """
        self.small_messages = ["Zagrajmy"]
        text = Text(self, self.small_messages)

        while self.dialouge:
            text.write()
            pygame.display.update()
        self.jetpack = JetpackGame(self)
        self.jetpack.run()
        self.game_state = "main_game"

    def cup_game(self):

        self.dialouge = True
        """
        self.bar_messages = ["To jest pierwsza wiadomość", "To jest druga wiadomość", "To jest trzecia wiadomość"
                               ,"To jest czwarta wiadomość"]
        """
        self.bar_messages = ["Zagrajmy"]
        text = Text(self, self.bar_messages)

        while self.dialouge:
            text.write()
            self.screen.blit(self.player_head, (0, WIN_HEIGHT - 300))
            pygame.display.update()
        self.bar = CupGame(self)
        self.bar.run()
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

                elif self.game_state == "shooter_game":
                    self.shooter_game()

                elif self.game_state == "jetpack_game":
                    self.jetpack_game()

                elif self.game_state == "cup_game":
                    self.cup_game()

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
    def victory(self):
        game_over_font = pg.font.Font(None, 36)
        game_over_text = game_over_font.render("Przestań naciskać x", True, (0, 255, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_text, game_over_rect)
        pg.display.flip()
        pg.time.wait(1000)
        pygame.quit()
        sys.exit()
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
