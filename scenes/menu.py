# scenes/menu.py
import pygame
import sys
from settings import screen
from utils.components.ui.button import Button
from utils.components.resource_loader import ResourceLoader

class MenuScene:
    def __init__(self):
        self.loader = ResourceLoader.get_instance()
        self.background = self.loader.get_image("data/images/home/Background.png")
        self.background = pygame.transform.scale(self.background, screen.get_size())
        
        # Cache font
        self.font_path = "data/images/home/font.ttf"
        
    def get_font(self, size):
        return self.loader.get_font(self.font_path, size)
    
    def create_text(self, text, size, color, center_position):
        text_surface = self.get_font(size).render(text, True, color)
        text_rect = text_surface.get_rect(center=center_position)
        return text_surface, text_rect

    def create_button_surface(self, size, color, alpha):
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((*color, alpha))
        return surface
    
    def run(self):
        while True:
            screen.blit(self.background, (0, 0))
            menu_mouse_pos = pygame.mouse.get_pos()

            # Create title text
            title1_surf, title1_rect = self.create_text(
                "Cambridge", screen.get_size()[1]//10, "#b68f40", (screen.get_size()[0]//2, screen.get_size()[1]//2 - screen.get_size()[1]//10)
            )
            title2_surf, title2_rect = self.create_text(
                "Gamble", screen.get_size()[1]//10, "#b68f40", (screen.get_size()[0]//2, screen.get_size()[1]//2)
            )

            # Create buttons
            button_size = (screen.get_size()[0]//3, screen.get_size()[1]//15)
            play_button_surface = self.create_button_surface(button_size, (255, 255, 255), 50)
            credits_button_surface = self.create_button_surface(button_size, (255, 255, 255), 50)
            quit_button_surface = self.create_button_surface(button_size, (255, 255, 255), 50)

            play_button = Button(
                image=play_button_surface,
                pos=(screen.get_size()[0]//2, screen.get_size()[1]//2 + screen.get_size()[1]//10),
                text_input="PLAY",
                font=self.get_font(screen.get_size()[1]//20),
                base_color="#d7fcd4",
                hovering_color="White"
            )
            
            credits_button = Button(
                image=credits_button_surface,
                pos=(screen.get_size()[0]//2, screen.get_size()[1]//2 + 2 * screen.get_size()[1]//10),
                text_input="CREDITS",
                font=self.get_font(screen.get_size()[1]//20),
                base_color="#d7fcd4",
                hovering_color="White"
            )
            
            quit_button = Button(
                image=quit_button_surface,
                pos=(screen.get_size()[0]//2, screen.get_size()[1]//2 + 3 * screen.get_size()[1]//10),
                text_input="QUIT",
                font=self.get_font(screen.get_size()[1]//20),
                base_color="#d7fcd4",
                hovering_color="White"
            )

            # Draw elements
            screen.blit(title1_surf, title1_rect)
            screen.blit(title2_surf, title2_rect)

            for button in [play_button, credits_button, quit_button]:
                button.changeColor(menu_mouse_pos)
                button.update(screen)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(menu_mouse_pos):
                        return "level_selection"
                    if credits_button.checkForInput(menu_mouse_pos):
                        return "credits"
                    if quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()        

            pygame.display.update()
