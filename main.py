# main.py
import pygame
from scenes.menu import MenuScene
from scenes.level1 import Level1Scene
from scenes.level_selection import LevelSelectionScene

class Game:
    def __init__(self):
        self.current_scene = "menu"
        self.scenes = {
            "menu": MenuScene(),
            "level_selection": LevelSelectionScene(),
            "level1": Level1Scene()
        }
    
    def run(self):
        while True:
            if self.current_scene == "menu":
                self.current_scene = self.scenes["menu"].run()
            elif self.current_scene == "level_selection":
                self.current_scene = self.scenes["level_selection"].run()
            elif self.current_scene == "level1":
                self.current_scene = self.scenes["level1"].run()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()