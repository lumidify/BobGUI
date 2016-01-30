import pygame
from pygame.locals import *

class Tab():
    def __init__(self, screen, rect, tabs, style={}, selected=0):
        self.screen = screen
        self.tabs = tabs
        self.selected = selected
    def calculate(self):
        for tab in self.tabs:
            tab[0] = Text()
    def update(self, event):
        if event.type == MOUSEBUTTONDOWN:
            for tab_rect in self.tab_rects