import pygame
from entries.entity import Entity

class Enemy:
    def __init__(self, x, y):
        self.entity = Entity(x, y, 40, 13, 'enemy')  # Increase the size of the entity

    def render(self, display, scroll):
        """Render the enemy on the display."""
        self.entity.display(display, scroll, center_image=True)