#!/usr/bin/env python
"""Version 0.0.1

Features:
    Keyboard entry.
"""
import sys

import pygame


if __name__ == '__main__':
    ## initialize PyGame and set up resources needed in the game
    pygame.init()
    BOARD = pygame.display.set_mode((320, 240))
    CLOCK  = pygame.time.Clock()

    image_path = 'images/player/default.png'
    player_image = pygame.image.load(image_path).convert_alpha()
    player_x = 0
    player_y = 0

    ## Set a condition that allows the game to continue or end
    game_over = False
    ## The main game loop
    while not game_over:
        BOARD.fill((10, 0, 15))

        ## Get input from the user (keyboard)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ## Did the user click the "close" icon on the game window?
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                elif event.key == pygame.K_UP:
                    player_y -= 1
                elif event.key == pygame.K_DOWN:
                    player_y += 1
                elif event.key == pygame.K_LEFT:
                    player_x -= 1
                elif event.key == pygame.K_RIGHT:
                    player_x += 1

        ## Draw the player on the baord and update the clock.
        BOARD.blit(player_image, (player_x, player_y))
        pygame.display.flip()
        CLOCK.tick(20)

    print('Goodbye!')
    ## Let PyGame release the resources it initialized
    pygame.quit()
    sys.exit()
