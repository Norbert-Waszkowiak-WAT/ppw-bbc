import random
import pygame
from numbers import *
import time
class JetpackGame:
    def __init__(self, main):
        self.main = main
        self.game_state = "jetpack_game"
        pygame.init()
        self.WIDTH = WIN_WIDTH
        self.HEIGHT = WIN_HEIGHT
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.bg_color = (128, 128, 128)

        self.fps = 60
        self.timer = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        self.lines = [0, self.WIDTH / 4, 2 * self.WIDTH / 4, 3 * self.WIDTH / 4]

        self.init_y = self.HEIGHT - 130
        self.player_y = self.init_y

        self.pause = False
        self.booster = False
        self.new_laser = True
        self.restart_cmd = False
        self.laser = []
        self.game_speed = 6
        self.distance = 0
        self.new_bg = 0
        self.counter = 0
        self.y_velocity = 0
        self.gravity = 0.4

        self.rocket_counter = 0
        self.rocket_active = False
        self.rocket_delay = 0
        self.rocket_coords = []

        self.read_high_score()


    def run(self):
        while self.game_state == "jetpack_game":
            self.update()

    def read_high_score(self):
        with open('score.txt', 'r') as file:
            read = file.readlines()
            self.high_score = int(read[0])
            self.lifetime = int(read[1])

    def draw_screen(self):
        self.screen.fill('black')
        pygame.draw.rect(self.surface, (self.bg_color[0], self.bg_color[1], self.bg_color[2], 50), [0, 0, self.WIDTH, self.HEIGHT])
        self.screen.blit(self.surface, (0, 0))
        top = pygame.draw.rect(self.screen, 'gray', [0, 0, self.WIDTH, 50])
        bot = pygame.draw.rect(self.screen, 'gray', [0, self.HEIGHT - 50, self.WIDTH, 50])

        for i in range(len(self.lines)):
            pygame.draw.line(self.screen, 'black', (self.lines[i], 0), (self.lines[i], 50), 3)
            pygame.draw.line(self.screen, 'black', (self.lines[i], self.HEIGHT - 50), (self.lines[i], self.HEIGHT), 3)
            if not self.pause:
                self.lines[i] -= self.game_speed
                self.laser[0][0] -= self.game_speed
                self.laser[1][0] -= self.game_speed
            if self.lines[i] < 0:
                self.lines[i] = self.WIDTH
        lase_line = pygame.draw.line(self.screen, 'yellow', (self.laser[0][0], self.laser[0][1]), (self.laser[1][0], self.laser[1][1]), 10)
        pygame.draw.circle(self.screen, 'yellow', (self.laser[0][0], self.laser[0][1]), 12)
        pygame.draw.circle(self.screen, 'yellow', (self.laser[1][0], self.laser[1][1]), 12)
        self.screen.blit(self.font.render(f'Distance: {int(self.distance)} m', True, 'white'), (10, 10))
        self.screen.blit(self.font.render(f'High Score: {int(self.high_score)} m', True, 'white'), (10, 70))
        return top, bot, lase_line

    def draw_pause(self):
        pygame.draw.rect(self.surface, (128, 128, 128, 150), [0, 0, self.WIDTH, self.HEIGHT])
        pygame.draw.rect(self.surface, 'dark gray', [200, 150, 600, 50], 0, 10)
        self.surface.blit(self.font.render('Game Paused. Escape Btn Resumes', True, 'black'), (220, 160))
        restart_btn = pygame.draw.rect(self.surface, 'white', [200, 220, 280, 50], 0, 10)
        self.surface.blit(self.font.render('Restart', True, 'black'), (220, 230))
        quit_btn = pygame.draw.rect(self.surface, 'white', [520, 220, 280, 50], 0, 10)
        self.surface.blit(self.font.render('Quit', True, 'black'), (540, 230))
        pygame.draw.rect(self.surface, 'dark gray', [200, 300, 600, 50], 0, 10)
        self.surface.blit(self.font.render(f'Lifetime Distance Ran: {int(self.lifetime)}', True, 'black'), (220, 310))
        self.screen.blit(self.surface, (0, 0))
        return restart_btn, quit_btn

    def modify_player_info(self):
        if self.distance > self.high_score:
            self.high_score = self.distance
        self.lifetime += self.distance
        with open('score.txt', 'w') as file:
            file.write(str(int(self.high_score)) + '\n')
            file.write(str(int(self.lifetime)))

    def check_colliding(self, player, bot_plat, top_plat, laser_line):
        coll = [False, False]
        rstrt = False
        if player.colliderect(bot_plat):
            coll[0] = True
        elif player.colliderect(top_plat):
            coll[1] = True
        if laser_line.colliderect(player):
            rstrt = True
        if self.rocket_active:
            if self.rocket.colliderect(player):
                rstrt = True
        return coll, rstrt

    def generate_laser(self):
        laser_type = random.choice([0, 1])
        offset = random.randint(10, 300)

        if laser_type == 0:
            laser_width = random.randint(100, 300)
            laser_y = random.randint(100, self.HEIGHT - 100)
            new_lase = [[self.WIDTH + offset, laser_y], [self.WIDTH + offset + laser_width, laser_y]]
        else:
            laser_height = random.randint(100, 300)
            laser_y = random.randint(100, self.HEIGHT - 400)
            new_lase = [[self.WIDTH + offset, laser_y], [self.WIDTH + offset, laser_y + laser_height]]

        return new_lase

    def update(self):
        if self.distance > 5000:
            self.victory()
        self.timer.tick(self.fps)
        if self.counter < 40:
            self.counter += 1
        else:
            self.counter = 0
        if self.new_laser:
            self.laser = self.generate_laser()
            self.new_laser = False
        top_plat, bot_plat, laser_line = self.draw_screen()
        if self.pause:
            restart, quits = self.draw_pause()

        if not self.rocket_active and not self.pause:
            self.rocket_counter += 1
        if self.rocket_counter > 180:
            self.rocket_counter = 0
            self.rocket_active = True
            self.rocket_delay = 0
            self.rocket_coords = [self.WIDTH, self.HEIGHT / 2]
        if self.rocket_active:
            if self.rocket_delay < 90:
                if not self.pause:
                    self.rocket_delay += 1
                self.rocket_coords, self.rocket = self.draw_rocket(self.rocket_coords, 0)
            else:
                self.rocket_coords, self.rocket = self.draw_rocket(self.rocket_coords, 1)
            if self.rocket_coords[0] < -50:
                self.rocket_active = False

        player = self.draw_player()
        colliding, self.restart_cmd = self.check_colliding(player, bot_plat, top_plat, laser_line)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.modify_player_info()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.pause:
                        self.pause = False
                    else:
                        self.pause = True
                if event.key == pygame.K_x:
                    self.victory()
                if event.key == pygame.K_SPACE and not self.pause:
                    self.booster = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.booster = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.pause:
                if restart.collidepoint(event.pos):
                    self.restart_cmd = True
                if quits.collidepoint(event.pos):
                    self.modify_player_info()
                    quit()

        if not self.pause:
            self.distance += self.game_speed
            if self.booster:
                self.y_velocity -= self.gravity
            else:
                self.y_velocity += self.gravity
            if (colliding[0] and self.y_velocity > 0) or (colliding[1] and self.y_velocity < 0):
                self.y_velocity = 0
            self.player_y += self.y_velocity

        if self.distance < 50000:
            self.game_speed = 4 + (self.distance // 500) / 10
        else:
            self.game_speed = 11

        if self.laser[0][0] < 0 and self.laser[1][0] < 0:
            self.new_laser = True

        if self.distance - self.new_bg > 500:
            self.new_bg = self.distance
            self.bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        if self.restart_cmd:
            self.modify_player_info()
            self.distance = 0
            self.rocket_active = False
            self.rocket_counter = 0
            self.pause = False
            self.player_y = self.init_y
            self.y_velocity = 0
            self.restart_cmd = 0
            self.new_laser = True

        if self.distance > self.high_score:
            self.high_score = int(self.distance)

        pygame.display.flip()

    def victory(self):
        pygame.mixer.stop()
        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render('Wygrałeś!!!', True, (255, 255, 0))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (WIN_WIDTH / 2, WIN_HEIGHT / 4)

        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

        time.sleep(3)
        self.game_state = "main_game"
        self.main.end_boss("jetpack_game")

    def draw_player(self):
        play = pygame.rect.Rect((120, self.player_y + 10), (25, 60))
        if self.player_y < self.init_y or self.pause:
            if self.booster:
                pygame.draw.ellipse(self.screen, 'red', [100, self.player_y + 50, 20, 30])
                pygame.draw.ellipse(self.screen, 'orange', [105, self.player_y + 50, 10, 30])
                pygame.draw.ellipse(self.screen, 'yellow', [110, self.player_y + 50, 5, 30])
            pygame.draw.rect(self.screen, 'yellow', [128, self.player_y + 60, 10, 20], 0, 3)
            pygame.draw.rect(self.screen, 'orange', [130, self.player_y + 60, 10, 20], 0, 3)
        else:
            if self.counter < 10:
                pygame.draw.line(self.screen, 'yellow', (128, self.player_y + 60), (140, self.player_y + 80), 10)
                pygame.draw.line(self.screen, 'orange', (130, self.player_y + 60), (120, self.player_y + 80), 10)
            elif 10 <= self.counter < 20:
                pygame.draw.rect(self.screen, 'yellow', [128, self.player_y + 60, 10, 20], 0, 3)
                pygame.draw.rect(self.screen, 'orange', [130, self.player_y + 60, 10, 20], 0, 3)
            elif 20 <= self.counter < 30:
                pygame.draw.line(self.screen, 'yellow', (128, self.player_y + 60), (120, self.player_y + 80), 10)
                pygame.draw.line(self.screen, 'orange', (130, self.player_y + 60), (140, self.player_y + 80), 10)
            else:
                pygame.draw.rect(self.screen, 'yellow', [128, self.player_y + 60, 10, 20], 0, 3)
                pygame.draw.rect(self.screen, 'orange', [130, self.player_y + 60, 10, 20], 0, 3)
        pygame.draw.rect(self.screen, 'white', [100, self.player_y + 20, 20, 30], 0, 5)
        pygame.draw.ellipse(self.screen, 'orange', [120, self.player_y + 20, 30, 50])
        pygame.draw.circle(self.screen, 'orange', (135, self.player_y + 15), 10)
        pygame.draw.circle(self.screen, 'black', (138, self.player_y + 12), 3)
        return play

    def draw_rocket(self, coords, mode):
        
        if mode == 0:
            rock = pygame.draw.rect(self.screen, 'dark red', [coords[0] - 60, coords[1] - 25, 50, 50], 0, 5)
            self.screen.blit(self.font.render('!', True, 'black'), (coords[0] - 40, coords[1] - 20))
            if not self.pause:
                if coords[1] > self.player_y + 10:
                    coords[1] -= 3
                else:
                    coords[1] += 3
        else:
            rock = pygame.draw.rect(self.screen, 'red', [coords[0], coords[1] - 10, 50, 20], 0, 5)
            pygame.draw.ellipse(self.screen, 'orange', [coords[0] + 50, coords[1] - 10, 50, 20], 7)
            if not self.pause:
                coords[0] -= 10 + self.game_speed

        return coords, rock


