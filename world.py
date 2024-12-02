import random

def generate_chunk(x, y, chunk_size):
    """Generate a chunk of the world."""
    chunk_data = []
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            target_x = x * chunk_size + x_pos
            target_y = y * chunk_size + y_pos
            tile_type = 0  # nothing
            if target_y > 10:
                tile_type = 2  # dirt
            elif target_y == 10:
                tile_type = 1  # grass
            elif target_y == 9:
                if random.randint(1, 5) == 1:
                    tile_type = 3  # plant
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data