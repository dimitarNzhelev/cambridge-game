import pygame
from settings import WINDOW_SIZE
from utils.components.ui.dialog_window import DialogWindow

class Quiz:
    def __init__(self, questions, screen, dialog_window=None):
        self.questions = questions
        self.score = 0
        self.questions_index = 0
        self.showed_score = False
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.dialog_window = dialog_window or DialogWindow("", "", (50, 50), WINDOW_SIZE[0] - 100, WINDOW_SIZE[1] - 100, 64)

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

    def show_question(self):
        if self.is_finished_no_score():
            self.dialog_window.set_text(f"Quiz finished! Your score: {self.get_score()}")
            self.dialog_window.render(self.screen)
            self.showed_score = True
            pygame.display.update()
            return

        current_question = self.get_current_question()
        question_text = current_question["problem"]
        self.dialog_window.set_text(question_text)
        self.dialog_window.render(self.screen)
        self.show_answer_choices()
        self.show_score_and_progress()
        pygame.display.update()  # Ensure the screen is updated

    def show_answer_choices(self):
        answer_choices = self.get_current_question()["answer_choices"]
        y_offset = self.dialog_window.position[1] + self.dialog_window.padding + self.dialog_window.font.size(self.dialog_window.text)[1] + 20

        for i, choice in enumerate(answer_choices):
            choice_text = self.font.render(str(choice), True, (255, 255, 255))
            x_offset = self.dialog_window.position[0] + (self.dialog_window.width - choice_text.get_width()) // 2
            self.screen.blit(choice_text, (x_offset, y_offset + i * 30))

    def handle_mouse_click(self, mouse_pos):
        answer_choices = self.get_current_question()["answer_choices"]
        y_offset = self.dialog_window.position[1] + self.dialog_window.padding + self.dialog_window.font.size(self.dialog_window.text)[1] + 20

        for i, choice in enumerate(answer_choices):
            choice_text = self.font.render(str(choice), True, (255, 255, 255))
            x_offset = self.dialog_window.position[0] + (self.dialog_window.width - choice_text.get_width()) // 2
            choice_rect = pygame.Rect(x_offset, y_offset + i * 30, choice_text.get_width(), choice_text.get_height())
            if choice_rect.collidepoint(mouse_pos):
                self.check_answer(choice)
                break

    def show_score_and_progress(self):
        score_text = self.font.render(f"Score: {self.get_score()}", True, (255, 255, 255))
        progress_text = self.font.render(f"Question: {self.questions_index + 1}/{len(self.questions)}", True, (255, 255, 255))
        
        score_x = self.dialog_window.position[0] + self.dialog_window.width - score_text.get_width() - 50
        score_y = self.dialog_window.position[1] + self.dialog_window.height - score_text.get_height() - 50
        progress_x = self.dialog_window.position[0] + 30
        progress_y = self.dialog_window.position[1] + self.dialog_window.height - progress_text.get_height() - 50
        
        self.screen.blit(score_text, (score_x, score_y))
        self.screen.blit(progress_text, (progress_x, progress_y))