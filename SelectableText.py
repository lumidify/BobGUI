"""
This file is part of BobGUI
Copyright © 2016 Lumidify Productions

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import sys
import pygame
from pygame.locals import *
from MultilineText import MultilineText
from helper_functions import get_closest

#FIXME: Selection currently lags considerably, presumably because the index-getting methods of the underlying text classes are quite slow.

class SelectableText():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.text = MultilineText(screen, **kwargs)
        self.rect = Rect(0, 0, kwargs.get("width", 0), kwargs.get("height", 0))
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.pressed = False
    def resize(self, size):
        self.rect.size = size
        self.text.resize(size)
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        collide_mouse = self.rect.collidepoint(mouse_pos)
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and collide_mouse:
            self.x1, self.y1 = self.x2, self.y2 = self.text.get_nearest_index(mouse_pos)
            self.pressed = True
        elif event.type == MOUSEMOTION and self.pressed and collide_mouse:
            self.x2, self.y2 = self.text.get_nearest_index(mouse_pos)
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            if not self.pressed and not collide_mouse:
                self.select_none()
            self.pressed = False
    def get_ordered_indeces(self):
        if self.y1 == self.y2:
            temp_x1, temp_x2 = sorted([self.x1, self.x2])
            return (temp_x1, self.y1), (temp_x2, self.y2)
        else:
            temp_y1, temp_y2 = [self.y1, self.y2]
            temp_x1, temp_x2 = [self.x1, self.x2]
            if temp_y1 > temp_y2:
                temp_y1, temp_y2 = reversed([self.y1, self.y2])
                temp_x1, temp_x2 = reversed([self.x1, self.x2])
            return (temp_x1, temp_y1), (temp_x2, temp_y2)
    def select_none(self):
        self.x1 = self.y1 = self.x2 = self.y2 = None
    def draw(self):
        if not None in (self.x1, self.y1, self.x2, self.y2):
            real_x1, real_y1 = self.text.get_index_pos((self.x1, self.y1))
            real_x2, real_y2 = self.text.get_index_pos((self.x2, self.y2))
            if real_y1 == real_y2:
                if real_x1 != real_x2:
                    real_x1, real_x2 = sorted((real_x1, real_x2))
                    pygame.draw.rect(self.screen, (100, 200, 100), ((real_x1, real_y1), (real_x2 - real_x1, self.text.textheight)))
            else:
                if real_y1 > real_y2:
                    real_y1, real_y2 = reversed([real_y1, real_y2])
                    real_x1, real_x2 = reversed([real_x1, real_x2])
                if self.rect.width - real_x1 > 0:
                    pygame.draw.rect(self.screen, (100, 200, 100), (real_x1, real_y1, self.rect.width - real_x1, self.text.textheight))
                if self.text.textheight != self.text.lineheight:
                    pygame.draw.rect(self.screen, (100, 200, 100), (0, real_y1 + self.text.textheight, self.rect.width, self.text.lineheight - self.text.textheight))
                if real_y2 - real_y1 > self.text.lineheight:
                    pygame.draw.rect(self.screen, (100, 200, 100), (0, real_y1 + self.text.lineheight, self.rect.width, real_y2 - real_y1 - self.text.lineheight))
                if real_x2 > 0:
                    pygame.draw.rect(self.screen, (100, 200, 100), (0, real_y2, real_x2, self.text.textheight))
        self.text.draw()
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), RESIZABLE)
    text = SelectableText(screen, text="Hello! This is an amazing demo.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", width=1000, height=700, wrap=True, font="liberationserif", align="center", shadow=True, fontsize=22, shadow_offsetx=2, shadow_offsety=2, lineheight=50)
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                text.resize(event.dict["size"])
            else:
                text.update(event)
        text.draw()
        pygame.display.update()
