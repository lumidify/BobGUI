import sys
import pygame
from pygame.locals import *

class Label():
    def __init__(self, screen, pos, text, font, color):
        self.screen = screen
        self.pos = pos
        self.text = text
        self.font = font
        self.color = color
    def draw(self):
        self.screen.blit(self.font.render(text, True, color), self.pos)