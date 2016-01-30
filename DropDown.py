import os
import pygame
from pygame.locals import *
class Dropdown():
    def __init__(self, screen, pos, choices, default):
        self.screen = screen
        self.pos = pos
        self.choices = choices
        self.default = default
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
    def draw(self):
        pass