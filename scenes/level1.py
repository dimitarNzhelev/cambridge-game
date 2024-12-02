import pygame, sys
from settings import screen, display, clock
from assets import load_assets
from player import Player
from world import load_tile_map

class Level1Scene:
    def __init__(self):
        self.assets = load_assets()
        self.grass_sound_timer = 0
        self.true_scroll = [0, 0]
        self.player = Player(152, 480)
        self.background_objects = [
            [0.25, [120, 10, 70, 400]],
            [0.25, [280, 30, 40, 400]],
            [0.5, [30, 40, 40, 400]],
            [0.5, [130, 90, 100, 400]],
            [0.5, [300, 80, 120, 400]]
        ]
        self.tile_map = load_tile_map('data/tile_map.txt')

    def run(self):
        while True:
            display.fill((146, 244, 255))  # clear screen by filling it with blue

            if self.grass_sound_timer > 0:
                self.grass_sound_timer -= 1

            self.true_scroll[0] += (self.player.entity.x - self.true_scroll[0] - 152) / 20
            self.true_scroll[1] += (self.player.entity.y - self.true_scroll[1] - 106) / 20

            scroll = self.true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
            for background_object in self.background_objects:
                obj_rect = pygame.Rect(
                    background_object[1][0] - scroll[0] * background_object[0],
                    background_object[1][1] - scroll[1] * background_object[0],
                    background_object[1][2], background_object[1][3]
                )
                if background_object[0] == 0.5:
                    pygame.draw.rect(display, (20, 170, 150), obj_rect)
                else:
                    pygame.draw.rect(display, (15, 76, 73), obj_rect)

            tile_rects = []
            for y, row in enumerate(self.tile_map):
                for x, tile in enumerate(row):
                    if tile != 0:
                        display.blit(self.assets['tile_index'][tile], (x * 16 - scroll[0], y * 16 - scroll[1]))
                        if tile in [1, 2]:
                            tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))

            self.player.update(tile_rects)
            self.player.render(display, scroll)

            for event in pygame.event.get():  # event loop
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if self.player.air_timer < 6:
                            self.assets['jump_sound'].play()
                            self.player.vertical_momentum = -5
                    if event.key == pygame.K_UP:
                        if self.player.air_timer < 6:
                            self.assets['jump_sound'].play()
                            self.player.vertical_momentum = -5
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.moving_right = True
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.moving_left = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.moving_right = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.moving_left = False

            screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    level1_scene = Level1Scene()
    level1_scene.run()