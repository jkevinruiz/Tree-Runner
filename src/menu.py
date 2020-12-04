import pygame


class Menu():
    def __init__(self, game):
        self.game = game

        self.run_display = True

        self.offset = -100
        self.middle_w = self.game.canvas_w / 2
        self.middle_h = self.game.canvas_h / 2
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(pygame.transform.scale(
            self.game.canvas, (self.game.window_w, self.game.window_h)), (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'start'

        self.start_x = self.middle_w
        self.start_y = self.middle_h + 30
        self.restart_x = self.middle_w
        self.restart_y = self.middle_h + 50
        # self.creditsx = self.middle_w
        # self.creditsy = self.middle_h + 70
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.canvas.fill(self.game.black)
            # self.game.canvas.blit(self.game.background, (0, 0))
            self.game.draw_text(
                'Tree Runner', 20, self.game.canvas_w / 2, self.game.canvas_h / 2 - 50)
            self.game.draw_text('Continue', 20, self.start_x, self.start_y)
            self.game.draw_text('Restart', 20, self.restart_x, self.restart_y)
            # self.game.draw_text('Credits', 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.down_key:
            if self.state == 'start':
                self.cursor_rect.midtop = (
                    self.restart_x + self.offset, self.restart_y)
                self.state = 'restart'
            elif self.state == 'restart':
                self.cursor_rect.midtop = (
                    self.start_x + self.offset, self.start_y)
                self.state = 'start'
        elif self.game.up_key:
            if self.state == 'start':
                self.cursor_rect.midtop = (
                    self.restart_x + self.offset, self.restart_y)
                self.state = 'restart'
            elif self.state == 'restart':
                self.cursor_rect.midtop = (
                    self.start_x + self.offset, self.start_y)
                self.state = 'start'
            # elif self.state == 'credits':
            #     self.cursor_rect.midtop = (
            #         self.restart_x + self.offset, self.restart_y)
            #     self.state = 'restart'

    def check_input(self):
        self.move_cursor()
        if self.game.enter_key:
            if self.state == 'start':
                if self.game.lives == 0:
                    print('restarting')
                    self.game.restart_game()
                self.game.playing = True
            elif self.state == 'restart':
                # self.game.current_menu = self.game.options_menu
                self.game.restart_game()
                self.game.playing = True
            elif self.state == 'credits':
                self.game.current_menu = self.game.credits_menu
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'volume'
        self.volx = self.middle_w
        self.voly = self.middle_h + 20
        self.controlsx = self.middle_w
        self.controlsy = self.middle_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            # self.game.canvas.blit(self.game.background, (0, 0))
            self.game.canvas.fill(self.game.black)
            self.game.draw_text(
                'Options', 20, self.game.canvas_w / 2, self.game.canvas_h / 2 - 50)
            self.game.draw_text('Volume', 15, self.volx, self.voly)
            self.game.draw_text('Controls', 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.back_key:
            self.game.current_menu = self.game.main_menu
            self.run_display = False
        elif self.game.up_key or self.game.down_key:
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
            if self.game.START_KEY or self.game.back_key:
                self.game.current_menu = self.game.main_menu
                self.run_display = False
            # self.game.canvas.blit(self.game.background, (0, 0))
            self.game.canvas.fill(self.game.black)
            self.game.draw_text('Credits', 20, self.game.canvas_w/2, self.game.canvas_h/2 - 50)
            self.game.draw_text('christianduenas', 15, self.game.canvas_w/2, self.game.canvas_h/2 + 10)
            self.game.draw_text('dafluffypotato', 15, self.game.canvas_w/2, self.game.canvas_h/2 + 30)
            self.blit_screen()
