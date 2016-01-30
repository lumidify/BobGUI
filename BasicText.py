import os
import sys
import pygame
from pygame.locals import *

class BasicText():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.italic = kwargs.get("italic", False)
        self.bold = kwargs.get("bold", False)
        self.underline = kwargs.get("underline": False)
        self.color = kwargs.get("color": (0, 0, 0))
        self.padding = kwargs.get("padding", [0, 0, 0, 0])
        self.margin = kwargs.get("margin", [0, 0, 0, 0])
        self.letter_spacing = kwargs.get("letter-spacing": None)
        self.word_spacing = kwargs.get("word-spacing": None)
        self.rect = Rect(0, 0, 0, 0)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                text.update(event)
        text.draw()
        pygame.display.update()