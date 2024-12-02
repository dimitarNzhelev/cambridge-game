# main.py
import pygame
from settings import screen
from scenes.menu import MenuScene
from scenes.level1 import Level1Scene 

class Game:
    def __init__(self):
        self.current_scene = "menu"
        self.scenes = {
            "menu": MenuScene(),
            "level1": Level1Scene()
        }
    
    def run(self):
        while True:
            if self.current_scene == "menu":
                self.current_scene = self.scenes["menu"].run()
            elif self.current_scene == "level1":
                self.scenes["level1"].run()
                self.current_scene = "menu"

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()