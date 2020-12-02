import pygame
import csv
import os

from src.tile import Tile

# TODO: animate tiles, store tiles in a separate list and draw those every couple of frames


class TileMap():
    def __init__(self, filename):
        self.tile_size = 16
        self.start_x, self.start_y = 60, 160
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface, camera):
        surface.blit(self.map_surface, (0 - camera.offset.x, 0 - camera.offset.y))

    def load_map(self):
        for tile in self.tiles:
            tile.draw_tile(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))

        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)

        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '1':
                    tiles.append(Tile('assets/tiles/grass.png',
                                      x * self.tile_size, y * self.tile_size))
                elif tile == '2':
                    tiles.append(Tile('assets/tiles/dirt.png', x *
                                      self.tile_size, y * self.tile_size))
                x += 1  # move to the next tile in the row
            y += 1  # move to the next row

        self.map_w, self.map_h = x * self.tile_size, y * \
            self.tile_size  # store the size of the map

        return tiles
