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
