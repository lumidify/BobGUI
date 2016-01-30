import os
import sys
import pygame
from Grid import Grid
from Flow import Flow
from Place import Place
from Widget import Widget
from pygame.locals import *

class Frame(Widget, Grid, Flow, Place):
    def __init__(self, parent, **kwargs):
        Widget.__init__(self, parent, **kwargs)
        self.rect = Rect(self.boundx, self.boundy, self.boundwidth, self.boundheight)
        self.layout = kwargs.get("layout", None)
        if self.layout == "grid":
            self.layout = Grid
        elif self.layout == "flow":
            self.layout = Flow
        elif self.layout == "place" or self.layout is None:
            self.layout = Place
        self.layout.__init__(self)
    def resize(self, **kwargs):
        self.layout.resize_widgets(self, **kwargs)
    def update_screen(self, screen):
        self.screen = screen
        self.layout.update_screen(self, screen)
