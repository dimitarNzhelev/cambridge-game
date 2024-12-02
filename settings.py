import pygame

# Game settings
WINDOW_SIZE = (1200, 800)
DISPLAY_SIZE = (300, 200)
CHUNK_SIZE = 8

# Initialize Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

# Set up display
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface(DISPLAY_SIZE)
pygame.display.set_caption('Pygame Platformer')

# Clock
clock = pygame.time.Clock()