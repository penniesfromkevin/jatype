#!/usr/bin/env python
"""Version 0.0.2

Features:
    Keybaord entry.
    Parameterization.
    Boundary checking.
    Player size.
    Random library.
"""
import random
import sys

import pygame

FRAME_RATE = 20
BOARD_WIDTH = 320
BOARD_HEIGHT = 240
SPEED = 2
BACKGROUND = (10, 0, 15)


if __name__ == '__main__':
    ## initialize PyGame and set up resources needed in the game
    pygame.init()
    BOARD = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    CLOCK  = pygame.time.Clock()

    ## The player
    image_path = 'images/player/default.png'
    player_image = pygame.image.load(image_path).convert_alpha()
    player_width, player_height = player_image.get_size()
    player_x = random.randint(0, BOARD_WIDTH - player_width)
    player_y = random.randint(0, BOARD_HEIGHT - player_height)

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
                elif event.key == pygame.K_UP:
                    player_y -= SPEED
                elif event.key == pygame.K_DOWN:
                    player_y += SPEED
                elif event.key == pygame.K_LEFT:
                    player_x -= SPEED
                elif event.key == pygame.K_RIGHT:
                    player_x += SPEED

        ## If the new x-position will take the player off the BOARD, prevent it
        if player_x < 0:
            player_x = 0
        elif player_x > BOARD_WIDTH - player_width:
            player_x = BOARD_WIDTH - player_width

        ## If the new y-position will take the player off the BOARD, prevent it
        if player_y < 0:
            player_y = 0
        elif player_y > BOARD_HEIGHT - player_height:
            player_y = BOARD_HEIGHT - player_height

        ## Draw the player on the baord and update the clock.
        BOARD.blit(player_image, (player_x, player_y))
        pygame.display.flip()
        CLOCK.tick(FRAME_RATE)

    print('Goodbye!')
    ## Let PyGame release the resources it initialized
    pygame.quit()
    sys.exit()
