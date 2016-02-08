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
from MultilineText import MultilineText

class Label(Widget):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.rendered_text = MultilineText(self.screen, **kwargs)
        self.padding = kwargs.get("padding", [0, 0, 0, 0])
        self.text_width, self.text_height = max(line.size_list[-1] for line in self.rendered_text.final_lines), self.rendered_text.height_size_list[-1]
        self.rect = Rect(0, 0, kwargs.get("width", self.text_width + self.padding[0] + self.padding[2]), kwargs.get("height", self.text_height + self.padding[1] + self.padding[3]))
    def resize(self, **kwargs):
        super().resize(**kwargs)
        self.rendered_text.resize(self.rect.size)
    def calculate_pos(self):
        self.rendered_text.rect.topleft = self.rect.topleft
    def update_screen(self, screen):
        self.screen = screen
        self.rendered_text.screen = screen
    def draw(self):
        self.rendered_text.draw()
