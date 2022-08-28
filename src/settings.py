class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)


        # ship settings
        self.ship_speed = 20
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed = 50
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        # alien settings
        self.alien_speed = 12
        self.fleet_speed = 12
        self.fleet_direction = 1    # this represents going right

        # game settings
        self.speedup = 1.3
        self.alien_points = 50
        self.initialize_dynamic_settings()
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        self.ship_speed = 15
        self.bullet_speed = 20
        self.alien_speed = 4
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup
        self.bullet_speed *= self.speedup
        self.alien_speed *= self.speedup
        self.alien_points *= self.score_scale

