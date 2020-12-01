import sys
import pygame

from pygame.locals import *
from src.menu import CreditsMenu, MainMenu, OptionsMenu
from src.camera import Camera, Auto
from src.tilemap import TileMap
from src.player import Player

pygame.init()


class Game():
    def __init__(self):
        self.running = True
        self.playing = False
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.WINDOW_W = 600
        self.WINDOW_H = 400
        self.CANVAS_W = 384
        self.CANVAS_H = 216
        self.TARGET_FPS = 60
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.font_name = 'assets/font/8-BIT WONDER.TTF'
        self.canvas = pygame.Surface((self.CANVAS_W, self.CANVAS_H))
        self.window = pygame.display.set_mode((self.WINDOW_W, self.WINDOW_H))
        self.clock = pygame.time.Clock()
        self.map = TileMap('map.csv')
        self.player = Player()
        self.camera = Camera(self.player)
        self.auto_scroll = Auto(self.camera, self.player)
        self.camera.set_method(self.auto_scroll)
        self.player.position.x = self.map.start_x
        self.player.position.y = self.map.start_y
        self.background = pygame.image.load(
            'assets/background/background.png').convert()
        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.current_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            delta_time = self.clock.tick(60) * .001 * self.TARGET_FPS
            delta_time = min(delta_time, 3)

            self.check_events()
            if self.START_KEY:
                self.playing = False

            self.player.update(delta_time, self.map.tiles)
            self.camera.scroll()
            self.canvas.fill(self.BLACK)
            # self.draw_text('Thanks for Playing', 20,
            #                self.CANVAS_W/2, self.CANVAS_H/2)
            self.canvas.blit(self.background, (0, 0))
            self.map.draw_map(self.canvas)
            self.player.draw_player(self.canvas)
            self.window.blit(pygame.transform.scale(
                self.canvas, (self.WINDOW_W, self.WINDOW_H)), (0, 0))
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                self.playing = False
                self.current_menu.run_display = False
                # pygame.quit()
                # sys.exit()

            if event.type == KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == K_UP:
                    self.UP_KEY = True

                if event.key == K_LEFT:
                    self.player.LEFT_KEY, self.player.FACING_LEFT = True, True
                elif event.key == K_RIGHT:
                    self.player.RIGHT_KEY, self.player.FACING_LEFT = True, False
                elif event.key == K_SPACE:
                    self.player.jump()

            if event.type == KEYUP:
                # if event.key == pygame.K_RETURN:
                #     self.START_KEY = False
                # if event.key == K_BACKSPACE:
                #     self.BACK_KEY = False
                # if event.key == pygame.K_DOWN:
                #     self.DOWN_KEY = False
                # if event.key == K_UP:
                #     self.UP_KEY = False

                if event.key == K_LEFT:
                    self.player.LEFT_KEY = False
                elif event.key == K_RIGHT:
                    self.player.RIGHT_KEY = False
                elif event.key == K_SPACE:
                    if self.player.isJumping:
                        self.player.velocity.y *= .25
                        self.player.isJumping = False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.canvas.blit(text_surface, text_rect)

    def reset_keys(self):
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
