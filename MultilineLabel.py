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
