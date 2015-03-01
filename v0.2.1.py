#!/usr/bin/env python
"""Version 0.2.1

Features:
    Keybaord entry.
    Parameterization.
    Boundary checking.
    Player size.
    Random library.
    Key-up handling.
    Speed.
    Speed control.
    Player object (dictionary)
    make_player() function.
"""
import random
import sys

import pygame

FRAME_RATE = 20
BOARD_WIDTH = 320
BOARD_HEIGHT = 240
SPEED = 2
SPEED_MAX = 10
BACKGROUND = (10, 0, 15)


def make_player():
    """Create the player object.

    Returns:
        Player dictionary.
    """
    image_path = 'images/player/default.png'
    player_image = pygame.image.load(image_path).convert_alpha()
    player_width, player_height = player_image.get_size()
    player = {
            'image': player_image,
            'width': player_width,
            'height': player_height,
            'x_position': random.randint(0, BOARD_WIDTH - player_width),
            'y_position': random.randint(0, BOARD_HEIGHT - player_height),
            'x_speed': 0,
            'y_speed': 0,
            'speed': SPEED,
            }
    return player


if __name__ == '__main__':
    ## initialize PyGame and set up resources needed in the game
    pygame.init()
    BOARD = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    CLOCK  = pygame.time.Clock()

    player = make_player()

    ## Set a condition that allows the game to continue or end
    game_over = False
    ## The main game loop
    while not game_over:
        BOARD.fill(BACKGROUND)

        ## Get input from the user (keyboard)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ## Did the user click the "close" icon on the game window?
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                elif event.key == pygame.K_LEFT:
                    player['x_speed'] = -player['speed']
                elif event.key == pygame.K_RIGHT:
                    player['x_speed'] = player['speed']
                elif event.key == pygame.K_UP:
                    player['y_speed'] = -player['speed']
                elif event.key == pygame.K_DOWN:
                    player['y_speed'] = player['speed']
                elif event.key == pygame.K_z:
                    if player['speed'] > 1:
                        player['speed'] -= 1
                elif event.key == pygame.K_x:
                    if player['speed'] < SPEED_MAX:
                        player['speed'] += 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player['x_speed'] = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player['y_speed'] = 0

        ## Update position based on speed in specific directions
        player['x_position'] += player['x_speed']
        player['y_position'] += player['y_speed']

        ## If the new x-position will take the player off the BOARD, prevent it
        if player['x_position'] < 0:
            player['x_position'] = 0
        elif player['x_position'] > BOARD_WIDTH - player['width']:
            player['x_position'] = BOARD_WIDTH - player['width']

        ## If the new y-position will take the player off the BOARD, prevent it
        if player['y_position'] < 0:
            player['y_position'] = 0
        elif player['y_position'] > BOARD_HEIGHT - player['height']:
            player['y_position'] = BOARD_HEIGHT - player['height']

        ## Draw the player on the baord and update the clock.
        BOARD.blit(player['image'], (player['x_position'],
                                     player['y_position']))
        pygame.display.flip()
        CLOCK.tick(FRAME_RATE)

    print('Goodbye!')
    ## Let PyGame release the resources it initialized
    pygame.quit()
    sys.exit()
