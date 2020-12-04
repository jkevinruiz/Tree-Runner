import pygame

class Goal():
    def __init__(self, game, x, y):
        self.game = game
        self.type = 'goal'
        self.image = pygame.image.load('assets/tiles/tree.png')
        self.rect = self.image.get_rect()
        self.rect.x = x - 46
        self.rect.y = y - 44

    
    def draw(self):
        pygame.draw.rect(self.game.canvas, (255, 0, 0), (self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y, self.rect.w, self.rect.h), 2)
        self.game.canvas.blit(self.image, (self.rect.x - self.game.camera.offset.x , self.rect.y))