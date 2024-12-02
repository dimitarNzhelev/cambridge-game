import random

def load_tile_map(file_path):
    """Load the tile map from a file."""
    with open(file_path, 'r') as file:
        tile_map = [list(map(int, line.split())) for line in file]
    return tile_map

def generate_chunk(x, y, chunk_size, tile_map):
    """Generate a chunk of the world based on the tile map."""
    chunk_data = []
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            target_x = x * chunk_size + x_pos
            target_y = y * chunk_size + y_pos
            if 0 <= target_y < len(tile_map) and 0 <= target_x < len(tile_map[target_y]):
                tile_type = tile_map[target_y][target_x]
                if tile_type != 0:
                    chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data

# Load the tile map
tile_map = load_tile_map('data/tile_map.txt')