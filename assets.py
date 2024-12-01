import pygame

# Load assets
player_image = pygame.image.load('./images/player.png')
player_image.set_colorkey((255, 255, 255))

grass_image = pygame.image.load('./images/grass.png')
TILE_SIZE = grass_image.get_width()

dirt_image = pygame.image.load('./images/dirt.png')