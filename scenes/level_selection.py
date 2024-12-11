# scenes/level_selection.py
import pygame
import sys
from settings import screen
from utils.components.ui.button import Button
from utils.components.resource_loader import ResourceLoader

class LevelSelectionScene:
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
    
    def run(self):
        while True:
            screen.blit(self.background, (0, 0))
            menu_mouse_pos = pygame.mouse.get_pos()

            # Create title text
            title1_surf, title1_rect = self.create_text(
                "Select", screen.get_size()[1]//10, "#b68f40", (screen.get_size()[0]//2, screen.get_size()[1]//2 - screen.get_size()[1]//10)
            )
            title2_surf, title2_rect = self.create_text(
                "Level", screen.get_size()[1]//10, "#b68f40", (screen.get_size()[0]//2, screen.get_size()[1]//2)
            )

            # Create buttons for levels
            buttons = []
            for i in range(1, 6):  # Assuming you have 5 levels
                button = Button(
                    image=self.loader.get_image("data/images/home/Play Rect.png"),
                    pos=(screen.get_size()[0]//2, screen.get_size()[1]//2 + (i * screen.get_size()[1]//10)),
                    text_input=f"LEVEL {i}",
                    font=self.get_font(screen.get_size()[1]//20),
                    base_color="#d7fcd4",
                    hovering_color="White"
                )
                buttons.append(button)
            
            back_button = Button(
                image=self.loader.get_image("data/images/home/Quit Rect.png"),
                pos=(screen.get_size()[0]//2, screen.get_size()[1]//2 + (6 * screen.get_size()[1]//10)),
                text_input="BACK",
                font=self.get_font(screen.get_size()[1]//20),
                base_color="#d7fcd4",
                hovering_color="White"
            )

            # Draw elements
            screen.blit(title1_surf, title1_rect)
            screen.blit(title2_surf, title2_rect)

            for button in buttons + [back_button]:
                button.changeColor(menu_mouse_pos)
                button.update(screen)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(buttons):
                        if button.checkForInput(menu_mouse_pos):
                            return f"level{i+1}"
                    if back_button.checkForInput(menu_mouse_pos):
                        return "menu"

            pygame.display.update()
