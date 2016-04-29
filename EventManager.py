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

class EventManager():
    def __init__(self, root):
        self.root = root
        self.mouse_buttons_pressed = []
        self.keys_pressed = []
        self.time_passed
        self.repeating = False
        self.delay = 0
        self.interval = 0
        self.repeat = False
        #TODO: Joystick Support
    def set_repeat(self, repeat=True, delay=0, interval=0):
        self.repeat = repeat
        if repeat:
            self.delay = delay
            self.interval = interval
    def update(self, time):
        if self.repeat:
            if not self.repeating:
                if self.time_passed >= self.delay:
                    self.repeating = True
                    self.time_passed -= self.delay
                    for key in self.keys_pressed:
                        # Send to widgets
                        pass
            else:
                if self.time_passed >= self.interval:
                    self.time_passed -= self.interval
                    # Send to widgets
    def event(self, event):
        if event.type == QUIT:
            pass

        if event.type == MOUSEBUTTONDOWN:
            self.mouse_buttons_pressed.append(event.button)

        elif event.type == MOUSEBUTTONUP:
            self.mouse_buttons_pressed.remove(event.button)

        elif event.type == MOUSEMOTION:
            pass

        if event.type == KEYDOWN:
            # event.unicode works for many keys. When it gives an empty string (for special keys),
            # we just get the name with pygame.key.name(event)
            key = event.unicode
            if not key:
                key = pygame.key.name(event.key)
            self.keys_pressed.append(key)
        elif event.type == KEYUP:
            key = event.unicode
            if not key:
                key = pygame.key.name(event)
            try:
                self.keys_pressed.remove(key)
            except ValueError:
                # Maybe key was pressed when program started, so it never was added to self.keys_pressed,
                # so we just let it go...
                pass

