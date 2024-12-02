import entries.entity as e

class Player:
    def __init__(self, x, y):
        self.entity = e.Entity(x, y, 5, 13, 'player')
        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.air_timer = 0
        self.health = 3

    def handle_movement(self):
        """Handle player movement based on input."""
        player_movement = [0, 0]
        if self.moving_right:
            player_movement[0] += 2
        if self.moving_left:
            player_movement[0] -= 2
        player_movement[1] += self.vertical_momentum
        self.vertical_momentum += 0.2
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3

        if player_movement[0] == 0:
            self.entity.set_action('idle')
        if player_movement[0] > 0:
            self.entity.set_flip(False)
            self.entity.set_action('run')
        if player_movement[0] < 0:
            self.entity.set_flip(True)
            self.entity.set_action('run')

        return player_movement

    def update(self, tile_rects):
        """Update player state and handle collisions."""
        player_movement = self.handle_movement()
        collision_types = self.entity.move(player_movement, tile_rects)

        if collision_types['bottom']:
            self.air_timer = 0
            self.vertical_momentum = 0
        else:
            self.air_timer += 1

        self.entity.change_frame(1)

    def render(self, display, scroll):
        """Render the player on the display."""
        self.entity.display(display, scroll)