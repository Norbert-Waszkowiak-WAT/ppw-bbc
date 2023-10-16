import pygame as pg
import time
import random

pg.init()

print("Podaj wielkość jednego pixela: ", end="")
pixel = 25  # int(input())
snake_speed = 250 // pixel
window_width = 1250
window_height = 750
knockdown = 0

pg.display.set_caption('Snake')
window = pg.display.set_mode((window_width, window_height))
fps = pg.time.Clock()

bot_position = [50 * pixel, 350]
snake_position = [4 * pixel, 350]

bot_body = [[50 * pixel, 350],
            [51 * pixel, 350],
            [52 * pixel, 350],
            [53 * pixel, 350]]
snake_body = [[4 * pixel, 350],
              [3 * pixel, 350],
              [2 * pixel, 350],
              [1 * pixel, 350]]

fruit_position = [random.randrange(0, (window_width // pixel)) * pixel,
                  random.randrange(0, (window_height // pixel)) * pixel]
fruit_spawn = True

bot_direction = 'L'
bot_change_to = bot_direction
direction = 'RIGHT'
change_to = direction
score = 0


def count_around_me(x, y, d):
    wall = ''
    if (snake_body.count([x, y - pixel]) == 1 or bot_body.count([x, y - pixel]) == 1 or y - pixel < 0) and d != 'D':
        wall += 'U'
    if (snake_body.count([x, y + pixel]) == 1 or bot_body.count([x, y + pixel]) == 1 or y + pixel == window_height) and d != 'U':
        wall += 'D'
    if (snake_body.count([x - pixel, y]) == 1 or bot_body.count([x - pixel, y]) == 1 or x - pixel < 0) and d != 'R':
        wall += 'L'
    if (snake_body.count([x + pixel, y]) == 1 or bot_body.count([x + pixel, y]) == 1 or x + pixel == window_width) and d != 'L':
        wall += 'R'
    return wall


def show_score(color, font, size):
    score_font = pg.font.SysFont(font, size)
    score_surface = score_font.render('Punkty: ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    window.blit(score_surface, score_rect)


def game_over():
    my_font = pg.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render(
        'Zdobyłeś ' + str(score) + ' punktów!!!', True, (255, 0, 0))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_width / 2, window_height / 4)

    window.blit(game_over_surface, game_over_rect)
    pg.display.flip()

    time.sleep(2)

    pg.quit()
    quit()


def victory():
    my_font = pg.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render(
        'Wygrałeś!!!', True, (255, 255, 0))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_width / 2, window_height / 4)

    window.blit(game_over_surface, game_over_rect)
    pg.display.flip()

    time.sleep(5)

    pg.quit()
    quit()


while True:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                change_to = 'UP'
            if event.key == pg.K_s:
                change_to = 'DOWN'
            if event.key == pg.K_a:
                change_to = 'LEFT'
            if event.key == pg.K_d:
                change_to = 'RIGHT'
        if event.type == pg.QUIT:
            quit()

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_position[1] -= pixel
    if direction == 'DOWN':
        snake_position[1] += pixel
    if direction == 'LEFT':
        snake_position[0] -= pixel
    if direction == 'RIGHT':
        snake_position[0] += pixel

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 1
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_width // pixel)) * pixel,
                          random.randrange(1, (window_height // pixel)) * pixel]

    fruit_spawn = True
    window.fill((0, 0, 0))

    pg.draw.rect(window, (0, 255, 0),
                 pg.Rect(snake_body[0][0], snake_body[0][1], pixel, pixel))
    color = 255
    for pos in snake_body[1:]:
        color -= 200 // len(snake_body)
        pg.draw.rect(window, (0, color, 0), pg.Rect(pos[0], pos[1], pixel, pixel))

    if bot_direction == 'x':
        pg.draw.rect(window, (255, 0, 255),
                     pg.Rect(bot_body[0][0], bot_body[0][1], pixel, pixel))
        color = 255
        for pos in bot_body[1:]:
            color -= 200 // len(bot_body)
            pg.draw.rect(window, (255, 0, color), pg.Rect(pos[0], pos[1], pixel, pixel))
    else:
        pg.draw.rect(window, (255, 0, 0),
                     pg.Rect(bot_body[0][0], bot_body[0][1], pixel, pixel))
        color = 255
        for pos in bot_body[1:]:
            color -= 200 // len(bot_body)
            pg.draw.rect(window, (color, 0, 0), pg.Rect(pos[0], pos[1], pixel, pixel))

    pg.draw.rect(window, (255, 255, 0), pg.Rect(
        fruit_position[0], fruit_position[1], pixel, pixel))

    if snake_position[0] < 0 or snake_position[0] > window_width - pixel:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_height - pixel:
        game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    ###################################################################

    if count_around_me(bot_position[0], bot_position[1], bot_direction) != '':
        warning = count_around_me(bot_position[0], bot_position[1], bot_direction)
        if len(warning) == 3:
            if bot_direction != 'x':
                knockdown += 1
            bot_change_to = 'x'
            bot_direction = 'x'
        elif warning.count('U') != 1 and bot_direction != 'D':
            if warning.count('D') != 1 and bot_direction != 'U' and fruit_position[1] > bot_position[1]:
                bot_change_to = 'D'
            else:
                bot_change_to = 'U'
        elif warning.count('D') != 1 and bot_direction != 'U':
            bot_change_to = 'D'
        elif warning.count('R') != 1 and bot_direction != 'L':
            bot_change_to = 'R'
        elif warning.count('L') != 1 and bot_direction != 'R':
            bot_change_to = 'L'
    elif fruit_position[0] > bot_position[0]:
        if bot_direction != 'L':
            bot_change_to = 'R'
        else:
            if fruit_position[1] > bot_position[1]:
                bot_change_to = 'D'
            else:
                bot_change_to = 'U'
    elif fruit_position[0] < bot_position[0]:
        if bot_direction != 'R':
            bot_change_to = 'L'
        else:
            if fruit_position[1] > bot_position[1]:
                bot_change_to = 'D'
            else:
                bot_change_to = 'U'
    elif fruit_position[1] < bot_position[1]:
        if bot_direction != 'D':
            bot_change_to = 'U'
        else:
            if fruit_position[0] > bot_position[0]:
                bot_change_to = 'R'
            else:
                bot_change_to = 'L'
    elif fruit_position[1] > bot_position[1]:
        if bot_direction != 'U':
            bot_change_to = 'D'
        else:
            if fruit_position[0] > bot_position[0]:
                bot_change_to = 'R'
            else:
                bot_change_to = 'L'

    if bot_change_to == 'U' and bot_direction != 'D':
        bot_direction = 'U'
    if bot_change_to == 'D' and bot_direction != 'U':
        bot_direction = 'D'
    if bot_change_to == 'L' and bot_direction != 'R':
        bot_direction = 'L'
    if bot_change_to == 'R' and bot_direction != 'L':
        bot_direction = 'R'

    if bot_direction == 'U':
        bot_position[1] -= pixel
    if bot_direction == 'D':
        bot_position[1] += pixel
    if bot_direction == 'L':
        bot_position[0] -= pixel
    if bot_direction == 'R':
        bot_position[0] += pixel

    bot_body.insert(0, list(bot_position))
    if bot_position[0] == fruit_position[0] and bot_position[1] == fruit_position[1]:
        fruit_spawn = False
    else:
        bot_body.pop()

    for block in bot_body:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score((255, 255, 255), 'times new roman', 30)
    pg.display.update()
    if knockdown > 2:
        victory()
    fps.tick(snake_speed)
