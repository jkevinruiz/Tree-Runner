import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)


class Save():
    def __init__(self, game, x, y):
        self.game = game
        self.type = 'save'

        # image
        self.image = pygame.image.load('assets/tiles/save.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # sfx
        self.save_sound = pygame.mixer.Sound('assets/sfx/save.ogg')

    def draw(self):
        self.game.canvas.blit(
            self.image, (self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y))
