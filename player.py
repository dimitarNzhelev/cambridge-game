import pygame
from assets import player_image
from utils import move

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, player_image.get_width(), player_image.get_height())
        self.moving_right = False
        self.moving_left = False
        self.y_momentum = 0
        self.air_timer = 0

    def handle_movement(self, tile_rects):
        movement = [0, 0]
        if self.moving_right:
            movement[0] += 2
        if self.moving_left:
            movement[0] -= 2
        movement[1] += self.y_momentum
        self.y_momentum += 0.2
        if self.y_momentum > 3:
            self.y_momentum = 3

        self.rect, collisions = move(self.rect, movement, tile_rects)

        if collisions['bottom']:
            self.y_momentum = 0
            self.air_timer = 0
        else:
            self.air_timer += 1

    def draw(self, display):
        display.blit(player_image, (self.rect.x, self.rect.y))