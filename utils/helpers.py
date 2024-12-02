import pygame
from typing import Tuple

def flip(img: pygame.Surface, boolean: bool = True) -> pygame.Surface:
    """Flip an image horizontally."""
    return pygame.transform.flip(img, boolean, False)

def blit_center(surf: pygame.Surface, surf2: pygame.Surface, pos: Tuple[int, int]) -> None:
    """Blit one surface onto another at its center."""
    x = int(surf2.get_width() / 2)
    y = int(surf2.get_height() / 2)
    surf.blit(surf2, (pos[0] - x, pos[1] - y))
