import pygame
import math
import random
from numbers import *
from pygame.locals import *


class Spritesheet:

    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.blocks_to_remove = []

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = 64
        self.height = 64

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.hitbox = self.rect.inflate(0,-13)

        self.down_animations = [self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(64, 0, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(128, 0, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(192, 0, self.width, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(0, 192, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(64, 192, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(128, 192, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(192, 192, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(0, 64, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(64, 64, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(128, 64, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(192, 64, self.width, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(0, 128, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(64, 128, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(128, 128, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(192, 128, self.width, self.height)]

    def update(self):

        self.movement()

        self.rect.x += self.x_change
        self.collide_obstacles('x')
        self.rect.y += self.y_change
        self.collide_obstacles('y')

        #self.rect.center = self.hitbox.center


        self.animate()

        self.collide_boss_area('x')
        self.collide_boss_area('y')
        self.collide_enemy()

        self.x_change = 0
        self.y_change = 0

    def attack(self):

        if self.facing == 'up':
            Attack(self.game, self.rect.x, self.rect.y - TILESIZE)
        if self.facing == 'down':
            Attack(self.game, self.rect.x, self.rect.y + TILESIZE)
        if self.facing == 'left':
            Attack(self.game, self.rect.x - TILESIZE, self.rect.y)
        if self.facing == 'right':
            Attack(self.game, self.rect.x + TILESIZE, self.rect.y)

    def collide_chest(self):
        for chest in self.game.chests:
            if self.rect.colliderect(chest.hitbox):
                a = [chest, chest.k]
                return a
    def chest(self):
        if self.collide_chest() is not None:
            k = self.collide_chest()[1]
            chest = self.collide_chest()[0]
            if k == 1:
                chest.state = 1
                return True
        return False

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

    def collide_enemy(self):

        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def collide_obstacles(self, direction):

        for block in self.game.blocks:
            if block.rect.colliderect(self.rect):
                if self.rect.bottom < block.rect.bottom:
                    block.image.set_alpha(128)
                    self.game.faded_sprites.append(block)
                    if self.game.all_sprites.get_layer_of_sprite(self) > self.game.all_sprites.get_layer_of_sprite(
                            block):
                        self.game.all_sprites.switch_layer(BLOCK_LAYER, PLAYER_LAYER)
                elif self.rect.bottom > block.rect.bottom:
                    if self.game.all_sprites.get_layer_of_sprite(self) < self.game.all_sprites.get_layer_of_sprite(
                            block):
                        self.game.all_sprites.switch_layer(BLOCK_LAYER, PLAYER_LAYER)

                if block.hitbox.colliderect(self.rect):
                    if direction == 'x':
                        if self.x_change > 0:
                            self.rect.right = block.hitbox.left
                        if self.x_change < 0:
                            self.rect.left = block.hitbox.right
                    elif direction == 'y':
                        if self.y_change > 0:
                            self.rect.bottom = block.hitbox.top
                        if self.y_change < 0:
                            self.rect.top = block.hitbox.bottom
        for door in self.game.doors:
            if door.rect.colliderect(self.rect):

                if door.hitbox.colliderect(self.rect):
                    if direction == 'x':
                        if self.x_change > 0:
                            self.rect.right = door.hitbox.left
                        if self.x_change < 0:
                            self.rect.left = door.hitbox.right
                    elif direction == 'y':
                        if self.y_change > 0:
                            self.rect.bottom = door.hitbox.top
                        if self.y_change < 0:
                            self.rect.top = door.hitbox.bottom

        for block in self.game.faded_sprites:
            if not block.rect.colliderect(self.rect):
                block.image.set_alpha(255)
                self.blocks_to_remove.append(block)

        for block in self.blocks_to_remove:
            if block in self.game.faded_sprites:
                self.game.faded_sprites.remove(block)
        self.blocks_to_remove.clear()







    def collide_boss_area(self, direction):

        hits = pygame.sprite.spritecollide(self, self.game.bosses, False)
        for boss in hits:

            if direction == 'x':

                if self.x_change > 0:

                    if boss.which_game == "cup_game":
                        self.game.game_state = "cup_game"

                    elif self.game.tokens == 0:
                        self.game.no_tokens()

                    else:
                        self.game.tokens -= 1
                        if boss.which_game == "snake_game":
                            self.game.game_state = "snake_game"
                        elif boss.which_game == "small_game":
                            self.game.game_state = "small_game"
                        elif boss.which_game == "shooter_game":
                            self.game.game_state = "shooter_game"
                        elif boss.which_game == "jetpack_game":
                            self.game.game_state = "jetpack_game"

                    self.rect.right = boss.rect.left - TILESIZE

                if self.x_change < 0:

                    if boss.which_game == "cup_game":
                        self.game.game_state = "cup_game"

                    elif self.game.tokens == 0:
                        self.game.no_tokens()

                    else:
                        self.game.tokens -= 1
                        if boss.which_game == "snake_game":
                            self.game.game_state = "snake_game"
                        elif boss.which_game == "small_game":
                            self.game.game_state = "small_game"
                        elif boss.which_game == "shooter_game":
                            self.game.game_state = "shooter_game"
                        elif boss.which_game == "jetpack_game":
                            self.game.game_state = "jetpack_game"
                    self.rect.left = boss.rect.right + TILESIZE

            if direction == 'y':

                if self.y_change > 0:

                    if boss.which_game == "cup_game":
                        self.game.game_state = "cup_game"

                    elif self.game.tokens == 0:
                        self.game.no_tokens()

                    else:
                        self.game.tokens -= 1
                        if boss.which_game == "snake_game":
                            self.game.game_state = "snake_game"
                        elif boss.which_game == "small_game":
                            self.game.game_state = "small_game"
                        elif boss.which_game == "shooter_game":
                            self.game.game_state = "shooter_game"
                        elif boss.which_game == "jetpack_game":
                            self.game.game_state = "jetpack_game"
                    self.rect.bottom = boss.rect.top - TILESIZE

                if self.y_change < 0:

                    if boss.which_game == "cup_game":
                        self.game.game_state = "cup_game"

                    elif self.game.tokens == 0:
                        self.game.no_tokens()

                    else:
                        self.game.tokens -= 1
                        if boss.which_game == "snake_game":
                            self.game.game_state = "snake_game"
                        elif boss.which_game == "small_game":
                            self.game.game_state = "small_game"
                        elif boss.which_game == "shooter_game":
                            self.game.game_state = "shooter_game"
                        elif boss.which_game == "jetpack_game":
                            self.game.game_state = "jetpack_game"
                    self.rect.top = boss.rect.bottom + TILESIZE

    def animate(self):

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.right_animations[0]
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

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

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
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(416, 672, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.hitbox = self.rect.inflate(0, -45)


class River(pygame.sprite.Sprite):
    def __init__(self, game, x, y, initial_frame):
        self.game = game
        self._layer = RIVER_LAYER
        self.groups = self.game.all_sprites, self.game.rivers
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.frame_index = initial_frame
        self.animation_loop = 0

        self.frames = []
        for i in range(3):
            self.frames.append(
                self.game.terrain_spritesheet.get_sprite(864 + i * TILESIZE, 160, self.width, self.height))

        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()

    def animate(self):
        self.animation_loop += 0.35

        if self.animation_loop >= 3:
            self.frame_index = (self.frame_index + 1) % 3
            self.image = self.frames[self.frame_index]
            self.animation_loop = 0


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
        self.i = random.randint(0, 2)
        self.image = self.game.terrain_spritesheet.get_sprite(TILESIZE * self.i, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Bridge(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.bridges
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * 2
        self.height = TILESIZE
        self.image = self.game.terrain_spritesheet.get_sprite(448, 576, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.hitbox = self.rect.inflate(10, 0)


class Attack(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER

        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.animation_loop = 0
        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        for enemy in self.game.enemies:
            if enemy.rect.colliderect(self.rect):
                enemy.kill()
    def animate(self):
        direction = self.game.player.facing

        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self, game, x, y, which_game, score):
        self.game = game
        self._layer = BOSS_LAYER
        self.groups = self.game.all_sprites, self.game.bosses
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.which_game = which_game
        self.score = score

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        if which_game == 'snake_game':
            self.image = self.game.terrain_spritesheet.get_sprite(560, 704, self.width, self.height * 1.5)
        elif which_game == 'small_game':
            self.image = self.game.terrain_spritesheet.get_sprite(624, 704, self.width, self.height * 1.5)
        elif which_game == "shooter_game":
            self.image = self.game.terrain_spritesheet.get_sprite(496, 704, self.width, self.height * 1.5)
        elif which_game == "jetpack_game":
            self.image = self.game.terrain_spritesheet.get_sprite(688, 704, self.width, self.height * 1.5)
        elif which_game == "cup_game":
            self.image = self.game.terrain_spritesheet.get_sprite(208, 864, 224, 144)



        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y




class Text:
    def __init__(self, game, text):

        self.game = game
        self.text = text
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.snip = self.font.render('', True, 'white')
        self.counter = 0
        self.speed = 50
        self.done = False
        self.active_message = 0
        self.message = text[self.active_message]

    def write(self):

        if self.counter < self.speed * len(self.message):
            self.counter += 1
        elif self.counter >= self.speed * len(self.message):
            self.done = True

        pygame.draw.rect(self.game.screen, BLACK, (0, WIN_HEIGHT - TEXT_HEIGHT, TEXT_WIDTH, TEXT_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.done and self.active_message < len(self.text) - 1:
                    self.active_message += 1
                    self.done = False
                    self.message = self.text[self.active_message]
                    self.counter = 0
                elif event.key == pygame.K_RETURN and self.done and self.active_message == len(self.text) - 1:
                    self.game.dialouge = False
        if not self.done:
            self.snip = self.font.render(self.message[0:self.counter // self.speed], True, 'white')
        self.game.screen.blit(self.snip, (10, WIN_HEIGHT - TEXT_HEIGHT))

class Door(pygame.sprite.Sprite):

    def __init__(self, game, x, y, health):
        self.game = game
        self._layer = DOOR_LAYER
        self.groups = self.game.all_sprites, self.game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE * 2
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(128, 768, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.health = health
        self.hitbox = self.rect.inflate(0,-45)
class Button(pygame.sprite.Sprite):
    def __init__(self,game, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.game = game
        self._layer = 7
        self.groups = self.game.all_sprites, self.game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Tree(pygame.sprite.Sprite):

    def __init__(self, game, x, y, size):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        if size == 1:
            self.x = x * TILESIZE
            self.y = y * TILESIZE
            self.width = TILESIZE * 2
            self.height = TILESIZE * 2

            self.image = self.game.terrain_spritesheet.get_sprite(544, 576, self.width, self.height)

            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

            self.hitbox = self.rect.inflate(-15,-30)

        if size == 2:
            self.x = x * TILESIZE
            self.y = y * TILESIZE
            self.width = TILESIZE * 4
            self.height = TILESIZE * 3.5

            self.image = self.game.terrain_spritesheet.get_sprite(224, 672, self.width, self.height)

            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

            self.hitbox = self.rect.inflate(-80, -30)

class Chest(pygame.sprite.Sprite):

    def __init__(self, game, x, y, k, state):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.chests
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.k = k

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE * 1.5

        self.image = self.game.terrain_spritesheet.get_sprite(448, 608, self.width, self.height)

        self.state = state

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.hitbox = self.rect.inflate(48 ,32)

    def update(self):

        if self.state == 0:
            self.image = self.game.terrain_spritesheet.get_sprite(448, 608, self.width, self.height)
        elif self.state == 1:
            self.image = self.game.terrain_spritesheet.get_sprite(480, 608, self.width, self.height)
            Weapon(self.game, self.x, self.y)
            self.game.looting(self.k)
        elif self.state == 2:
            self.kill()

class Weapon(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = 0
        self.groups = self.game.all_sprites, self.game.weapons
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game.all_sprites.move_to_front(self)

        self.x = x
        self.y = y
        self.width = TILESIZE * 2
        self.height = TILESIZE * 2

        self.image = self.game.terrain_spritesheet.get_sprite(608, 576, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.scaled_image = self.image.copy()

    def scale_image(self, scale_factor):
        #"""
        new_width = int(self.rect.width * scale_factor)
        new_height = int(self.rect.height * scale_factor)
        self.scaled_image = pygame.transform.smoothscale(self.image, (new_width, new_height))
        #"""

        """
        self.scaled_image = pygame.transform.scale(self.image, (
            int(self.rect.width * scale_factor),
            int(self.rect.height * scale_factor)
        
        ))
        """
class Floor(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.grounds
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        if type == 'w':
            self.image = self.game.terrain_spritesheet.get_sprite(352, 672, self.width, self.height)
        elif type == 'b' or type == 'P' or type == 'c':
            self.image = self.game.terrain_spritesheet.get_sprite(416, 736, self.width, self.height)
        elif type == 'z' or type == 'S' or type == 'd':
            self.image = self.game.terrain_spritesheet.get_sprite(352, 736, self.width, self.height)
        elif type == 'x' or type == 's':
            self.image = self.game.terrain_spritesheet.get_sprite(352, 800, self.width, self.height)
        else:
            self.image = self.game.terrain_spritesheet.get_sprite(352, 672, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class White(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.grounds
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(416, 800, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


