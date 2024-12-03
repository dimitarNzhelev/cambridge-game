import math
import pygame
from core.physics import PhysicsObject
from utils.helpers import flip, blit_center
from graphics.animation import animation_database, animation_higher_database

class Entity:
    """
    A game entity with physics, animation, and rendering capabilities.
    """
    def __init__(self,x,y,size_x,size_y,e_type): # x, y, size_x, size_y, type
        """
        Initialize a new Entity instance.
        
        Args:
            x (float): Initial x-coordinate position
            y (float): Initial y-coordinate position
            size_x (int): Width of the entity
            size_y (int): Height of the entity
            e_type (str): Type of entity, used for determining animation sets
        """
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.obj = PhysicsObject(x,y,size_x,size_y)
        self.animation = None
        self.image = None
        self.animation_frame = 0
        self.animation_tags = []
        self.flip = False
        self.offset = [0,0]
        self.rotation = 0
        self.type = e_type # used to determine animation set among other things
        self.action_timer = 0
        self.action = ''
        self.set_action('idle') # overall action for the entity
        self.entity_data = {}
        self.alpha = None
 
    def set_pos(self,x,y):
        """
        Set the absolute position of the entity.
        
        Args:
            x (float): New x-coordinate position
            y (float): New y-coordinate position
        """
        self.x = x
        self.y = y
        self.obj.x = x
        self.obj.y = y
        self.obj.rect.x = x
        self.obj.rect.y = y
 
    def move(self,momentum,platforms,ramps=[]):
        """
        Move the entity based on momentum and handle collisions.
        
        Args:
            momentum (List[float]): [x, y] movement vector
            platforms (List): List of platform objects to check collisions against
            ramps (List, optional): List of ramp objects to check collisions against
        
        Returns:
            dict: Dictionary containing collision information
        """
        collisions = self.obj.move(momentum,platforms,ramps)
        self.x = self.obj.x
        self.y = self.obj.y
        return collisions
 
    def rect(self):
        """
        Get the entity's rectangular boundary.
        
        Returns:
            pygame.Rect: Rectangle representing the entity's boundaries
        """
        return pygame.Rect(self.x,self.y,self.size_x,self.size_y)
 
    def set_flip(self,boolean):
        """
        Set whether the entity's sprite should be flipped horizontally.
        
        Args:
            boolean (bool): True to flip the sprite, False otherwise
        """
        self.flip = boolean
 
    def set_animation_tags(self,tags):
        """
        Set the animation tags for the entity.
        
        Args:
            tags (List[str]): List of animation tags
        """
        self.animation_tags = tags
 
    def set_animation(self,sequence):
        """
        Set the current animation sequence.
        
        Args:
            sequence (List): Animation sequence to play
        """
        self.animation = sequence
        self.animation_frame = 0
 
    def set_action(self,action_id,force=False):
        """
        Set the current action and corresponding animation.
        
        Args:
            action_id (str): ID of the action to perform
            force (bool, optional): Force the action change even if it's the same action
        """
        if (self.action == action_id) and (force == False):
            pass
        else:
            self.action = action_id
            anim = animation_higher_database[self.type][action_id]
            self.animation = anim[0]
            self.set_animation_tags(anim[1])
            self.animation_frame = 0

    def get_entity_angle(self, entity_2):
        """
        Calculate the angle between this entity and another entity.
        
        Args:
            entity_2 (Entity): The target entity
            
        Returns:
            float: Angle in radians between the two entities
        """
        x1 = self.x+int(self.size_x/2)
        y1 = self.y+int(self.size_y/2)
        x2 = entity_2.x+int(entity_2.size_x/2)
        y2 = entity_2.y+int(entity_2.size_y/2)
        angle = math.atan((y2-y1)/(x2-x1))
        if x2 < x1:
            angle += math.pi
        return angle

    def get_center(self):
        """
        Get the center coordinates of the entity.
        
        Returns:
            List[float]: [x, y] coordinates of entity's center
        """
        x = self.x+int(self.size_x/2)
        y = self.y+int(self.size_y/2)
        return [x,y]
 
    def clear_animation(self):
        """
        Clear the current animation sequence.
        """
        self.animation = None
 
    def set_image(self,image):
        """
        Set the entity's static image.
        
        Args:
            image (pygame.Surface): Image to set for the entity
        """
        self.image = image
 
    def set_offset(self,offset):
        """
        Set the rendering offset for the entity.
        
        Args:
            offset (List[float]): [x, y] offset values
        """
        self.offset = offset
 
    def set_frame(self,amount):
        """
        Set the current animation frame.
        
        Args:
            amount (int): Frame number to set
        """
        self.animation_frame = amount
 
    def handle(self):
        """
        Handle entity updates per frame.
        Updates action timer and animation frames.
        """
        self.action_timer += 1
        self.change_frame(1)
 
    def change_frame(self,amount):
        """
        Change the current animation frame by the specified amount.
        
        Args:
            amount (int): Number of frames to advance (positive) or rewind (negative)
        """
        self.animation_frame += amount
        if self.animation != None:
            while self.animation_frame < 0:
                if 'loop' in self.animation_tags:
                    self.animation_frame += len(self.animation)
                else:
                    self.animation = 0
            while self.animation_frame >= len(self.animation):
                if 'loop' in self.animation_tags:
                    self.animation_frame -= len(self.animation)
                else:
                    self.animation_frame = len(self.animation)-1
 
    def get_current_img(self):
        """
        Get the current image of the entity without any transformations.
        
        Returns:
            pygame.Surface: Current frame of animation or static image
        """
        if self.animation == None:
            if self.image != None:
                return flip(self.image,self.flip)
            else:
                return None
        else:
            return flip(animation_database[self.animation[self.animation_frame]],self.flip)

    def get_drawn_img(self):
        """
        Get the current image with all transformations applied (rotation, flip, alpha).
        
        Returns:
            Tuple[pygame.Surface, float, float]: Transformed image and its center coordinates
        """
        image_to_render = None
        if self.animation == None:
            if self.image != None:
                image_to_render = flip(self.image,self.flip).copy()
        else:
            image_to_render = flip(animation_database[self.animation[self.animation_frame]],self.flip).copy()
        if image_to_render != None:
            center_x = image_to_render.get_width()/2
            center_y = image_to_render.get_height()/2
            image_to_render = pygame.transform.rotate(image_to_render,self.rotation)
            if self.alpha != None:
                image_to_render.set_alpha(self.alpha)
            return image_to_render, center_x, center_y
        
    def check_collision(self,other_entity):
        """
        Check if the entity is colliding with another entity.
        
        Args:
            other_entity (Entity): The entity to check collision against
            
        Returns:
            bool: True if the entities are colliding, False otherwise
        """
        return self.obj.rect.colliderect(other_entity.obj.rect)
 
    def display(self, surface, scroll, center_image=False):
        """
        Display the entity on the given surface with scroll offset.
        
        Args:
            surface (pygame.Surface): Surface to draw the entity on
            scroll (List[float]): [x, y] scroll offset values
            center_image (bool): Whether to center the image within the entity
        """
        image_to_render = None
        if self.animation is None:
            if self.image is not None:
                image_to_render = flip(self.image, self.flip).copy()
        else:
            image_to_render = flip(animation_database[self.animation[self.animation_frame]], self.flip).copy()
        
        if image_to_render is not None:
            image_to_render = pygame.transform.rotate(image_to_render, self.rotation)
            if self.alpha is not None:
                image_to_render.set_alpha(self.alpha)
            if center_image:
                center_x = self.size_x / 2
                center_y = self.size_y / 2
                blit_center(surface, image_to_render, (int(self.x - scroll[0] + center_x), int(self.y - scroll[1] + center_y)))
            else:
                center_x = image_to_render.get_width() / 2
                center_y = image_to_render.get_height() / 2
                blit_center(surface, image_to_render, (int(self.x) - scroll[0] + self.offset[0] + center_x, int(self.y) - scroll[1] + self.offset[1] + center_y))