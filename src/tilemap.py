import pygame
import csv
import os

from src.tile import Tile
from src.coin import Coin
from src.enemy import Skeleton
from src.goal import Goal


class TileMap():
    def __init__(self, game, filename):
        self.game = game

        self.tile_size = 16
        self.vflip = False

        self.goal = []
        self.tiles = []
        self.coins = []
        self.enemies = []

        self.create_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load()

    # def draw(self, surface, camera):
    #     surface.blit(self.map_surface,
    #                  (0 - camera.offset.x, 0 - camera.offset.y))
    def draw(self):
        self.game.canvas.blit(
            self.map_surface, (0 - self.game.camera.offset.x, 0 - self.game.camera.offset.y))

    def load(self):
        for tile in self.tiles:
            tile.draw_tile(self.map_surface)

    def read(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))

        return map

    def create_tiles(self, filename):
        map = self.read(filename)

        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                # if tile == '0':
                #     self.decors.append([pygame.image.load('assets/tiles/decor.png'),
                #                        x * self.tile_size, y * self.tile_size])
                if tile == '673':
                    self.tiles.append(Tile('assets/tiles/grass.png',
                                           x * self.tile_size, y * self.tile_size))
                elif tile == '721':
                    self.tiles.append(Tile('assets/tiles/dirt.png', x *
                                           self.tile_size, y * self.tile_size))
                elif tile == '3':
                    self.coins.append(
                        Coin(self.game, x * self.tile_size, y * self.tile_size))
                elif tile == '666':
                    self.enemies.append(
                        Skeleton(self.game, x * self.tile_size, y * self.tile_size))
                elif tile == '999':
                    self.goal = Goal(
                        self.game, x * self.tile_size, y * self.tile_size)
                elif tile == '5':
                    self.game.tree_location = [
                        x * self.tile_size, y * self.tile_size]

                x += 1
            y += 1 

        self.map_w = x * self.tile_size
        self.map_h = y * self.tile_size