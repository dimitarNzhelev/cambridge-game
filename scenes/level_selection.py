import pygame
import sys
import json
from settings import screen
from utils.components.ui.button import Button
from utils.components.resource_loader import ResourceLoader
from utils.components.ui.dialog_window import DialogWindow

class LevelSelectionScene:
    def __init__(self, scores):
        self.scores = scores
        self.loader = ResourceLoader.get_instance()
        self.background = self.loader.get_image("data/images/home/map.png")
        self.background = pygame.transform.scale(self.background, screen.get_size())
        self.font_path = "data/images/home/font.ttf"
        self.levels = self.load_levels("levels.json")
        self.dialog_window = None
        self.selected_level = None

    def load_levels(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def get_font(self, size):
        return self.loader.get_font(self.font_path, size)

    def create_text(self, text, size, color, center_position):
        text_surface = self.get_font(size).render(text, True, color)
        text_rect = text_surface.get_rect(center=center_position)
        return text_surface, text_rect

    def calculate_position_and_size(self, level):
        screen_width, screen_height = screen.get_size()
        position = (int(level["position"][0] * screen_width / 800), int(level["position"][1] * screen_height / 600))
        size = (int(level["size"][0] * screen_width / 800), int(level["size"][1] * screen_height / 600))
        return position, size

    def run(self):
        while True:
            screen.blit(self.background, (0, 0))
            menu_mouse_pos = pygame.mouse.get_pos()

            title1_surf, title1_rect = self.create_text(
                "Select", screen.get_size()[1]//10, "#ced4da", (screen.get_size()[0]//2, screen.get_size()[1]//2 - screen.get_size()[1]//10)
            )
            title2_surf, title2_rect = self.create_text(
                "Level", screen.get_size()[1]//10, "#ced4da", (screen.get_size()[0]//2, screen.get_size()[1]//2)
            )

            screen.blit(title1_surf, title1_rect)
            screen.blit(title2_surf, title2_rect)

            for level in self.levels:
                position, size = self.calculate_position_and_size(level)
                level_surface = pygame.Surface(size, pygame.SRCALPHA)
                level_rect = pygame.Rect(position, size)
                if level_rect.collidepoint(menu_mouse_pos):
                    level_surface.fill((255, 255, 255, 50))  # Slightly lighter on hover
                else:
                    level_surface.fill((255, 255, 255, 0))  # Fully transparent
                screen.blit(level_surface, position)

            if self.dialog_window:
                self.dialog_window.render(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.dialog_window and self.dialog_window.dialog_shown:
                        self.dialog_window.set_dialog_shown(False)
                        self.dialog_window = None
                    elif event.key == pygame.K_ESCAPE and not self.dialog_window:
                        return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.dialog_window and self.dialog_window.check_play_button(menu_mouse_pos):
                        return f"level{self.selected_level}"
                    i = 0
                    for level in self.levels:
                        position, size = self.calculate_position_and_size(level)
                        level_rect = pygame.Rect(position, size)
                        if level_rect.collidepoint(menu_mouse_pos):
                            self.selected_level = self.levels.index(level) + 1
                            highest_score = self.scores.get(self.levels.index(level) + 1, 0)
                            self.dialog_window = DialogWindow(
                                font_path=None,
                                text=f"{level['name']}\n\n{level['description']}\n\nHighest Score: {highest_score} / 5",
                                width=screen.get_size()[0]//2,
                                height=screen.get_size()[1]//2,
                                font_size=screen.get_size()[1]//20,
                                show_play_button=True  # Enable play button
                            )
                        i += 1

            pygame.display.update()
