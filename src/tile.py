import pygame

class Tile():
    def __init__(self, path, vflip, x, y):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.flip(self.image, False, vflip)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


