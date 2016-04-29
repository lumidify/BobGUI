# This file is part of BobGUI, a free GUI library for Pygame.
# Copyright (C) 2016  Lumidify Productions <lumidify@openmailbox.org>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import GridFrame
import pygame
from Label import Label
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
b = Label(a, text="Hi! This is a label!", padding=[10, 10, 10, 10], fontsize=50, color=(150, 150, 0))
b.grid(row=0, column=0)
a.config_column(0, weight=1)
a.config_row(0, weight=1)
while True:
    for event in pygame.event.get():
        root.update(event=event)
    root.update()
    root.draw()
    pygame.display.update()
