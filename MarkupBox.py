import pygame
from pygame.locals import *

class MarkupBox():
    def __init__(self, screen, rect, xml):
        self.screen = screen
        self.rect = rect
        self.xml = xml