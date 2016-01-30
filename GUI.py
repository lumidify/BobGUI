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
import GridFrame
import Button
import pygame
from Grid import Grid
from Flow import Flow
from Place import Place
from pygame.locals import *

class GUI(Grid, Flow, Place):
    def __init__(self, **kwargs):
        pygame.init()
        self.screen_info = pygame.display.Info()
        self.screen_size = kwargs.get("screen_size", (0, 0))
        self.resizable = kwargs.get("resizable", True)
        if self.resizable:
            self.screen = pygame.display.set_mode(self.screen_size, RESIZABLE)
        else:
            self.screen = pygame.display.set_mode(self.screen_size)
        self.rect = Rect((0, 0), self.screen.get_size())
        self.layout = kwargs.get("layout", None)
        if self.layout == "grid":
            Grid.__init__(self)
            self.layout = Grid
        elif self.layout == "flow":
            Flow.__init__(self)
            self.layout = Flow
        elif self.layout == "place" or self.layout is None:
            Place.__init__(self)
            self.layout = Place
        self.fullscreen = kwargs.get("fullscreen", False)
        self.last_screen_size = self.rect.size
    def toggle_fullscreen(self):
        pygame.display.quit()
        pygame.display.init()
        if self.fullscreen:
            self.rect.size = self.last_screen_size
            self.screen = pygame.display.set_mode(self.rect.size, RESIZABLE)
        else:
            self.last_screen_size = self.rect.size
            self.rect.size = (self.screen_info.current_w, self.screen_info.current_h)
            self.screen = pygame.display.set_mode(self.rect.size, FULLSCREEN)
        self.fullscreen = not self.fullscreen
        self.resize()
        self.layout.update_screen(self, self.screen)
    def resize(self, **kwargs):
        width = kwargs.get("width", self.rect.width)
        height = kwargs.get("height", self.rect.height)
        kwargs.setdefault("width", width)
        kwargs.setdefault("height", height)
        self.layout.resize_widgets(self, **kwargs)
    def update(self, **kwargs):
        event = kwargs.get("event", None)
        if event:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                self.rect.size = event.dict["size"]
                self.screen = pygame.display.set_mode(self.screen_size, RESIZABLE)
                self.resize()
            else:
                self.layout.update(self, event=event)
    def draw(self):
        self.layout.draw(self)
"""
parent.grid(widget, ...) or widget.grid(...)?
"""
root = GUI(layout="grid")
a = GridFrame.GridFrame(root)
a.grid(row=0, column=0, sticky="nswe")
root.config_column(0, weight=1)
root.config_row(0, weight=1)
b = Button.Button(a, text="Hi! This is a button!", command=sys.exit, padding=[10, 10, 10, 10])
b.grid(row=0, column=0)
a.config_column(0, weight=1)
a.config_row(0, weight=1)
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_F11:
                root.toggle_fullscreen()
        root.update(event=event)
    root.update()
    root.draw()
    pygame.display.update()
