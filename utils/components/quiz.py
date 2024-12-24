import pygame
from settings import screen
from utils.components.ui.dialog_window import DialogWindow

class Quiz:
    def __init__(self, questions, screen, dialog_window=None):
        self.questions = questions
        self.score = 0
        self.questions_index = 0
        self.showed_score = False
        self.screen = screen
        self.font_size = screen.get_size()[0] // 30  # Adjust font size based on screen width
        self.font = pygame.font.Font(None, self.font_size)
        self.dialog_window = dialog_window or DialogWindow("", "", screen.get_size()[0] - screen.get_size()[0]//10, screen.get_size()[1] - screen.get_size()[1]//10, screen.get_size()[0]//20)

    def get_current_question(self):
        return self.questions[self.questions_index]
    
    def check_answer(self, answer):
        if answer == self.get_current_question()["answer"]:
            self.score += 1
        self.questions_index += 1

    def is_finished(self):
        return self.questions_index == len(self.questions) and self.showed_score
    
    def is_finished_no_score(self):
        return self.questions_index == len(self.questions)
    
    def get_score(self):
        return self.score

    def reset(self):
        self.score = 0
        self.questions_index = 0
        self.showed_score = False

    def show_question(self):
        if self.is_finished_no_score():
            self.dialog_window.set_text(f"Quiz finished! Your score: {self.get_score()}")
            self.dialog_window.render(self.screen)
            self.showed_score = True
            pygame.display.update()
            pygame.time.delay(5000)  # Display the text for 5 seconds
            return True  # Indicate that the quiz is finished

        current_question = self.get_current_question()
        question_image_path = current_question["problem"]
        self.dialog_window.set_image(question_image_path)
        self.dialog_window.render(self.screen)
        self.show_answer_choices()
        self.show_score_and_progress()
        pygame.display.update()  # Ensure the screen is updated
        return False  # Indicate that the quiz is not finished yet

    def show_answer_choices(self):
        y_offset = screen.get_size()[1] // 2 + screen.get_size()[1] // 10  # Position a little below the half of the screen
        mouse_pos = pygame.mouse.get_pos()
        spacing = screen.get_size()[0] // 10  # Increase the spacing between answers
        rect_padding = screen.get_size()[0] // 80  # Add padding to make the rect bigger
        current_question = self.get_current_question()

        for i, choice in enumerate(current_question["answer_choices"]):
            choice_text = str(choice)
            x_offset = self.dialog_window.position[0] + (i * spacing) + (self.dialog_window.width - (len(current_question["answer_choices"]) - 1) * spacing) // 2
            choice_rect = pygame.Rect(x_offset - rect_padding, y_offset - rect_padding, self.font.size(choice_text)[0] + 2 * rect_padding, self.font.size(choice_text)[1] + 2 * rect_padding)
            if choice_rect.collidepoint(mouse_pos):
                self.dialog_window.render_text(self.screen, choice_text, (x_offset, y_offset), (255, 0, 0))
            else:
                self.dialog_window.render_text(self.screen, choice_text, (x_offset, y_offset), (255, 255, 255))

    def handle_mouse_click(self, mouse_pos):
        y_offset = screen.get_size()[1] // 2 + screen.get_size()[1] // 10  # Position a little below the half of the screen
        rect_padding = screen.get_size()[0] // 80  # Add padding to make the rect bigger
        current_question = self.get_current_question()

        for i, choice in enumerate(current_question["answer_choices"]):
            choice_text = str(choice)
            x_offset = self.dialog_window.position[0] + (i * screen.get_size()[0] // 10) + (self.dialog_window.width - (len(current_question["answer_choices"]) - 1) * screen.get_size()[0] // 10) // 2
            choice_rect = pygame.Rect(x_offset - rect_padding, y_offset - rect_padding, self.font.size(choice_text)[0] + 2 * rect_padding, self.font.size(choice_text)[1] + 2 * rect_padding)
            if choice_rect.collidepoint(mouse_pos):
                self.check_answer(choice)
                break

    def show_score_and_progress(self):
        score_font_size = screen.get_size()[0] // 30  # Adjust font size based on screen width
        score_font = pygame.font.Font(None, score_font_size)
        
        score_text = score_font.render(f"Score: {self.get_score()}", True, (255, 255, 255))
        progress_text = score_font.render(f"Question: {self.questions_index + 1}/{len(self.questions)}", True, (255, 255, 255))
        
        score_x = self.dialog_window.position[0] + self.dialog_window.width - score_text.get_width() - screen.get_size()[0] // 20
        score_y = self.dialog_window.position[1] + self.dialog_window.height - score_text.get_height() - screen.get_size()[0] // 20
        progress_x = self.dialog_window.position[0] + screen.get_size()[0] // 18
        progress_y = self.dialog_window.position[1] + self.dialog_window.height - progress_text.get_height() - screen.get_size()[0] // 20
        
        self.screen.blit(score_text, (score_x, score_y))
        self.screen.blit(progress_text, (progress_x, progress_y))