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

import pygame
from pygame.locals import *

class Cursor():
    """
    height: height of the text for drawing the cursor
    width: width of cursor
    visible_time: the amount of time in milliseconds the cursor should be visible in each blink
    hidden_time: the amount of time in milliseconds the cursor should be hidden in each blink
    """
    def __init__(self, **kwargs):
        self.x_index = 0
        self.y_index = 0
        self.visible_time = kwargs.get("visible_time", 700)
        self.hidden_time = kwargs.get("hidden_time", 500)
        self.time_passed = self.visible_time
        self.blink_counter = 0
        self.change_in_time = 0
        self.visible = False
        self.blinking = False
        self.current_time = pygame.time.get_ticks()
        self.width = kwargs.get("width", 2)
        self.height = kwargs.get("height", 20)
    def update(self):
        if self.blinking:
            self.change_in_time = pygame.time.get_ticks() - self.current_time
            self.current_time += self.change_in_time
            self.time_passed += self.change_in_time
            self.blink()
    def event(self):
        if self.blinking:
            self.time_passed = 0
            self.visible = True
    def blink(self):
        if self.time_passed >= self.visible_time:
            self.blink_counter += self.change_in_time
            if self.visible:
                if self.blink_counter >= self.visible_time:
                    self.visible = False
                    self.blink_counter = 0
            else:
                if self.blink_counter >= self.hidden_time:
                    self.visible = True
                    self.blink_counter = 0
    def start(self):
        self.blinking = True
        self.visible = True
        self.blink_counter = 0
        self.time_passed = self.visible_time
        self.current_time = pygame.time.get_ticks()
    def stop(self):
        self.blinking = False
        self.visible = False
    def draw(self, screen, pos):
        if self.visible:
            pygame.draw.rect(screen, (0, 0, 0), (pos, (self.width, self.height)))
