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

