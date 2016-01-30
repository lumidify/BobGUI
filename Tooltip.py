import os
import sys
import pygame
from pygame.locals import *

class Tooltip():
    def __init__(self, pos, text, delay=500, on_time=5000):
        self.pos = pos
        self.text = text
        self.delay = delay
        self.on_time = on_time
    def update(self, collide):
        pass
    def draw(self):
        pass