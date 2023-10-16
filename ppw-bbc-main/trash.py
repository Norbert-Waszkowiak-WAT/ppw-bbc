import pygame
from pygame.sprite import Sprite, LayeredUpdates

pygame.init()

# Tworzenie grupy sprite'ów LayeredUpdates
all_sprites = LayeredUpdates()

# Tworzenie kilku sprite'ów z różnymi warstwami
sprite1 = Sprite()
sprite1.image = pygame.Surface((50, 50))
sprite1.image.fill((255, 0, 0))
sprite1.rect = sprite1.image.get_rect()
sprite1.rect.center = (100, 100)
sprite1.layer = 1

sprite2 = Sprite()
sprite2.image = pygame.Surface((50, 50))
sprite2.image.fill((0, 255, 0))
sprite2.rect = sprite2.image.get_rect()
sprite2.rect.center = (150, 150)
sprite2.layer = 2

# Dodawanie sprite'ów do grupy
all_sprites.add(sprite1)
all_sprites.add(sprite2)

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Aktualizacja i renderowanie sprite'ów
    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()