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
from Widget import Widget
from pygame.locals import *
from BasicText import BasicText

class Label(Widget):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.rendered_text = BasicText(self.screen, **kwargs)
        self.padding = kwargs.get("padding", [0, 0, 0, 0])
        self.text_width, self.text_height = self.rendered_text.size_list[-1], self.rendered_text.height
        self.rect = Rect(0, 0, kwargs.get("width", self.text_width + self.padding[0] + self.padding[2]), kwargs.get("height", self.text_height + self.padding[1] + self.padding[3]))
    def update_screen(self, screen):
        self.screen = screen
        self.rendered_text.screen = screen
    def draw(self):
        self.rendered_text.draw((self.rect.x + (self.rect.width - self.text_width - self.padding[0] - self.padding[2]) // 2 + self.padding[0], self.rect.y + (self.rect.height - self.text_height - self.padding[1] - self.padding[3]) // 2 + self.padding[1]))
