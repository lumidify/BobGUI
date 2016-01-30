import os
import sys
import pygame
from Grid import Grid
from Widget import Widget
from pygame.locals import *

class GridFrame(Widget, Grid):
    def __init__(self, parent, **kwargs):
        Widget.__init__(self, parent)
        Grid.__init__(self)
        self.rect = Rect(0, 0, kwargs.get("width", 0), kwargs.get("height", 0))
    def update_screen(self, screen):
        Grid.update_screen(self, screen)
    def resize(self, **kwargs):
        Grid.resize_widgets(self, **kwargs)

