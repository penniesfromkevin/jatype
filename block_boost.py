#!/usr/bin/env python
"""A dashing game, without geometry.
"""
__author__ = 'Kevin'

import argparse
import logging
import os
import random
import sys

import pygame

FRAME_RATE = 30
BOARD_WIDTH, BOARD_HEIGHT = BOARD_SIZE = 640, 480
DEFAULT_SPEED = 10
DEFAULT_ENEMIES = 10
INCREASE_TIME = 5

LOG_LEVELS = ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG')
DEFAULT_LOG_LEVEL = LOG_LEVELS[3]
LOGGER = logging.getLogger()


class ImageStore(object):
    """Image store.
    """
    def __init__(self, path, ext='png'):
        """Initialize the store.

        Args:
            path: Path to image files.
            ext: File extension image files.
        """
        self._store = {}
        self._path = path
        self._ext = ext

    def get(self, name):
        """Get image object.

        If the image does not exist in the store, this will also try to
        add it first, but it is better to pre-add images as there is
        less delay.

        Args:
            name: Name of image to get.

        Returns:
            Image object, or None if object could not be found.
        """
        if name in self._store:
            image = self._store[name]
        else:
            image = self.add(name)
        LOGGER.debug(self._store)
        return image

    def add(self, name):
        """Add image object to the store.

        Args:
            name: Name of image to add.

        Returns:
            Image object, or None if object could not be loaded.
        """
        image_path = os.path.join(self._path, '%s.%s' % (name, self._ext))
        try:
            image_object = pygame.image.load(image_path).convert_alpha()
        except:
            image_object = None
        self._store[name] = image_object
        return image_object


class Character(pygame.sprite.Sprite):
    """All controllable things.
    """
    def __init__(self, kind, board, x_pos=0, y_pos=0):
        """Initialize character.
        """
        super(Character, self).__init__()
        #pygame.sprite.Sprite.__init__(self)

        self.kind = kind
        self.board = board
        self.speed = DEFAULT_SPEED

        self.image = IMAGES.get(kind)
        self.width, self.height = self.image.get_size()

        # Fetch the rectangle object that has the dimensions of the image
        # Update position by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

        self.rect.x = self.x_pos = x_pos
        self.rect.y = self.y_pos = y_pos

        self.x_inc = 0
        self.y_inc = 0

    def display(self, x_pos=None, y_pos=None):
        """Display the character.
        """
        if x_pos is None:
            x_pos = self.x_pos
        if y_pos is None:
            y_pos = self.y_pos
        self.board.blit(self.image, (x_pos, y_pos))

    def update(self):
        """Update sprite.
        """
        self.x_pos += self.x_inc
        self.y_pos += self.y_inc
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.display()


class Enemy(Character):
    """All user-controllable things.
    """
    def __init__(self, kind, board):
        """Initialize Enemy.
        """
        board_x, board_y = board.get_size()
        x_pos = random.randint(0, board_x) + board_x
        image = 'enemy/%s' % kind
        super(Enemy, self).__init__(image, board, x_pos)
        self.speed = DEFAULT_SPEED
        self.x_inc = -self.speed
        y_max = board_y - self.height
        self.y_pos = random.randint(0, y_max)


class Player(Character):
    """All user-controllable things.
    """
    def __init__(self, kind, board, x_pos=0, y_pos=0):
        """Initialize Player.
        """
        image = 'player/%s' % kind
        super(Player, self).__init__(image, board, x_pos, y_pos)
        self.y_inc = self.speed
        self.mirror = False

    def get_input(self):
        """Get user input.

        Returns:
            String: 'quit', 'pause', or '' (empty string)
        """
        return_value = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ## Did the user click the 'close' icon on the game window?
                return_value = 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_value = 'quit'
                elif event.key == pygame.K_p:
                    return_value = 'pause'
                elif event.key == pygame.K_SPACE:
                    self.y_inc = -self.speed
                elif event.key == pygame.K_z:
                    self.mirror = not self.mirror
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    self.x_inc = 0
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    self.y_inc = 0
                elif event.key in (pygame.K_SPACE,):
                    self.y_inc = self.speed
        return return_value

    def update(self):
        """Update player.
        """
        if self.x_pos + self.x_inc > BOARD_WIDTH - self.width:
            self.x_pos = BOARD_WIDTH - self.width
            self.x_inc = 0
        elif self.x_pos + self.x_inc < 0:
            self.x_pos = 0
            self.x_inc = 0
        if self.y_pos + self.y_inc > BOARD_HEIGHT - self.height:
            self.y_pos = BOARD_HEIGHT - self.height
            self.y_inc = 0
        elif self.y_pos + self.y_inc < 0:
            self.y_pos = 0
            self.y_inc = 0
        super(Player, self).update()
        if self.mirror:
            half_board = self.board.get_height() / 2
            mirror_y = half_board - (self.y_pos - half_board) - self.height
            self.display(y_pos=mirror_y)


