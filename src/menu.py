import pygame


class Menu():
    def __init__(self, game):
        self.game = game

        self.run_display = True

        self.offset = -100
        self.middle_w = self.game.canvas_w / 2
        self.middle_h = self.game.canvas_h / 2
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
    
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.game.font_name, size)
        surface = font.render(text, True, (255, 255, 255))
        rect = surface.get_rect()
        rect.center = (x, y)

        self.game.canvas.blit(surface, rect)

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(pygame.transform.scale(
            self.game.canvas, (self.game.window_w, self.game.window_h)), (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = 'start'

        self.start_x = self.middle_w
        self.start_y = self.middle_h + 30
        self.restart_x = self.middle_w
        self.restart_y = self.middle_h + 50
        self.quit_x = self.middle_w
        self.quit_y = self.middle_h + 70
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)

    def display_menu(self):
        pygame.mixer.music.load('assets/bgm/track1.ogg')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.canvas.fill(self.game.black)
            self.draw_text(
                'Tree Runner', 20, self.game.canvas_w / 2, self.game.canvas_h / 2 - 50)
            self.draw_text('Continue', 20, self.start_x, self.start_y)
            self.draw_text('Restart', 20, self.restart_x, self.restart_y)
            self.draw_text('Quit', 20, self.quit_x, self.quit_y)
            self.draw_cursor()
            self.blit_screen()
        pygame.mixer.music.stop()

    def move_cursor(self):
        if self.game.down_key:
            if self.state == 'start':
                self.cursor_rect.midtop = (
                    self.restart_x + self.offset, self.restart_y)
                self.state = 'restart'
            elif self.state == 'restart':
                self.cursor_rect.midtop = (
                    self.quit_x + self.offset, self.quit_y)
                self.state = 'quit'
            elif self.state == 'quit':
                self.cursor_rect.midtop = (
                    self.start_x + self.offset, self.start_y)
                self.state = 'start'
        elif self.game.up_key:
            if self.state == 'start':
                self.cursor_rect.midtop = (
                    self.quit_x + self.offset, self.quit_y)
                self.state = 'quit'
            elif self.state == 'restart':
                self.cursor_rect.midtop = (
                    self.start_x + self.offset, self.start_y)
                self.state = 'start'
            elif self.state == 'quit':
                self.cursor_rect.midtop = (
                    self.restart_x + self.offset, self.restart_y)
                self.state = 'restart'

    def check_input(self):
        self.move_cursor()
        if self.game.enter_key:
            if self.state == 'start':
                if self.game.lives < 1:
                    # TODO: reset the game
                    self.game.reset()
                self.game.playing = True
            elif self.state == 'restart':
                # TODO: reset the game
                self.game.reset()
                self.game.playing = True
            elif self.state == 'quit':
                self.game.quit()

            self.run_display = False

class PauseScreen(Menu):
    def __init__(self, game):
        super().__init__(game)
    
    def display_menu(self):
        pygame.mixer.music.load('assets/bgm/track3.ogg')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.run_display = True
        while self.run_display:
            self.game.check_events()

            self.game.canvas.fill(self.game.black)
            self.draw_text('Pause', 20, self.middle_w, self.middle_h - 50)
            self.draw_text('P to continue', 10, self.middle_w, self.middle_h)
            self.draw_text('ESC to title screen', 10 , self.middle_w, self.middle_h + 30)
            self.blit_screen()
        pygame.mixer.music.stop()
    
class GameOver(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = 'restart'

        self.restart_x = self.middle_w
        self.restart_y = self.middle_h + 30
        self.quit_x = self.middle_w
        self.quit_y = self.middle_h + 50
        self.cursor_rect.midtop = (self.restart_x + self.offset, self.restart_y)
    
    def display_menu(self):
        pygame.mixer.music.load('assets/bgm/track6.ogg')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.canvas.fill(self.game.black)
            self.draw_text('Game Over', 20, self.middle_w, self.middle_h - 50)
            self.draw_text('Restart', 20, self.restart_x, self.restart_y)
            self.draw_text('Quit', 20, self.quit_x, self.quit_y)
            self.draw_cursor()
            self.blit_screen()
        pygame.mixer.music.stop()
    
    def move_cursor(self):
        if self.game.down_key:
            if self.state == 'restart':
                self.cursor_rect.midtop = (
                    self.quit_x + self.offset, self.quit_y)
                self.state = 'quit'
            elif self.state == 'quit':
                self.cursor_rect.midtop = (
                    self.restart_x + self.offset, self.restart_y)
                self.state = 'restart'
        elif self.game.up_key:
            if self.state == 'start':
                self.cursor_rect.midtop = (
                    self.quit_x + self.offset, self.quit_y)
                self.state = 'quit'
            elif self.state == 'quit':
                self.cursor_rect.midtop = (
                    self.restart_x + self.offset, self.restart_y)
                self.state = 'restart'

    def check_input(self):
        self.move_cursor()
        if self.game.enter_key:
            if self.state == 'restart':
                self.game.reset()
                self.game.playing = True
            elif self.state == 'quit':
                self.game.quit()
            self.run_display = False

class GameComplete(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = 'restart'

        self.restart_x = self.middle_w
        self.restart_y = self.middle_h + 30
        self.quit_x = self.middle_w
        self.quit_y = self.middle_h + 50
        self.cursor_rect.midtop = (self.restart_x + self.offset, self.restart_y)
    
    def display_menu(self):
        pygame.mixer.music.load('assets/bgm/track2.ogg')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.canvas.fill(self.game.black)
            self.draw_text('Game Won', 20, self.middle_w, self.middle_h - 80)
            self.draw_text('Thanks for Playing', 20, self.middle_w, self.middle_h - 30)
            self.draw_text('Restart', 20, self.restart_x, self.restart_y)
            self.draw_text('Quit', 20, self.quit_x, self.quit_y)
            self.draw_cursor()
            self.blit_screen()
        pygame.mixer.music.stop()
    
    def move_cursor(self):
        if self.game.down_key:
            if self.state == 'restart':
                self.cursor_rect.midtop = (
                    self.quit_x + self.offset, self.quit_y)
                self.state = 'quit'
            elif self.state == 'quit':
                self.cursor_rect.midtop = (
                    self.restart_x + self.offset, self.restart_y)
                self.state = 'restart'
        elif self.game.up_key:
            if self.state == 'start':
                self.cursor_rect.midtop = (
                    self.quit_x + self.offset, self.quit_y)
                self.state = 'quit'
            elif self.state == 'quit':
                self.cursor_rect.midtop = (
                    self.restart_x + self.offset, self.restart_y)
                self.state = 'restart'

    def check_input(self):
        self.move_cursor()
        if self.game.enter_key:
            if self.state == 'restart':
                    self.game.reset()
                    self.game.playing = True
            elif self.state == 'quit':
                self.game.quit()
            self.run_display = False