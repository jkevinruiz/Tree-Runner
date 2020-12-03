
import random
import pygame

from pygame.locals import *
from src.menu import CreditsMenu, MainMenu, OptionsMenu
from src.camera import Camera, Auto, Follow
from src.coin import Coin
from src.tilemap import TileMap
from src.player import Player

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
class Game():
    def __init__(self):
        self.running = True
        self.playing = False
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.WINDOW_W = 800
        self.WINDOW_H = 500
        self.CANVAS_W = 384
        self.CANVAS_H = 248
        self.TITLE = 'Tree Runner'
        self.TARGET_FPS = 60
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GOLD_COUNT = 0
        self.life = 3
        self.start_scrolling = False
        self.jump_sound = pygame.mixer.Sound('assets/sfx/mario_jump.ogg')
        pygame.mixer.music.load('assets/bgm/track4.ogg')
        pygame.mixer.music.play(-1)
        self.font_name = 'assets/font/8-BIT WONDER.TTF'
        self.canvas = pygame.Surface((self.CANVAS_W, self.CANVAS_H))
        self.window = pygame.display.set_mode((self.WINDOW_W, self.WINDOW_H))
        self.tree_location = [0, 0]
        self.clock = pygame.time.Clock()
        self.player = Player(self)
        self.camera = Camera(self.player)
        self.map = TileMap(self, 'assets/maps/Level 1_group.csv')
        self.coin_list = self.map.coins 
        self.enemy_list = self.map.enemies
        self.auto_scroll = Auto(self.camera, self.player)
        self.follow_scroll = Follow(self.camera, self.player)
        self.camera.set_method(self.auto_scroll)
        # self.camera.set_method(self.follow_scroll)
        self.player.position.x = 55 
        self.player.position.y = 100
        self.distance = int(self.tree_location[0] - self.player.position.x)
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
            
            if self.player.rect.x + self.player.rect.w/2 <= self.camera.offset.x or self.player.rect.top >= self.CANVAS_H:
                if self.life != 0:
                    self.life -= 1

                if self.life >= 1: 
                    self.respawn()
            
            if self.life == 0:
                self.playing = False
                # self.current_menu = self.main_menu
            
            if self.player.position.x >= 200:
                self.start_scrolling = True
            
            if self.start_scrolling:
                if self.player.rect.x < 800:
                    self.camera.scroll_speed = 0.8
                if self.player.rect.x > 800:
                    self.camera.scroll_speed = 1.0
                # if self.player.rect.x > 800:
                #     self.camera.scroll_speed += 0.001 
            
            
            
            # print(self.player.velocity.x)
            self.update_distance()
            print(self.camera.scroll_speed)

            self.player.update(delta_time, self.map.tiles, self.coin_list, self.enemy_list)
            # self.player.update(delta_time, self.map.tiles)
            self.camera.scroll()
            self.canvas.fill(self.BLACK)
            # self.draw_text('Thanks for Playing', 20,
            #                self.CANVAS_W/2, self.CANVAS_H/2)
            self.canvas.blit(pygame.transform.scale(self.background, (384, 248)), (0, 0 - self.camera.offset.y))
            self.map.draw_map(self.canvas, self.camera)
            # self.coin.draw_coin()
            for coin in self.coin_list:
                coin.draw_coin()
            for enemy in self.enemy_list:
                enemy.draw_skeleton()
            self.player.draw_player(self.canvas, self.camera)
            self.canvas.blit(pygame.image.load('assets/hud/heart.png'), (8, 2))
            self.draw_text(f' x {str(self.life)}', 10, 40, 9)
            self.canvas.blit(pygame.image.load('assets/hud/gold.png'), (70, 4))
            self.draw_text(f' x {str(self.GOLD_COUNT)}', 10, 100, 9)
            self.canvas.blit(pygame.transform.scale2x(pygame.image.load('assets/tiles/tree.png')), (self.tree_location[0] - self.camera.offset.x, self.tree_location[1] - self.camera.offset.y - 64))
            # self.draw_text(f'DISTANCE TO GOAL'){str(self.player.position.x - self.tree_location[0])} , 10, 125  9)
            self.canvas.blit(pygame.image.load('assets/hud/flag.png'), (128, 2))
            self.draw_text(f' x {str(self.distance)} px', 10, 190, 9)
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
                    self.jump_sound.play()
                    self.player.jump()
                elif event.key == K_LSHIFT:
                    self.player.LSHIFT_KEY = True

            if event.type == KEYUP:
            #     if event.key == pygame.K_RETURN:
            #         self.START_KEY = False
            #     if event.key == K_BACKSPACE:
            #         self.BACK_KEY = False
            #     if event.key == pygame.K_DOWN:
            #         self.DOWN_KEY = False
            #     if event.key == K_UP:
            #         self.UP_KEY = False

                if event.key == K_LEFT:
                    self.player.LEFT_KEY = False
                elif event.key == K_RIGHT:
                    self.player.RIGHT_KEY = False
                elif event.key == K_SPACE:
                    if self.player.isJumping:
                        self.player.velocity.y *= .25
                        self.player.isJumping = False
                elif event.key == K_LSHIFT:
                    self.player.LSHIFT_KEY = False

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

    def respawn(self):
        self.player = Player(self)
        self.player.position.x = 100
        self.player.position.y = 100
        self.camera.reset()
        self.start_scrolling = False

    def restart_game(self):
        self.player = Player(self)
        self.camera = Camera(self.player)
        self.map = TileMap(self, 'assets/maps/level_1_alpha.csv')
        self.coin_list = self.map.coins 
        self.auto_scroll = Auto(self.camera, self.player)
        self.follow_scroll = Follow(self.camera, self.player)
        self.camera.set_method(self.auto_scroll)
        # self.camera.set_method(self.follow_scroll)
        self.player.position.x = 32 
        self.player.position.y = 100
        self.life = 3
        self.GOLD_COUNT = 0
    
    def update_distance(self):
        self.distance = int(self.tree_location[0] - self.player.position.x)