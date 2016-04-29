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
from Grid import Grid
from Widget import Widget
from pygame.locals import *

class GridFrame(Widget, Grid):
    def __init__(self, parent, **kwargs):
        Widget.__init__(self, parent)
        Grid.__init__(self)
        self.rect = Rect(0, 0, kwargs.get("width", 0), kwargs.get("height", 0))
    def update_screen(self, screen):
        Grid.update_screen(self, screen)
    def resize(self, **kwargs):
        Grid.resize_widgets(self, **kwargs)

