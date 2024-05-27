import pygame
from copy import deepcopy
from random import choice, randrange

W, H = 10, 15
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 700
FPS = 60


class TetrisGame:
    def __init__(self, main):
        pygame.init()
        self.game = main
        self.sc = pygame.display.set_mode(RES)
        self.game_sc = pygame.Surface(GAME_RES)
        self.clock = pygame.time.Clock()
        self.game_state = "easter_egg"
        self.grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

        self.figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                            [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                            [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                            [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                            [(0, 0), (0, -1), (0, 1), (-1, -1)],
                            [(0, 0), (0, -1), (0, 1), (1, -1)],
                            [(0, 0), (0, -1), (0, 1), (-1, 0)]]

        self.figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in self.figures_pos]
        self.figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
        self.field = [[0 for _ in range(W)] for _ in range(H)]

        self.anim_count, self.anim_speed, self.anim_limit = 0, 60, 2000

        self.bg = pygame.image.load('img/bg.jpg').convert()
        self.game_bg = pygame.image.load('img/bg2.jpg').convert()

        self.main_font = pygame.font.Font('font/font.ttf', 65)
        self.font = pygame.font.Font('font/font.ttf', 45)

        self.title_tetris = self.main_font.render('TETRIS', True, pygame.Color('darkorange'))
        self.title_score = self.font.render('score:', True, pygame.Color('darkorange'))
        self.title_record = self.font.render('record:', True, pygame.Color('darkorange'))

        self.figure, self.next_figure = deepcopy(choice(self.figures)), deepcopy(choice(self.figures))
        self.color, self.next_color = self.get_color(), self.get_color()

        self.score, self.lines = 0, 0
        self.scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def get_color(self):
        return (randrange(30, 256), randrange(30, 256), randrange(30, 256))

    def check_borders(self):
        for i in range(4):
            if self.figure[i].x < 0 or self.figure[i].x > W - 1:
                return False
            elif self.figure[i].y > H - 1 or self.field[self.figure[i].y][self.figure[i].x]:
                return False
        return True

    def get_record(self):
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')
            return '0'

    def set_record(self, record, score):
        rec = max(int(record), score)
        with open('record', 'w') as f:
            f.write(str(rec))

    def handle_events(self):
        dx, rotate = 0, False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.game_state = "main_game"
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    self.anim_limit = 100
                elif event.key == pygame.K_UP:
                    rotate = True

        return dx, rotate

    def move_figure(self, dx, rotate):
        # move x
        figure_old = deepcopy(self.figure)
        for i in range(4):
            self.figure[i].x += dx
            if not self.check_borders():
                self.figure = deepcopy(figure_old)
                break
        # move y
        self.anim_count += self.anim_speed
        if self.anim_count > self.anim_limit:
            self.anim_count = 0
            figure_old = deepcopy(self.figure)
            for i in range(4):
                self.figure[i].y += 1
                if not self.check_borders():
                    for i in range(4):
                        self.field[figure_old[i].y][figure_old[i].x] = self.color
                    self.figure, self.color = self.next_figure, self.next_color
                    self.next_figure, self.next_color = deepcopy(choice(self.figures)), self.get_color()
                    self.anim_limit = 2000
                    break
        # rotate
        center = self.figure[0]
        figure_old = deepcopy(self.figure)
        if rotate:
            for i in range(4):
                x = self.figure[i].y - center.y
                y = self.figure[i].x - center.x
                self.figure[i].x = center.x - x
                self.figure[i].y = center.y + y
                if not self.check_borders():
                    self.figure = deepcopy(figure_old)
                    break

    def check_lines(self):
        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if self.field[row][i]:
                    count += 1
                self.field[line][i] = self.field[row][i]
            if count < W:
                line -= 1
            else:
                self.anim_speed += 3
                lines += 1
        self.score += self.scores[lines]

    def draw(self, record):
        self.sc.blit(self.bg, (0, 0))
        self.sc.blit(self.game_sc, (20, 20))
        self.game_sc.blit(self.game_bg, (0, 0))

        [pygame.draw.rect(self.game_sc, (80, 80, 80), i_rect, 1) for i_rect in self.grid]

        for i in range(4):
            self.figure_rect.x = self.figure[i].x * TILE
            self.figure_rect.y = self.figure[i].y * TILE
            pygame.draw.rect(self.game_sc, self.color, self.figure_rect)

        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if col:
                    self.figure_rect.x, self.figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(self.game_sc, col, self.figure_rect)

        for i in range(4):
            self.figure_rect.x = self.next_figure[i].x * TILE + 350
            self.figure_rect.y = self.next_figure[i].y * TILE + 220
            pygame.draw.rect(self.sc, self.next_color, self.figure_rect)

        self.sc.blit(self.title_score, (540, 50))
        self.sc.blit(self.font.render(str(self.score), True, pygame.Color('white')), (580, 120))
        self.sc.blit(self.title_record, (540, 400))
        self.sc.blit(self.font.render(record, True, pygame.Color('white')), (580, 500))

    def game_over(self, record):
        for i in range(W):
            if self.field[0][i]:
                self.set_record(record, self.score)
                self.field = [[0 for _ in range(W)] for _ in range(H)]
                self.anim_count, self.anim_speed, self.anim_limit = 0, 60, 2000
                self.score = 0
                for i_rect in self.grid:
                    pygame.draw.rect(self.game_sc, self.get_color(), i_rect)
                    self.sc.blit(self.game_sc, (20, 20))
                    pygame.display.flip()
                    self.clock.tick(200)

    def run(self):
        while True and self.score < 500 and self.game_state == "easter_egg":
            record = self.get_record()
            dx, rotate = self.handle_events()
            self.move_figure(dx, rotate)
            self.check_lines()
            self.draw(record)
            self.game_over(record)
            pygame.display.flip()
            self.clock.tick(FPS)
        quit()





