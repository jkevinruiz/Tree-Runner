import pygame
from pygame import Vector2
from abc import ABC, abstractmethod


class Camera():
    def __init__(self, player):
        self.player = player
        self.offset = Vector2(0, 0)
        self.offset_float = Vector2(0, 0)
        self.scroll_speed = 0
        self.DISPLAY_W = 300
        self.DISPLAY_H = 200
        self.CONST = Vector2(-self.DISPLAY_W/2 +
                             player.rect.w / 2, -141 )

    def set_method(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()
    
    def reset(self):
        self.offset = Vector2(0, 0)
        self.offset_float = Vector2(0, 0)
        self.scroll_speed = 0

class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass


class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x -
                                       self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y -
                                       self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x = int(self.camera.offset_float.x)
        self.camera.offset.y = int(self.camera.offset_float.y)


class Auto(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        if self.camera.scroll_speed > 3:
            self.camera.scroll_speed = 3
        self.camera.offset.x += self.camera.scroll_speed
