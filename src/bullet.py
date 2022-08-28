import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """a class to manage the bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        """create a bullet object at ships current positon"""
        super().__init__()  # this is to inherit correctly the attributes from sprite
        self.screen = screen

        # create a bullet at (0, 0)
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)  # this is how to build a
        # rect from scratch
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed

    def update(self):
        """update the bullet position continuously"""
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """draws bullet to screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
