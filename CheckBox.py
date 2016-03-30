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
import Widget
import pygame
from pygame.locals import *
from Image import ScaledImage
class CheckBox(Widget.Widget):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.screen = self.parent.screen
        self.normal_image = ScaledImage(self.screen, os.path.join("..", "..", "images", "checkbox_normal.png"))
        self.checked_image = ScaledImage(self.screen, os.path.join("..", "..", "images", "checkbox_checked.png"))

        self.boundwidth = kwargs.get("width", self.normal_image.width)
        self.boundheight = kwargs.get("height", self.normal_image.height)
        self.rect = Rect(0, 0, self.boundwidth, self.boundheight)
        self.bounding_rect = Rect(0, 0, self.boundwidth, self.boundheight)
        self.checked = kwargs.get("checked", False)
        self.pressed = False
    def update_screen(self, screen):
        self.screen = screen
        for image in [self.normal_image, self.checked_image]:
            image.screen = screen
    def resize_images(self):
        for image in [self.normal_image, self.checked_image]:
            image.resize(width=self.rect.width, height=self.rect.height)
    def resize(self, **kwargs):
        temp_width, temp_height = self.rect.width, self.rect.height
        super().resize(**kwargs)
        if temp_width != self.rect.width or temp_height != self.rect.height:
            self.resize_images()
    def calculate_pos(self):
        super().calculate_pos()
        for image in [self.normal_image, self.checked_image]:
            image.x = self.rect.x
            image.y = self.rect.y
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        collide_button = self.rect.collidepoint(mouse_pos)
        if event.type == MOUSEBUTTONDOWN:
            if collide_button:
                self.pressed = True
        elif event.type == MOUSEBUTTONUP:
            if collide_button:
                if self.pressed:
                    if self.checked:
                        self.checked = False
                    else:
                        self.checked = True
                    self.pressed = False
    def draw(self):
        if self.checked:
            image = self.checked_image
        else:
            image = self.normal_image
        image.draw()

