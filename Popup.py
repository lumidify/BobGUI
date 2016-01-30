import os
import sys
import pygame
from pygame.locals import *

class Popup():
    def __init__(self, screen, pos, size):
        self.screen = screen
        self.pos = pos
        self.size = size