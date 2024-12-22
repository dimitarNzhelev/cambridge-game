import pygame
import sys
from settings import screen, display, clock

class CreditsScene:
    def __init__(self):
        self.font = pygame.font.Font(None, 20)
        self.credits = [
            {
                "name": "Ели",
                "credits": "реши всички задачки и ни събра",
                "image": None
            },
            {
                "name": "Емма",
                "credits": "направи егати готините рисунки",
                "image": None
            },
            {
                "name": "Митко",
                "credits": "накоди ти играта тъпако",
                "image": None
            },
        ]

    def run(self):
        while True:
            display.fill((0, 0, 0))  # Fill the screen with black
            y_offset = 50
            for entry in self.credits:
                name_surface = self.font.render(entry["name"], True, (255, 255, 255))
                credits_surface = self.font.render(entry["credits"], True, (255, 255, 255))
                display.blit(name_surface, (display.get_size()[0] // 2 - name_surface.get_width() // 2, y_offset))
                y_offset += 40
                display.blit(credits_surface, (display.get_size()[0] // 2 - credits_surface.get_width() // 2, y_offset))
                y_offset += 40

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
            
            screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
            pygame.display.update()
            clock.tick(60)