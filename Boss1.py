import pygame as pg

pg.init()
window_width = 1500
window_height = 750
pg.display.set_caption('BOSS')
window = pg.display.set_mode((window_width, window_height))
fps = pg.time.Clock()


class Player:
    def __init__(self, x, y, width, hight):
        self.x = x
        self.y = y
        self.size = [width, hight]
        self.x_vel = 0
        self.y_vel = 0

    def movement(self, x_vel, y_vel):
        self.x += x_vel // 2
        self.y += y_vel // 4


def drawing(x, y, width, hight):
    pg.draw.rect(window, (255, 0, 0), pg.Rect(x, y, width, hight))


wait = False
H = 50
W = 25
hero = Player(750, 300, W, H)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()

    keys = pg.key.get_pressed()
    if keys[pg.K_w] and not wait and hero.y > 150:
        if hero.y > 250:
            hero.y_vel -= 20 - abs(hero.y_vel // 4)
        else:
            hero.y_vel += 8
    elif hero.y < window_height - H:
        if hero.y_vel >= 0:
            hero.y_vel += (0.1 * hero.y_vel) // 1 + 1
        else:
            hero.y_vel += abs(hero.y_vel // 2) + 10
        wait = True
    else:
        hero.y_vel = 0
        hero.y = window_height - H
        wait = False

    if keys[pg.K_a]:
        if hero.x < 0:
            hero.x = 0
            hero.x_vel = 0
        else:
            if hero.x_vel > 0:
                hero.x_vel -= (hero.x_vel // 2) + 1
            elif hero.x_vel > -40:
                hero.x_vel -= (abs(0.25 * hero.x_vel)) // 1 + 1
    elif keys[pg.K_d]:
        if hero.x > window_width - W:
            hero.x = window_width - W
            hero.x_vel = 0
        else:
            if hero.x_vel < 0:
                hero.x_vel -= (hero.x_vel // 2) - 1
            elif hero.x_vel < 40:
                hero.x_vel += (0.25 * hero.x_vel) // 1 + 1
    elif hero.x_vel > 0:
        hero.x_vel -= (hero.x_vel // 2) + 1
    elif hero.x_vel < 0:
        hero.x_vel -= (hero.x_vel // 2) - 1

    window.fill((100, 100, 100))
    hero.movement(hero.x_vel, hero.y_vel)
    drawing(hero.x, hero.y, hero.size[0], hero.size[1])
    pg.display.update()
    fps.tick(60)
