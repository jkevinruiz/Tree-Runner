import pygame
from pygame import Vector2
from abc import ABC, abstractmethod


class Camera():
    def __init__(self, player):
        self.player = player
        self.scroll_speed = 0
        self.offset = Vector2(0, 0)
        self.offset_float = Vector2(0, 0)

    def set_method(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()
    
    def reset(self):
        self.scroll_speed = 0
        self.offset = Vector2(0, 0)
        self.offset_float = Vector2(0, 0)

class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass

class Auto(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        if self.camera.scroll_speed > 3:
            self.camera.scroll_speed = 3

        self.camera.offset.x += self.camera.scroll_speed
