# utils/resource_loader.py
import pygame
import os

class ResourceLoader:
    """Handles loading and caching of game resources."""
    
    _instance = None
    _fonts = {}
    _images = {}
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_font(self, path, size):
        """Load and cache fonts."""
        key = f"{path}_{size}"
        if key not in self._fonts:
            self._fonts[key] = pygame.font.Font(path, size)
        return self._fonts[key]
    
    def get_image(self, path):
        """Load and cache images."""
        if path not in self._images:
            self._images[path] = pygame.image.load(path)
        return self._images[path]
