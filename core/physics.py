import pygame
import core.collision as collision
class PhysicsObject:
    """
    A 2D physics object with basic position and size properties.
    """
    def __init__(self, x: float, y: float, x_size: float, y_size: float):
        self.width = x_size
        self.height = y_size
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.x = x
        self.y = y

    def move(self,movement,platforms,ramps=[]):
        self.x += movement[0]
        self.rect.x = int(self.x)
        block_hit_list = collision.collision_test(self.rect,platforms)
        collision_types = {'top':False,'bottom':False,'right':False,'left':False,'slant_bottom':False,'data':[]}
        # added collision data to "collision_types". ignore the poorly chosen variable name
        for block in block_hit_list:
            markers = [False,False,False,False]
            if movement[0] > 0:
                self.rect.right = block.left
                collision_types['right'] = True
                markers[0] = True
            elif movement[0] < 0:
                self.rect.left = block.right
                collision_types['left'] = True
                markers[1] = True
            collision_types['data'].append([block,markers])
            self.x = self.rect.x
        self.y += movement[1]
        self.rect.y = int(self.y)
        block_hit_list = collision.collision_test(self.rect,platforms)
        for block in block_hit_list:
            markers = [False,False,False,False]
            if movement[1] > 0:
                self.rect.bottom = block.top
                collision_types['bottom'] = True
                markers[2] = True
            elif movement[1] < 0:
                self.rect.top = block.bottom
                collision_types['top'] = True
                markers[3] = True
            collision_types['data'].append([block,markers])
            self.change_y = 0
            self.y = self.rect.y
        return collision_types

class Cuboid:
    """
    A 3D collision object represented by x, y, z coordinates and dimensions.
    """
    def __init__(self, x: float, y: float, z: float, x_size: float, y_size: float, z_size: float):
        self.x = x
        self.y = y
        self.z = z
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
    
    def set_pos(self, x: float, y: float, z: float) -> None:
        """Update the position of the cuboid."""
        self.x = x
        self.y = y
        self.z = z
    
    def collidecuboid(self, cuboid_2: 'Cuboid') -> bool:
        """Check collision between two cuboids."""
        cuboid_1_xy = pygame.Rect(self.x, self.y, self.x_size, self.y_size)
        cuboid_1_yz = pygame.Rect(self.y, self.z, self.y_size, self.z_size)
        cuboid_2_xy = pygame.Rect(cuboid_2.x, cuboid_2.y, cuboid_2.x_size, cuboid_2.y_size)
        cuboid_2_yz = pygame.Rect(cuboid_2.y, cuboid_2.z, cuboid_2.y_size, cuboid_2.z_size)
        return (cuboid_1_xy.colliderect(cuboid_2_xy) and 
                cuboid_1_yz.colliderect(cuboid_2_yz))
