import random
from utils.components.falling_object import FallingObject

class FallingObjectManager:
    def __init__(self, falling_object_image, player, screen_height):
        self.falling_objects = []
        self.falling_object_image = falling_object_image
        self.player = player
        self.screen_height = screen_height

    def create_falling_object(self):
        if not self.player.is_immune and random.randint(1, 100) == 1:  # Adjust the frequency as needed
            new_object = FallingObject(random.randint(0, 300), -20, self.falling_object_image)
            self.falling_objects.append(new_object)

    def update_and_render(self, display, scroll):
        if self.player.is_immune:
            return  # Do not update or render falling objects if the player is immune

        for obj in self.falling_objects:
            obj.update()
            obj.render(display, scroll)
            if obj.check_collision(self.player.entity.rect()):
                self.player.health -= 1  # Decrease player health
                self.falling_objects.remove(obj)  # Remove the object after collision

        # Remove objects that have fallen off the screen
        self.falling_objects = [obj for obj in self.falling_objects if obj.rect.y < self.screen_height]
