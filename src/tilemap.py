import pygame
import csv
import os

from src.tile import Tile
from src.coin import Coin
from src.enemy import Skeleton
from src.goal import Goal

# TODO: animate tiles, store tiles in a separate list and draw those every couple of frames


class TileMap():
    def __init__(self, game, filename):
        self.game = game
        self.tile_size = 16
        self.start_x, self.start_y = 60, 160
        self.coins = []
        self.tiles = []
        self.decors = []
        self.enemies = []
        self.goal = ''
        self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface, camera):
        surface.blit(self.map_surface,
                     (0 - camera.offset.x, 0 - camera.offset.y))

    def load_map(self):
        for tile in self.tiles:
            tile.draw_tile(self.map_surface)

        for decor in self.decors:
            self.map_surface.blit(decor[0], (decor[1], decor[2]))

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))

        return map

    def load_tiles(self, filename):
        map = self.read_csv(filename)

        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    self.decors.append([pygame.image.load('assets/tiles/decor.png'),
                                       x * self.tile_size, y * self.tile_size])
                elif tile == '673':
                    self.tiles.append(Tile('assets/tiles/grass.png',
                                           x * self.tile_size, y * self.tile_size))
                elif tile == '721':
                    self.tiles.append(Tile('assets/tiles/dirt.png', x *
                                           self.tile_size, y * self.tile_size))
                elif tile == '3':
                    self.coins.append(
                        Coin(self.game, x * self.tile_size, y * self.tile_size))
                elif tile == '666':
                    self.enemies.append(Skeleton(self.game, x * self.tile_size, y * self.tile_size))
                elif tile == '999':
                    self.goal = Goal(self.game, x * self.tile_size, y * self.tile_size)
                elif tile == '5':
                    self.game.tree_location = [x * self.tile_size, y * self.tile_size]
                    # self.game.canvas.blit(pygame.image.load('assets/tiles/tree.png'), (x * self.tile_size, y * self.tile_size))

                x += 1  # move to the next tile in the row
            y += 1  # move to the next row

        self.map_w, self.map_h = x * self.tile_size, y * \
            self.tile_size  # store the size of the map
