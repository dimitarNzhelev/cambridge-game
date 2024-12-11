import pygame
from scenes.menu import MenuScene
from scenes.level_selection import LevelSelectionScene
from scenes.level_base import LevelBaseScene

class Game:
    def __init__(self):
        self.current_scene = "menu"
    
    def run(self):
        while True:
            if self.current_scene == "menu":
                scene = MenuScene()
            elif self.current_scene == "level_selection":
                scene = LevelSelectionScene()
            elif self.current_scene.startswith("level"):
                level_number = int(self.current_scene.replace("level", ""))
                scene = LevelBaseScene(level_number)
            self.current_scene = scene.run()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()