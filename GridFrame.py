# This file is part of BobGUI
# Copyright © 2016 Lumidify Productions <lumidify@openmailbox.org> <lumidify@protonmail.ch>
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

