import random

class FallingObject:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = random.uniform(2, 5)

    def update(self):
        self.y += self.speed
        self.rect.y = int(self.y)

    def render(self, display, scroll):
        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)