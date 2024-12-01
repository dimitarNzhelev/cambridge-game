import pygame, sys
from pygame.locals import *
from settings import WINDOW_SIZE, DISPLAY_SIZE, FPS
from map import draw_map
from player import Player

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface(DISPLAY_SIZE)

player = Player(50, 50)

while True:
    display.fill((146, 244, 255))

    tile_rects = draw_map(display)
    player.handle_movement(tile_rects)
    player.draw(display)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.moving_right = True
            if event.key == K_LEFT:
                player.moving_left = True
            if event.key == K_UP:
                if player.air_timer < 6:
                    player.y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player.moving_right = False
            if event.key == K_LEFT:
                player.moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(FPS)