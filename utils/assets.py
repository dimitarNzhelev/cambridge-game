import pygame
from graphics.animation import animation_sequence, set_global_colorkey, animation_higher_database

def load_assets():
    """Load game assets like images and sounds."""
    assets = {}
    
    # Load images
    assets['grass_img'] = pygame.image.load('data/images/grass.png')
    assets['dirt_img'] = pygame.image.load('data/images/dirt.png')
    assets['plant_img'] = pygame.image.load('data/images/plant.png').convert()
    assets['plant_img'].set_colorkey((255, 255, 255))
    assets['background_image'] = pygame.image.load('data/images/castle.webp').convert()

    # Load sounds
    # assets['jump_sound'] = pygame.mixer.Sound('data/audio/jump.wav')
    assets['grass_sounds'] = [
        pygame.mixer.Sound('data/audio/grass_0.wav'),
        pygame.mixer.Sound('data/audio/grass_1.wav')
    ]
    assets['grass_sounds'][0].set_volume(0.2)
    assets['grass_sounds'][1].set_volume(0.2)

    # Create a tile index mapping
    assets['tile_index'] = {
        1: assets['grass_img'],
        2: assets['dirt_img'],
        3: assets['plant_img']
    }
    
    # Load animations
    load_animations()
    
    # Load music
    pygame.mixer.music.load('data/audio/music.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    
    return assets

def load_animations(size_x=7.5, size_y=19.5):
    """Load animations for entities from entity_animations.txt."""
    global animation_higher_database
    with open('data/images/entities/entity_animations.txt', 'r') as f:
        data = f.read().splitlines()
    
    for line in data:
        if line.strip():
            parts = line.split(' ')
            anim_path = parts[0]
            entity_type, animation_name = anim_path.split('/')[:2]
            frame_durations = list(map(int, parts[1].split(';')))
            tags = parts[2].split(';') if len(parts) > 2 else []

            sequence = [[i, duration] for i, duration in enumerate(frame_durations)]
            anim = animation_sequence(sequence, f'data/images/entities/{anim_path}', size_x, size_y)
            
            if entity_type not in animation_higher_database:
                animation_higher_database[entity_type] = {}
            animation_higher_database[entity_type][animation_name] = [anim, tags]