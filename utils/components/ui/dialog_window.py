# utils/components/dialog_window.py
import pygame
from utils.components.resource_loader import ResourceLoader
from utils.components.ui.button import Button
from settings import screen

class DialogWindow:
    def __init__(self,font_path, text, width, height, font_size=36, show_play_button=False):
        self.font = pygame.font.Font(font_path if font_path else None, font_size)
        self.text = text
        self.width = width
        self.height = height
        self.position = (screen.get_size()[0] // 2 - self.width // 2, screen.get_size()[1] // 2 - self.height // 2)  # Center the dialog window
        self.loader = ResourceLoader.get_instance()
        self.background_image = self.loader.get_image("data/images/text_box.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.text_color = (255, 255, 255)
        self.padding = 50
        self.current_line_index = 0
        self.dialog_lines = []
        self.dialog_shown = True
        self.show_play_button = show_play_button
        self.image = None  # Add an attribute to store the image
        if self.show_play_button:
            self.play_button = Button(
                image=self.loader.get_image("data/images/home/Play Rect.png"),
                pos=(screen.get_size()[0] // 2, 2.5 * (screen.get_size()[1] // 4) ),
                text_input="PLAY",
                font=self.font,
                base_color="#d7fcd4",
                hovering_color="White"
            )

    def render(self, screen):
        if not self.dialog_shown:
            return  # Do not render if the dialog has been shown
        # Draw background
        dialog_rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        screen.blit(self.background_image, dialog_rect)

        if self.image:
            # Render image
            image_rect = self.image.get_rect(center=(self.position[0] + self.width // 2, self.position[1] + self.height // 5))
            screen.blit(self.image, image_rect)
        else:
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

        if self.show_play_button:
            self.play_button.update(screen)

    def render_text(self, screen, text, position, color):
        text_surface = self.font.render(text, True, color)
        screen.blit(text_surface, position)

    def set_text(self, text):
        self.text = text
        self.image = None  # Reset image when text is set

    def set_image(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()

        original_width, original_height = self.image.get_size()
        aspect_ratio = original_width / original_height

        if original_width > original_height:
            new_width = min(screen.get_size()[0] // 2, original_width)
            new_height = new_width / aspect_ratio
        else:
            new_height = min(screen.get_size()[1] // 2.5, original_height)
            new_width = new_height * aspect_ratio

        self.image = pygame.transform.scale(self.image, (int(new_width), int(new_height)))
        self.text = ""

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

    def check_play_button(self, position):
        if self.show_play_button:
            return self.play_button.checkForInput(position)
        return False
