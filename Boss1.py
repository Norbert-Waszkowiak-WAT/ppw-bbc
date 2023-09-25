import pygame as pg
import os

pg.init()
window = pg.display.set_mode((1280, 720))

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.body = pg.image.load(os.path.join('pliki', 'player.png'))
        self.width = 80
        self.height = 150
        self.body = pg.transform.scale(self.body, (self.width, self.height))
        self.speed = 7
        self.hitbox = pg.Rect(self.x, self.y, self.width, self.height)

    def move(self, key_pressed):
        if key_pressed[pg.K_a]:
            self.x -= self.speed
        if key_pressed[pg.K_d]:
            self.x += self.speed
        if key_pressed[pg.K_w]:
            self.y -= self.speed
        if key_pressed[pg.K_s]:
            self.y += self.speed

        self.hitbox = pg.Rect(self.x, self.y, self.width, self.height)
        Player.draw(self)

    def draw(self):
        window.blit(self.body, (self.x, self.y))

def main():
    clock = pg.time.Clock()
    run = True
    player = Player()
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        key_pressed = pg.key.get_pressed()
        window.fill((255, 255, 255))
        player.move(key_pressed)
        clock.tick(60)
        pg.display.update()



main()