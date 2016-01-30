import os
import sys
import Place.Place
import Widget.Widget
import pygame
from pygame.locals import *

class PlaceFrame(Widget, Place):
    def __init__(self, parent, **kwargs):
        Widget.__init__(parent)
        Place.__init__()
