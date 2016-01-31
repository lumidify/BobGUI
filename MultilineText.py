"""
BobGUI 1.0
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
from BasicText import BasicText

class MultilineText():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.text = kwargs.get("text", "")
        self.lines = self.text.splitlines()
        self.final_lines = []
        for line in self.lines:
            kwargs.update({"text": line})
            self.final_lines.append(BasicText(self.screen, **kwargs))
    def draw(self):
        y = 0
        for line in self.final_lines:
            line.draw((0, y))
            y += line.height

pygame.init()
screen = pygame.display.set_mode((0, 0))
text = MultilineText(screen, text="Hk:js;ldkfj;sdlkj;lkjjjsdfklaioaioweruiawopsdmnmm,xcvm,.xnvxcnm,vnxm,nm,nm,.sdm,fsdjf\nssdfsdfsdadf\\nsfsdasffsssdfssdddfsdfsdfsdfsdfsdffffffffffffffffff\nsssssssssssssssssssssssssssssssdfdjklkjla;kjsd;lfjklsdjfklsdjlfjklsal;sdlfkj", fontsize=50, color=(255, 10, 100))
while True:
    screen.fill((255, 255, 255))
    text.draw()
    pygame.display.update()
