import sys

import pygame

from bullet import Bullet

from alien import Alien

from ship import Morty

from time import sleep


def check_events(ai_settings, screen, stats, sb, button, ship, aliens, bullets):
    """responds to keypressing and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_button(ai_settings, screen, stats, sb, button, ship, aliens, bullets, mouse_x, mouse_y)


def check_button(ai_settings, screen, stats, sb, button, ship, aliens, bullets, mouse_x, mouse_y):
    if button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        stats.game_active = True
        stats.reset_stats()

        pygame.mouse.set_visible(False)

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

        aliens.empty()
        for bullet in bullets.sprites():
            bullets.remove(bullet)

        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()
        ai_settings.initialize_dynamic_settings()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, button):
    """update images on screen and flips to new screen"""

    # redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        button.draw_button()

    sb.show_score()
    # make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, aliens, bullets):
    """Update position of bullets and gets rid of old ones"""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien(ai_settings, screen, stats, sb, aliens, bullets)


def create_fleet(ai_settings, screen, aliens):
    morty = Morty(ai_settings, screen)
    alien = Alien(ai_settings, screen)

    num_aliens = get_num_aliens(ai_settings, alien.rect.width)
    num_rows = get_num_rows(ai_settings, morty.rect.height, alien.rect.height)

    for row_num in range(num_rows):
        for alien_num in range(num_aliens):
            create_alien(ai_settings, screen, aliens, alien_num, row_num)


def check_keydown(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.rect.centerx += 1
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.rect.centerx -= 1
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        if len(bullets) <= 5:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def get_num_aliens(ai_settings, screen):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 2 * alien_width
    num_aliens = int(available_space_x / (2 * alien_width))
    return num_aliens


def create_alien(ai_settings, screen, aliens, alien_num, row_num):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_num
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_num
    aliens.add(alien)


def get_num_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    num_rows = int(available_space_y / (2 * alien_height))
    return num_rows


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    check_fleet_edge(ai_settings, aliens)
    aliens.update()

    # check for game ending collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def check_fleet_edge(ai_settings, aliens):
    """respond to the fleet hitting the edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """drop the fleet and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_speed
    ai_settings.fleet_direction *= -1


def check_bullet_alien(ai_settings, screen, stats, sb, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, aliens)
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    if stats.ships_left > 0:

        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()

        sleep(0.5)

    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def check_high(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
