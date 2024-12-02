import random

def load_tile_map(file_path):
    """Load the tile map from a file."""
    with open(file_path, 'r') as file:
        tile_map = [list(map(int, line.split())) for line in file]
    return tile_map
