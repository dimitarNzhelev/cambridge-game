from typing import List
import pygame

def collision_test(object_1: pygame.Rect, object_list: List[pygame.Rect]) -> List[pygame.Rect]:
    """
    Test collision between one object and a list of objects.
    Returns a list of objects that collide with object_1.
    """
    return [obj for obj in object_list if obj.colliderect(object_1)]
