import pygame


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w = self.game.CANVAS_W / 2
        self.mid_h = self.game.CANVAS_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(pygame.transform.scale(
            self.game.canvas, (self.game.WINDOW_W, self.game.WINDOW_H)), (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'start'
        self.startx = self.mid_w
        self.starty = self.mid_h + 30
        self.optionsx = self.mid_w
        self.optionsy = self.mid_h + 50
        self.creditsx = self.mid_w
        self.creditsy = self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.canvas.fill(self.game.BLACK)
            # self.game.canvas.blit(self.game.background, (0, 0))
            self.game.draw_text(
                'Tree Runner', 20, self.game.CANVAS_W / 2, self.game.CANVAS_H / 2 - 50)
            self.game.draw_text('Start Game', 20, self.startx, self.starty)
            self.game.draw_text('Options', 20, self.optionsx, self.optionsy)
            self.game.draw_text('Credits', 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'start':
                self.cursor_rect.midtop = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = 'options'
            elif self.state == 'options':
                self.cursor_rect.midtop = (
                    self.creditsx + self.offset, self.creditsy)
                self.state = 'credits'
            elif self.state == 'credits':
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = 'start'
        elif self.game.UP_KEY:
            if self.state == 'start':
                self.cursor_rect.midtop = (
                    self.creditsx + self.offset, self.creditsy)
                self.state = 'credits'
            elif self.state == 'options':
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = 'start'
            elif self.state == 'credits':
                self.cursor_rect.midtop = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = 'options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'start':
                self.game.playing = True
            elif self.state == 'options':
                self.game.current_menu = self.game.options_menu
            elif self.state == 'credits':
                self.game.current_menu = self.game.credits_menu
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'volume'
        self.volx = self.mid_w
        self.voly = self.mid_h + 20
        self.controlsx = self.mid_w
        self.controlsy = self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            # self.game.canvas.blit(self.game.background, (0, 0))
            self.game.canvas.fill(self.game.BLACK)
            self.game.draw_text(
                'Options', 20, self.game.CANVAS_W / 2, self.game.CANVAS_H / 2 - 50)
            self.game.draw_text('Volume', 15, self.volx, self.voly)
            self.game.draw_text('Controls', 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.current_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'volume':
                self.state = 'controls'
                self.cursor_rect.midtop = (
                    self.controlsx + self.offset, self.controlsy)
            elif self.state == 'controls':
                self.state = 'volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # TODO: Create a volume menu and a controls menu
            pass

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.current_menu = self.game.main_menu
                self.run_display = False
            # self.game.canvas.blit(self.game.background, (0, 0))
            self.game.canvas.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.CANVAS_W/2, self.game.CANVAS_H/2 - 50)
            self.game.draw_text('christianduenas', 15, self.game.CANVAS_W/2, self.game.CANVAS_H/2 + 10)
            self.game.draw_text('dafluffypotato', 15, self.game.CANVAS_W/2, self.game.CANVAS_H/2 + 30)
            self.blit_screen()
