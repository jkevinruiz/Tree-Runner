import pygame
import csv
import os

from src.tile import Tile
from src.coin import Coin
from src.trap import Trap
from src.goal import Goal
from src.save import Save
from src.enemy import Skeleton


class TileMap():
    def __init__(self, game, filename):
        self.game = game

        self.tile_size = 16
        self.vflip = False

        self.tiles = [] # contains floor and ceiling tiles
        self.objects = [] # contains goal point, coins, saved points
        self.enemies = [] # contains enemies
        self.goal = 6000

        self.create_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load()

    def draw(self):
        self.game.canvas.blit(
            self.map_surface, (0 - self.game.camera.offset.x, 0 - self.game.camera.offset.y))

    def load(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

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
                if tile == '673':
                    self.tiles.append(Tile('assets/tiles/grass.png', False,
                                           x * self.tile_size, y * self.tile_size))
                elif tile == '674':
                    self.tiles.append(Tile('assets/tiles/grass.png', True,
                                           x * self.tile_size, y * self.tile_size))
                elif tile == '721':
                    self.tiles.append(Tile('assets/tiles/dirt.png', False, x *
                                           self.tile_size, y * self.tile_size))
                elif tile == '722':
                    self.tiles.append(Tile('assets/tiles/dirt.png', True,
                                           x * self.tile_size, y * self.tile_size))
                elif tile == '702':
                    self.enemies.append(
                        Skeleton(self.game, x * self.tile_size, y * self.tile_size))
                elif tile == '900':
                    self.objects.append(
                        Coin(self.game, x * self.tile_size, y * self.tile_size))
                elif tile == '895':
                    self.objects.append(Trap(self.game, False, x * self.tile_size, y * self.tile_size))
                elif tile == '847':
                    self.objects.append(Trap(self.game, True, x * self.tile_size, y * self.tile_size))
                elif tile == '937':
                    self.goal = x * self.tile_size
                    self.objects.append(Goal(
                        self.game, x * self.tile_size, y * self.tile_size))
                elif tile == '558':
                    self.objects.append(Save(self.game, x * self.tile_size, y * self.tile_size))

                x += 1
            y += 1

        self.map_w=x * self.tile_size
        self.map_h=y * self.tile_size