class Background(object):
    """Backgrounds.  Yes, plural.
    """
    def __init__(self, levels, board, x_inc=0, y_inc=0):
        """Initialize scrolling background object.

        Args:
            levels: A single background name, or list of backgrounds.
        """
        self.board = board
        if not isinstance(levels, (list, tuple)):
            levels = [levels]
        self.levels = []
        for incr, level in enumerate(levels):
            image = 'background/%s' % level
            background = Character(image, self.board, 0, 0)
            background.display()
            background.x_inc = x_inc + int(x_inc * (incr + 1) / len(levels))
            background.y_inc = y_inc + int(y_inc * (incr + 1) / len(levels))
            LOGGER.debug('x: %d, y: %d', background.x_inc, background.y_inc)
            self.levels.append(background)

    def update(self):
        """Update backgrounds.
        """
        for level in self.levels:
            if level.x_pos <= -level.width or level.x_pos >= level.width:
                level.x_pos = 0
            if level.y_pos <= -level.height or level.y_pos >= level.height:
                level.y_pos = 0

            if level.x_inc:
                self.board.blit(level.image,
                        (level.x_pos - cmp(level.x_inc, 0) * level.width,
                         level.y_pos))
            if level.y_inc:
                self.board.blit(level.image,
                        (level.x_pos,
                         level.y_pos - cmp(level.y_inc, 0) * level.height))
                # If movement is diagonal, a fourth copy is required
                if level.x_inc:
                    self.board.blit(level.image,
                            (level.x_pos - cmp(level.x_inc, 0) * level.width,
                             level.y_pos - cmp(level.y_inc, 0) * level.height))
            level.update()


def parse_args():
    """Parse user arguments and return as parser object.

    Returns:
        Parser object with arguments as attributes.
    """
    parser = argparse.ArgumentParser(
            description='Test basic Kphue functionality.')
    parser.add_argument('-i', '--infinite', action='store_true',
            help='Enable infinite.')

    parser.add_argument('-k', '--kphue', action='store_true',
            help='Enable kphue.')
    parser.add_argument('-b', '--bridge',
            help='IP of Bridge.')
    parser.add_argument('-n', '--l1',
            help='Name of a light that exists on the bridge.')

    parser.add_argument('-L', '--loglevel', choices=LOG_LEVELS,
            default=DEFAULT_LOG_LEVEL, help='Set the logging level.')
    args = parser.parse_args()
    return args


def set_orb(orb, param, value):
    """Set a Light value.

    Args:
        orb: Light object to set.
        param: Light parameter to set.
        value: Value of light parameter.
    """
    if orb:
        orb.set(param, value)


def main():
    """Main script.
    """
    exit_code = 0
    #To play music, simply select and play
    #pygame.mixer.music.load('Track1.mp3')
    #pygame.mixer.music.play()

    backdrop = Background(('far', 'near'), BOARD, -6)
    y_half = BOARD_HEIGHT / 2
    player = Player('default', BOARD, 10, y_half)

    game_over = False
    increase_counter = 0
    enemies = pygame.sprite.Group()
    enemy_count = DEFAULT_ENEMIES
    while not game_over:
        BOARD.fill((10, 0, 15))
        backdrop.update()

        if len(enemies) < enemy_count:
            new_enemy = Enemy('manta', BOARD)
            enemies.add(new_enemy)

        intent = player.get_input()
        player.update()

        enemies_gone = [enemy for enemy in enemies
                        if enemy.x_pos < -enemy.width]
        enemies.remove(enemies_gone)
        enemies.update()

        enemies_collided = pygame.sprite.spritecollide(player, enemies, True)
        if enemies_collided:
            print('Ouch')
            player.x_pos -= 5
            increase_counter = 0

        increase_counter += 1
        if increase_counter > INCREASE_TIME * FRAME_RATE:
            increase_counter = 0
            player.x_pos += 5
            enemy_count += 1

        if intent:
            game_over = True

        CLOCK.tick(FRAME_RATE)
        pygame.display.flip()

    return exit_code


if __name__ == '__main__':
    ARGS = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        level=getattr(logging, ARGS.loglevel))

    pygame.init()
    BOARD = pygame.display.set_mode(BOARD_SIZE)
    CLOCK = pygame.time.Clock()
    IMAGES = ImageStore(os.path.join(sys.path[0], 'images'), 'png')

    LIGHT1 = None
    if ARGS.kphue:
        import kphue
        my_bridge = kphue.Bridge(ARGS.bridge)
        if ARGS.l1:
            LIGHT1 = my_bridge.get_light(ARGS.l1)
            LOGGER.debug('Light found: %s', LIGHT1)
            set_orb(LIGHT1, 'on', True)
            set_orb(LIGHT1, 'rgb', (0, 0, 255))

    exit_code = main()

    if LIGHT1:
        set_orb(LIGHT1, 'on', False)

    pygame.quit()
    sys.exit(exit_code)
