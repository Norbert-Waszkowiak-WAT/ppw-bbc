import pygame
import math
import random
from numbers import *

class Spirtesheet:

    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):

        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def movement(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change = -PLAYER_SPEED
            self.facing = 'left'

        if keys[pygame.K_d]:
            self.x_change = PLAYER_SPEED
            self.facing = 'right'

        if keys[pygame.K_w]:
            self.y_change = -PLAYER_SPEED
            self.facing = 'up'

        if keys[pygame.K_s]:
            self.y_change = PLAYER_SPEED
            self.facing = 'down'

        self.rect.x += self.x_change
        self.collide_block('x')
        self.rect.y += self.y_change
        self.collide_block('y')
        self.animate()

        self.collide_block('x')
        self.collide_block('y')
        self.collide_enemy()

        self.x_change = 0
        self.y_change = 0



    def collide_enemy(self):

        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def collide_block(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        for block in hits:
            if direction == 'x':
                if self.x_change > 0:
                    self.rect.right = block.rect.left
                if self.x_change < 0:
                    self.rect.left = block.rect.right
            if direction == 'y':
                if self.y_change > 0:
                    self.rect.bottom = block.rect.top
                if self.y_change < 0:
                    self.rect.top = block.rect.bottom


    def animate(self):

        self.down_animations = [self.game.character_spritesheet.get_sprite(0, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(33, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(65, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(97, 1, self.width, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(1, 97, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(33, 97, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(65, 97, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(97, 97, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(1, 33, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(33, 33, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(65, 33, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(97, 33, self.width, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 65, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(33, 65, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(65, 65, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(97, 65, self.width, self.height)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 1, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 97, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 33, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 65, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

class Enemy(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):

        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):

        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

        if self.facing == 'up':
            self.y_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= self.max_travel:
                self.facing = 'down'

        if self.facing == 'down':
            self.y_change += ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= self.max_travel:
                self.facing = 'up'

    def animate(self):

        self.down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Block(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,  self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(992, 544, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        self.groups.add(self)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y