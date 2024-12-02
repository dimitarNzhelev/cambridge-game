import pygame, sys
from settings import screen, display, clock, CHUNK_SIZE
from assets import load_assets
from player import Player
from world import generate_chunk

def main():
    assets = load_assets()
    game_map = {}
    grass_sound_timer = 0
    true_scroll = [0, 0]

    player = Player(100, 100)

    background_objects = [
        [0.25, [120, 10, 70, 400]],
        [0.25, [280, 30, 40, 400]],
        [0.5, [30, 40, 40, 400]],
        [0.5, [130, 90, 100, 400]],
        [0.5, [300, 80, 120, 400]]
    ]

    while True:
        display.fill((146, 244, 255))  # clear screen by filling it with blue

        if grass_sound_timer > 0:
            grass_sound_timer -= 1

        true_scroll[0] += (player.entity.x - true_scroll[0] - 152) / 20
        true_scroll[1] += (player.entity.y - true_scroll[1] - 106) / 20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
        for background_object in background_objects:
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
        for y in range(3):
            for x in range(4):
                target_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * 16)))
                target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * 16)))
                target_chunk = str(target_x) + ';' + str(target_y)
                if target_chunk not in game_map:
                    game_map[target_chunk] = generate_chunk(target_x, target_y, CHUNK_SIZE)
                for tile in game_map[target_chunk]:
                    display.blit(assets['tile_index'][tile[1]], (tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1]))
                    if tile[1] in [1, 2]:
                        tile_rects.append(pygame.Rect(tile[0][0] * 16, tile[0][1] * 16, 16, 16))

        player.update(tile_rects)
        player.render(display, scroll)

        for event in pygame.event.get():  # event loop
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if player.air_timer < 6:
                        assets['jump_sound'].play()
                        player.vertical_momentum = -5
                if event.key == pygame.K_UP:
                    if player.air_timer < 6:
                        assets['jump_sound'].play()
                        player.vertical_momentum = -5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.moving_right = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.moving_left = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.moving_right = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.moving_left = False

        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()