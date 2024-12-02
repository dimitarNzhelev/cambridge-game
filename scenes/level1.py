import pygame, sys, time
from settings import screen, display, clock, DISPLAY_SIZE, WINDOW_SIZE
from utils.assets import load_assets
from utils.player import Player
from utils.world import load_tile_map
from utils.falling_object_manager import FallingObjectManager

class Level1Scene:
    def __init__(self):
        self.assets = load_assets()
        self.grass_sound_timer = 0
        self.player = Player(166, 600)
        self.true_scroll = [self.player.entity.x - DISPLAY_SIZE[0] // 2, 0]
        self.background_objects = [
            [0.25, [120, 10, 70, 400]],
            [0.25, [280, 30, 40, 400]],
            [0.5, [30, 40, 40, 400]],
            [0.5, [130, 90, 100, 400]],
            [0.5, [300, 80, 120, 400]]
        ]
        self.tile_map = load_tile_map('data/map1.txt')
        self.falling_object_manager = FallingObjectManager(self.assets['plant_img'], self.player, WINDOW_SIZE[1])
        self.font = pygame.font.Font(None, 36)  # Default font and size
        self.player.is_immune = False

    def run(self):
        while True:
            display.fill((146, 244, 255))  # clear screen by filling it with blue

            if self.grass_sound_timer > 0:
                self.grass_sound_timer -= 1

            # Update only the Y component of true_scroll
            self.true_scroll[1] += (self.player.entity.y - self.true_scroll[1] - 106) / 20

            scroll = self.true_scroll.copy()
            scroll[0] = int(self.true_scroll[0])  # Keep the X component constant
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

            # Create and update falling objects
            self.falling_object_manager.create_falling_object()
            self.falling_object_manager.update_and_render(display, scroll)

            # Check if player has reached the top of the 1s
            if self.player.entity.y < self.get_top_of_ones():
                print("Player is immune")
                self.player.is_immune = True
            else:
                self.player.is_immune = False

            # Check if player is dead
            if self.player.health <= 0:
                self.show_game_over()
                time.sleep(5)
                pygame.quit()
                sys.exit()
                
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
            self.render_health()
            pygame.display.update()
            clock.tick(60)

    def render_health(self):
        for i in range(self.player.health):
            screen.blit(pygame.image.load('data/images/heart.jpg'), (WINDOW_SIZE[0] - 60 * (i + 1), 10))

    def show_game_over(self):
        game_over_text = self.font.render("YOU LOST", True, (255, 0, 0))
        screen.blit(game_over_text, (WINDOW_SIZE[0] // 2 - 100, WINDOW_SIZE[1] // 2 - 50))
        pygame.display.update()

    def get_top_of_ones(self):
        for y, row in enumerate(self.tile_map):
            for x, tile in enumerate(row):
                if tile == 1:
                    return y * 16  # Assuming each tile is 16 pixels high
        return float('inf')  # Return a very high value if no 1s are found