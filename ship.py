import pygame
from pygame.sprite import Sprite


class Morty:

    def __init__(self, ai_settings, screen):
        """initialize morty and his starting position"""
        self.screen = screen
        self.ai_settings = ai_settings

        # load in ship
        self.image = pygame.image.load("frost.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # start this guy in the middle of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # this will hold the float value for ships center
        self.center = self.rect.centerx

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed

        # update ships center positions
        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
