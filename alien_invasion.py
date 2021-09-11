import pygame

import sys

from settings import Settings
import game_functions as gf
from ship import Morty
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()  # initialize game and create screen object AND SETTINGS
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    button = Button(ai_settings, screen, "Come here *burps* Morty")

    # instance of game stats
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # make a morty
    morty = Morty(ai_settings, screen)
    # make a bullet group
    bullets = Group()
    # make an alien group
    aliens = Group()

    # create a fleet of aliens
    gf.create_fleet(ai_settings, screen, aliens)
    # start main loop for game
    while True:
        gf.check_events(ai_settings, screen, stats, sb, button, morty, aliens, bullets)

        if stats.game_active:
            morty.update()
            gf.update_bullets(ai_settings, screen, stats, sb, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, morty, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, morty, aliens, bullets, button)


run_game()
