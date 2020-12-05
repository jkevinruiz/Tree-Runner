import sys
import random
import pygame

from pygame.locals import *
from src.menu import MainMenu, PauseScreen, GameOver, GameComplete
from src.camera import Camera, Auto
from src.tilemap import TileMap
from src.player import Player

class Game():
    def __init__(self):
        # init
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)

        # constants
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.window_w = 800
        self.window_h = 500
        self.canvas_w = 384
        self.canvas_h = 248
        self.target_fps = 60
        self.dt = 1
        self.title = 'Tree Runner'
        self.font_name = 'assets/font/8-BIT WONDER.TTF'
        self.clock = pygame.time.Clock()
        self.canvas = pygame.Surface((self.canvas_w, self.canvas_h))
        self.window = pygame.display.set_mode((self.window_w, self.window_h))
        self.background_image = pygame.image.load('assets/background/background.png').convert()
        self.background = pygame.transform.scale(self.background_image, (self.canvas_w, self.canvas_h))
        self.heart = pygame.image.load('assets/hud/heart.png')
        self.finish = pygame.image.load('assets/hud/flag.png')
        self.enemy = pygame.image.load('assets/hud/enemy.png')
        self.coin = pygame.transform.scale(
            pygame.image.load('assets/hud/gold.png'), (16, 16))

        # state
        self.running = True
        self.playing = False
        self.complete = False
        self.pause = False

        # keys
        self.up_key = False
        self.down_key = False
        self.enter_key = False
        self.back_key = False
        self.esc_key = False
        self.p_key = False

        # hud
        self.lives = 10
        self.gold = 0
        self.kills = 0
        self.distance = 0

        # player
        self.player = Player(self)
        self.alive = True
        
        # player spawn location
        self.spawn_x = 16
        self.spawn_y = 100
        self.player.position.x = self.spawn_x 
        self.player.position.y = self.spawn_y

        # save location
        self.save_x = 16
        self.save_y = 100
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 0

        # camera
        self.camera = Camera(self.player)
        self.auto_scroll = Auto(self.camera, self.player)
        self.camera.set_method(self.auto_scroll)
        self.start_scrolling = False

        # map
        self.map = TileMap(self, 'assets/maps/level 1.csv')

        # menu
        self.main_menu = MainMenu(self)
        self.pause_screen = PauseScreen(self)
        self.gameover_screen = GameOver(self)
        self.gamecomplete_screen = GameComplete(self)
        self.current_menu = self.main_menu

    def game_loop(self):
        self.load_music()
        while self.playing:
            self.dt = min(self.clock.tick(60) * .001 * self.target_fps, 3)

            self.check_events()

            if self.pause:
                self.pause_screen.display_menu()
                self.pause = False
                self.load_music()
            
            if self.lives < 1:
                self.current_menu = self.gameover_screen
                self.playing = False
            
            if self.complete:
                self.current_menu = self.gamecomplete_screen
                self.playing = False

            if self.player.rect.x + self.player.rect.w/2 <= self.camera.offset.x or self.player.rect.top >= self.canvas_h:
                if self.lives != 0:
                    self.lives -= 1

                if self.lives >= 1: 
                    self.respawn()
            
            if self.player.position.x >= 200:
                self.start_scrolling = True
            elif self.player.position.x < 200:
                self.start_scrolling = False
            
            if self.start_scrolling:
                if self.player.rect.x < 800:
                    self.camera.scroll_speed = 0.8
                if self.player.rect.x > 800:
                    self.camera.scroll_speed = 1.0
            
            # player movement
            self.player.update()

            # camera movement
            self.camera.scroll()
            # self.canvas.fill(self.black)
            # self.canvas.blit(pygame.transform.scale(self.background, (384, 248)), (0, 0 - self.camera.offset.y))
            # self.map.draw()
            # for object in self.map.objects:
            #     object.draw()

            # for enemy in self.map.enemies:
            #     if random.randint(0, 5000) == 1:
            #         enemy.state = 'idle'
            #     enemy.draw_skeleton()

            # draw
            self.draw()
            

            # self.player.draw()
            self.canvas.blit(self.heart, (8, 2))
            self.draw_text(f' x {str(self.lives)}', 10, 40, 9)
            self.canvas.blit(self.coin, (70, 2))
            self.draw_text(f' x {str(self.gold)}', 10, 100, 9)
            self.canvas.blit(self.finish, (128, 2))
            self.draw_text(f' x {str(self.distance)} px', 10, 190, 9)
            self.window.blit(pygame.transform.scale(
                self.canvas, (self.window_w, self.window_h)), (0, 0))
                

            pygame.display.update()
            self.reset_keys()
        pygame.mixer.music.stop()    
    
    def draw(self):
        # clear screen
        self.canvas.fill(self.black)
        # draw background
        self.canvas.blit(pygame.transform.scale(self.background, (self.canvas_w, self.canvas_h)), (0, 0))
        # draw floor and ceiling
        self.map.draw()
        # draw objects like coins, traps, save points, and goal
        for object in self.map.objects:
            object.draw()
        # draw enemies like skeleton
        for enemy in self.map.enemies:
            # set state idle or walking
            if random.randint(0, 999) == 19:
                enemy.state = 'idle'
            enemy.draw_skeleton()
        # draw player
        self.player.draw()


    def draw_hud(self):
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                self.playing = False
                self.current_menu.run_display = False
                # pygame.quit()
                # sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.playing = False
                    self.pause_screen.run_display = False
                if event.key == pygame.K_RETURN:
                    self.enter_key = True
                if event.key == K_BACKSPACE:
                    self.back_key = True
                if event.key == pygame.K_DOWN:
                    self.down_key = True
                if event.key == K_UP:
                    self.up_key = True
                if event.key == K_p:
                    if self.pause:
                        self.pause_screen.run_display = False
                    self.pause = True
                if event.key == K_r:
                    if self.lives < 1:
                        print('restarting game')

                if event.key == K_LEFT:
                    self.player.left_key, self.player.flip = True, True
                elif event.key == K_RIGHT:
                    self.player.right_key, self.player.flip = True, False
                elif event.key == K_SPACE:
                    self.player.jump()
                elif event.key == K_LSHIFT:
                    self.player.lshift_key = True

            if event.type == KEYUP:
                if event.key == K_LEFT:
                    self.player.left_key = False
                elif event.key == K_RIGHT:
                    self.player.right_key = False
                elif event.key == K_LSHIFT:
                    self.player.lshift_key = False
                elif event.key == K_SPACE:
                    if self.player.is_jumping:
                        self.player.velocity.y *= .25
                        self.player.is_jumping = False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.white)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.canvas.blit(text_surface, text_rect)
    
    def game_over(self):
        if self.lives < 1:
            self.playing = False
            self.lives = 10
            self.current_menu = self.gameover_screen

    def reset_keys(self):
        self.up_key = False
        self.down_key = False
        self.enter_key = False
        self.back_key = False

    def respawn(self):
        self.player = Player(self)
        self.player.position.x = self.save_x
        self.player.position.y = self.save_y
        # self.camera.offset.x = self.camera_x
        # self.camera.offset_float.x = self.camera_x
        self.camera.reset(self.camera_speed, self.camera_x, self.camera_x)
        self.start_scrolling = False

    def reset(self):
        # state
        self.running = True
        self.playing = False
        self.complete = False
        self.pause = False

        # keys
        self.up_key = False
        self.down_key = False
        self.enter_key = False
        self.back_key = False
        self.esc_key = False
        self.p_key = False

        # hud
        self.lives = 10
        self.gold = 0
        self.kills = 0
        self.distance = 0

        # player
        self.player = Player(self)
        self.alive = True
        
        # player spawn location
        self.spawn_x = 16
        self.spawn_y = 100
        self.player.position.x = self.spawn_x 
        self.player.position.y = self.spawn_y

        # save location
        self.save_x = 16
        self.save_y = 100
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 0

        # camera
        self.camera = Camera(self.player)
        self.auto_scroll = Auto(self.camera, self.player)
        self.camera.set_method(self.auto_scroll)
        self.start_scrolling = False

        # map
        self.map = TileMap(self, 'assets/maps/level 1.csv')

        # menu
        self.main_menu = MainMenu(self)
        self.pause_screen = PauseScreen(self)
        self.gameover_screen = GameOver(self)
        self.gamecomplete_screen = GameComplete(self)
        self.current_menu = self.main_menu
    
    def load_music(self):
        pygame.mixer.music.load('assets/bgm/track4.ogg')
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(-1)
    
    def quit(self):
        pygame.quit()
        sys.exit()

    
    # def update_distance(self):
    #     self.distance = int(self.tree_location[0] - self.player.position.x)