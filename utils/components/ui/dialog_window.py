# utils/components/dialog_window.py
import pygame
from settings import WINDOW_SIZE
from utils.components.resource_loader import ResourceLoader

class DialogWindow:
    def __init__(self, font_path, text, position, width, height, font_size=36):
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.loader = ResourceLoader.get_instance()
        self.background_image = self.loader.get_image("data/images/text_box.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.text_color = (255, 255, 255)
        self.padding = 50
        self.current_line_index = 0
        self.dialog_lines = []
        self.dialog_shown = True  # Add a flag to track if the dialog has been shown

    def render(self, screen):
        if not self.dialog_shown:
            return  # Do not render if the dialog has been shown
        # Draw background
        dialog_rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        screen.blit(self.background_image, dialog_rect)

        # Render text
        lines = self.text.split('\n')
        y_offset = self.position[1] + self.padding

        for line in lines:
            words = line.split(' ')
            current_line = []
            current_width = 0

            for word in words:
                word_surface = self.font.render(word, True, self.text_color)
                word_width = word_surface.get_width()
                if current_width + word_width + self.padding * 2 > self.width:
                    line_surface = self.font.render(' '.join(current_line), True, self.text_color)
                    x_offset = self.position[0] + (self.width - line_surface.get_width()) // 2
                    screen.blit(line_surface, (x_offset, y_offset))
                    y_offset += line_surface.get_height()
                    current_line = [word]
                    current_width = word_width
                else:
                    current_line.append(word)
                    current_width += word_width + self.font.size(' ')[0]

            line_surface = self.font.render(' '.join(current_line), True, self.text_color)
            x_offset = self.position[0] + (self.width - line_surface.get_width()) // 2
            screen.blit(line_surface, (x_offset, y_offset))
            y_offset += line_surface.get_height()

    def set_text(self, text):
        self.text = text

    def load_dialog(self, dialog_lines):
        self.dialog_lines = dialog_lines
        self.current_line_index = 0
        self.set_text(self.dialog_lines[self.current_line_index])

    def advance_dialog(self):
        if self.current_line_index < len(self.dialog_lines) - 1:
            self.current_line_index += 1
            self.set_text(self.dialog_lines[self.current_line_index])
        else:
            self.current_line_index = -1  # Indicate end of dialog

    def is_dialog_ended(self):
        return self.current_line_index == -1

    def set_dialog_shown(self, shown):
        self.dialog_shown = shown  # Method to set the dialog_shown flag