import pygame
from typing import List, Tuple, Dict

animation_database: Dict[str, pygame.Surface] = {}
animation_higher_database: Dict[str, dict] = {}

def set_global_colorkey(colorkey: Tuple[int, int, int]) -> None:
    """Set the global color key for transparency."""
    global e_colorkey
    e_colorkey = colorkey

def animation_sequence(sequence: List[List[int]], 
                      base_path: str,
                      size_x: int = 10,
                      size_y: int = 26,
                      colorkey: Tuple[int, int, int] = (255, 255, 255),
                      transparency: int = 255) -> List[str]:
    """
    Create an animation sequence from image files.
    Returns a list of image IDs for the animation.
    """
    global animation_database
    result = []
    for frame in sequence:
        frame_index, duration = frame
        image_id = f"{base_path}{base_path.split('/')[-2]}_{frame_index}"
        image_temp = pygame.image.load(f"{image_id}.png").convert_alpha()  # Use convert_alpha for transparency
        image = pygame.transform.scale(image_temp, (size_x, size_y))
        # Remove the background of the image
        image.set_colorkey(colorkey)
        image.set_alpha(transparency)
        animation_database[image_id] = image.copy()
        result.extend([image_id] * duration)
    return result