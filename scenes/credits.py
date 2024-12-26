import pygame
import sys
from settings import screen, clock
from utils.components.resource_loader import ResourceLoader  # Remove display import

class CreditsScene:
    def __init__(self):
        self.loader = ResourceLoader.get_instance()
        self.background = self.loader.get_image("data/images/background.png")
        self.background = pygame.transform.scale(self.background, screen.get_size())
        self.font_path = "data/images/home/font.ttf"
        self.font = pygame.font.Font(self.font_path, screen.get_size()[1] // 24)
        self.font_small = pygame.font.Font(None, screen.get_size()[1] // 30)
        self.title_font = pygame.font.Font(self.font_path, screen.get_size()[1] // 10)
        
        self.credits = [
            {
                "name": "Ели",
                "credits": "реши всички задачки и ни събра",
                "image": "data/images/eli.jpg"
            },
            {
                "name": "Емма",
                "credits": "направи егати готините рисунки",
                "image": "data/images/mitko.jpg"
            },
            {
                "name": "Митко",
                "credits": "накоди ти играта тъпако",
                "image": "data/images/mitko.jpg"
            },
        ]
        

    def draw_rounded_rect(self, surface, color, rect, corner_radius):
        """ Draw a rectangle with rounded corners. """
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

    def draw_blurred_rect(self, surface, rect, blur_radius):
        """ Draw a blurred rectangle. """
        sub_surface = surface.subsurface(rect).copy()
        sub_surface = pygame.transform.smoothscale(sub_surface, (rect.width // blur_radius, rect.height // blur_radius))
        sub_surface = pygame.transform.smoothscale(sub_surface, (rect.width, rect.height))
        surface.blit(sub_surface, rect.topleft)

    def run(self):
        while True:
            screen.blit(self.background, (0, 0))
            y_offset = screen.get_size()[1] // 4
            card_width = screen.get_size()[0] // 4
            card_height = screen.get_size()[1] // 2
            x_offsets = [screen.get_size()[0] // 6, 3 * screen.get_size()[0] // 6, 5 * screen.get_size()[0] // 6]

            # Draw title
            title_surface = self.title_font.render("CREDITS", True, "#0077b6")
            screen.blit(title_surface, (screen.get_size()[0] // 2 - title_surface.get_width() // 2, screen.get_size()[1] // 10))

            for i, entry in enumerate(self.credits):
                card_rect = pygame.Rect(x_offsets[i] - card_width // 2, y_offset, card_width, card_height)
                self.draw_rounded_rect(screen, (255, 255, 255), card_rect, 20)  # Draw white border
                inner_rect = card_rect.inflate(-10, -10)  # Create inner rect for the image
                self.draw_rounded_rect(screen, (0, 0, 0), inner_rect, 20)  # Draw black background

                if entry["image"]:
                    image_surface = pygame.image.load(entry["image"]).convert_alpha()
                    image_surface = pygame.transform.scale(image_surface, (inner_rect.width, inner_rect.height))
                    screen.blit(image_surface, (inner_rect.x, inner_rect.y))

                # Draw blurred background for text
                text_background_rect = pygame.Rect(inner_rect.x, inner_rect.bottom - inner_rect.height // 5, inner_rect.width, inner_rect.height // 5)
                self.draw_blurred_rect(screen, text_background_rect, 30)

                name_surface = self.font.render(entry["name"], True, (255, 255, 255))
                credits_surface = self.font_small.render(entry["credits"], True, (255, 255, 255))
                screen.blit(name_surface, (inner_rect.centerx - name_surface.get_width() // 2, inner_rect.bottom - inner_rect.height // 6))
                screen.blit(credits_surface, (inner_rect.centerx - credits_surface.get_width() // 2, inner_rect.bottom - inner_rect.height // 12))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
            
            pygame.display.update()
            clock.tick(60)