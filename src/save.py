import pygame


class Save():
    def __init__(self, game, x, y):
        self.game = game
        self.type = 'save'
        self.image = pygame.image.load('assets/tiles/save.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        self.game.canvas.blit(self.image, (self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y))
