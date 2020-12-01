import pygame

class Tile():
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw_tile(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


