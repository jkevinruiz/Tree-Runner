import os
import sys
import pygame

from pygame.locals import *
from src.tilemap import TileMap
from src.player import Player

WINDOW_W, WINDOW_H = 600, 400
CANVAS_W, CANVAS_H = 384, 216
TARGET_FPS = 60

pygame.init()

window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
canvas = pygame.Surface((CANVAS_W, CANVAS_H))
clock = pygame.time.Clock()

map = TileMap('map.csv')
player = Player()
player.position.x , player.position.y = map.start_x, map.start_y


background_image = pygame.image.load(
    'assets/background/background.png').convert()


def game_loop():
    running = True

    while running:
        # frame rate independence to compensate for when fps is dropping
        delta_time = clock.tick(60) * .001 * TARGET_FPS

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player.LEFT_KEY, player.FACING_LEFT = True, True
                elif event.key == K_RIGHT:
                    player.RIGHT_KEY, player.FACING_LEFT = True, False
                elif event.key == K_SPACE:
                    player.jump()
            
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    player.LEFT_KEY = False
                elif event.key == K_RIGHT:
                    player.RIGHT_KEY =  False
                elif event.key == K_SPACE:
                    if player.isJumping:
                        player.velocity.y *= .25
                        player.isJumping = False

        player.update(delta_time, map.tiles)
        # canvas.fill((0, 0, 0))
        canvas.blit(background_image, (0, 0))
        map.draw_map(canvas)
        player.draw_player(canvas)
        # canvas.blit(player.image, player.rect)
        window.blit(pygame.transform.scale(
            canvas, (WINDOW_W, WINDOW_H)), (0, 0))
        pygame.display.update()


# game_loop()
