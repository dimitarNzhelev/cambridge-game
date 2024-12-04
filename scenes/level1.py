# scenes/level1.py
import pygame, sys, time
from settings import screen, display, clock, DISPLAY_SIZE, WINDOW_SIZE
from utils.assets import load_assets
from utils.components.player import Player
from utils.world import load_tile_map
from utils.components.falling_object_manager import FallingObjectManager
from utils.components.enemy import Enemy
from utils.components.ui.dialog_window import DialogWindow
from utils.math_problems import load_math_problems, get_random_problems
from utils.components.quiz import Quiz

class Level1Scene:
    def __init__(self):
        self.reset()

    def reset(self):
        self.assets = load_assets()
        self.grass_sound_timer = 0
        self.player = Player(166, 600)
        self.true_scroll = [self.player.entity.x - DISPLAY_SIZE[0] // 2, 0]
        self.background_objects = [
            [0.25, [120, 10, 70, 400]],
            [0.25, [280, 30, 40, 400]],
            [0.5, [30, 40, 40, 400]],
            [0.5, [130, 90, 100, 400]],
            [0.5, [300, 80, 120, 400]]
        ]
        self.tile_map = load_tile_map('data/map1.txt')
        self.falling_object_manager = FallingObjectManager(self.assets['plant_img'], self.player, WINDOW_SIZE[1])
        self.font = pygame.font.Font(None, 36)  # Default font and size
        self.enemy = Enemy(280, 147)  # Initialize the enemy with the new size
        self.conversation_active = False
        self.dialog_window = DialogWindow("", "", (50, 50), WINDOW_SIZE[0] - 100, WINDOW_SIZE[1] - 100, 64)
        self.load_dialog_from_file('data/enemies/level1.npc')
        self.math_problems = get_random_problems(load_math_problems(1), 2)
        self.current_problems = []
        self.current_problem_index = 0
        self.problem_solved = False
        self.quiz = Quiz(self.math_problems, screen)
        self.conversation_shown = False
        self.dialog_window.set_dialog_shown(True)  # Ensure the dialog is not shown initially

    def run(self):
        self.reset()
        while True:
            display.fill((146, 244, 255))  # clear screen by filling it with blue

            if self.grass_sound_timer > 0:
                self.grass_sound_timer -= 1

            # Update only the Y component of true_scroll
            self.true_scroll[1] += (self.player.entity.y - self.true_scroll[1] - 106) / 20

            scroll = self.true_scroll.copy()
            scroll[0] = int(self.true_scroll[0])  # Keep the X component constant
            scroll[1] = int(scroll[1])

            pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
            for background_object in self.background_objects:
                obj_rect = pygame.Rect(
                    background_object[1][0] - scroll[0] * background_object[0],
                    background_object[1][1] - scroll[1] * background_object[0],
                    background_object[1][2], background_object[1][3]
                )
                if background_object[0] == 0.5:
                    pygame.draw.rect(display, (20, 170, 150), obj_rect)
                else:
                    pygame.draw.rect(display, (15, 76, 73), obj_rect)

            tile_rects = []
            for y, row in enumerate(self.tile_map):
                for x, tile in enumerate(row):
                    if tile != 0:
                        display.blit(self.assets['tile_index'][tile], (x * 16 - scroll[0], y * 16 - scroll[1]))
                        if tile in [1, 2]:
                            tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))

            self.player.update(tile_rects)
            self.player.render(display, scroll)

            # Create and update falling objects
            self.falling_object_manager.create_falling_object()
            self.falling_object_manager.update_and_render(display, scroll)

            # Render the enemy
            self.enemy.render(display, scroll)

            # Check if player has reached the top of the 1s
            if self.player.entity.y < self.get_top_of_ones():
                self.player.is_immune = True
            else:
                self.player.is_immune = False

            # Check if player is dead
            if self.player.health <= 0:
                return self.show_game_over()

            for event in pygame.event.get():  # event loop
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if self.player.air_timer < 6:
                            # self.assets['jump_sound'].play()
                            self.player.vertical_momentum = -5
                    if event.key == pygame.K_UP:
                        if self.player.air_timer < 6:
                            # self.assets['jump_sound'].play()
                            self.player.vertical_momentum = -5
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.moving_right = True
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.moving_left = True
                    if event.key == pygame.K_RETURN and self.conversation_active:
                        self.dialog_window.advance_dialog()
                        if self.dialog_window.is_dialog_ended():
                            print("Conversation ended")
                            self.dialog_window.set_dialog_shown(False)
                            self.conversation_active = False
                            self.conversation_shown = True
                            self.current_problems = get_random_problems(self.math_problems)
                            self.current_problem_index = 0
                            self.problem_solved = False
                            self.quiz.show_question()
                            pygame.display.update()  # Ensure the screen is updated immediately
                    if event.key == pygame.K_RETURN and not self.conversation_active and not self.problem_solved:
                        if self.quiz.is_finished():
                            print("Quiz ended")
                            self.quiz.dialog_window.set_dialog_shown(False)
                            pygame.display.update()
                        else:
                            print("Quiz started")
                            self.check_answer()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.moving_right = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.moving_left = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.quiz and not self.quiz.is_finished():
                        self.quiz.handle_mouse_click(event.pos)
                    elif self.quiz and self.quiz.is_finished():
                        self.quiz.dialog_window.set_dialog_shown(False)
                        print("Removing the dialog window")
                        pygame.display.update()

            screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
            self.render_health()

            if not self.conversation_active and not self.problem_solved and self.conversation_shown and not self.quiz.is_finished():
                self.quiz.show_question()
                pygame.display.update()  # Ensure the screen is updated immediately

            if self.player.entity.check_collision(self.enemy.entity) and self.dialog_window.dialog_shown:
                self.conversation_active = True
                self.show_conversation()
            else:
                self.conversation_active = False

            if not self.conversation_active and not self.problem_solved and self.conversation_shown:
                self.quiz.show_question()

            pygame.display.update()
            clock.tick(60)

    def render_health(self):
        for i in range(self.player.health):
            screen.blit(pygame.image.load('data/images/heart.jpg'), (WINDOW_SIZE[0] - 60 * (i + 1), 10))

    def show_game_over(self):
        game_over_text = self.font.render("YOU LOST", True, (255, 0, 0))
        screen.blit(game_over_text, (WINDOW_SIZE[0] // 2 - 100, WINDOW_SIZE[1] // 2 - 50))
        pygame.display.update()
        pygame.time.delay(2000)  # Display the text for 2 seconds
        return "level_selection"

    def show_math_problem(self):
        if self.current_problem_index < len(self.current_problems):
            problem_text = self.current_problems[self.current_problem_index]
            problem_surface = self.font.render(problem_text, True, (0, 0, 0))
            screen.blit(problem_surface, (WINDOW_SIZE[0] // 2 - problem_surface.get_width() // 2, WINDOW_SIZE[1] // 2 - problem_surface.get_height() // 2))

    def check_answer(self):
        # Implement logic to check the player's answer
        # For simplicity, assume the player always gives the correct answer
        self.current_problem_index += 1
        if self.current_problem_index >= len(self.current_problems):
            self.problem_solved = True
    
    def get_top_of_ones(self):
        for y, row in enumerate(self.tile_map):
            for x, tile in enumerate(row):
                if tile == 1:
                    return y * 16  # Assuming each tile is 16 pixels high
        return float('inf')  # Return a very high value if no 1s are found

    def load_dialog_from_file(self, filepath):
        with open(filepath, 'r') as file:
            dialog_lines = file.read().splitlines()
        self.dialog_window.load_dialog(dialog_lines)

    def show_conversation(self):
        if not self.dialog_window.dialog_shown:
            return  # Do not show the conversation if the dialog has been shown
        if self.dialog_window.current_line_index < len(self.dialog_window.dialog_lines):
            current_line = self.dialog_window.dialog_lines[self.dialog_window.current_line_index]
            if current_line.startswith('-'):
                # Player's line
                self.dialog_window.set_text("Player: \n" + current_line[1:].strip())            
            else:
                # Enemy's line
                self.dialog_window.set_text(current_line)
        self.dialog_window.render(screen)