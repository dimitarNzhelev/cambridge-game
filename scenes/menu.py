# scenes/menu.py
import pygame
import sys
from settings import WINDOW_SIZE, screen
from utils.button import Button
from utils.resource_loader import ResourceLoader

class MenuScene:
    def __init__(self):
        self.loader = ResourceLoader.get_instance()
        self.background = self.loader.get_image("data/images/home/Background.png")
        self.background = pygame.transform.scale(self.background, WINDOW_SIZE)
        
        # Cache font
        self.font_path = "data/images/home/font.ttf"
        
    def get_font(self, size):
        return self.loader.get_font(self.font_path, size)
    
    def create_text(self, text, size, color, center_position):
        text_surface = self.get_font(size).render(text, True, color)
        text_rect = text_surface.get_rect(center=center_position)
        return text_surface, text_rect
    
    def run(self):
        while True:
            screen.blit(self.background, (0, 0))
            menu_mouse_pos = pygame.mouse.get_pos()

            # Create title text
            title1_surf, title1_rect = self.create_text(
                "Cambridge", 100, "#b68f40", (WINDOW_SIZE[0]//2, 100)
            )
            title2_surf, title2_rect = self.create_text(
                "Gamble", 100, "#b68f40", (WINDOW_SIZE[0]//2, 200)
            )

            # Create buttons
            play_button = Button(
                image=self.loader.get_image("data/images/home/Play Rect.png"),
                pos=(WINDOW_SIZE[0]//2, 350),
                text_input="PLAY",
                font=self.get_font(75),
                base_color="#d7fcd4",
                hovering_color="White"
            )
            
            quit_button = Button(
                image=self.loader.get_image("data/images/home/Quit Rect.png"),
                pos=(WINDOW_SIZE[0]//2, 550),
                text_input="QUIT",
                font=self.get_font(75),
                base_color="#d7fcd4",
                hovering_color="White"
            )

            # Draw elements
            screen.blit(title1_surf, title1_rect)
            screen.blit(title2_surf, title2_rect)

            for button in [play_button, quit_button]:
                button.changeColor(menu_mouse_pos)
                button.update(screen)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(menu_mouse_pos):
                        return "level1"
                    if quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
