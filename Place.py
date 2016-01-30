import os
import sys
import pygame
from pygame.locals import *

class Place():
    def __init__(self):
        self.widgets = set()
    def place(self, widget, **kwargs):
        self.widgets.add(widget)
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        widget.rect.x = x
        widget.rect.y = y
    def update(self, **kwargs):
        event = kwargs.get("event", None)
        for widget in self.widgets:
            widget.update(event=event)
    def draw(self):
        for widget in self.widgets:
            widget.draw()
