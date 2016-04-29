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
import pygame
from Widget import Widget
from pygame.locals import *
from Image import ScaledImage
from BasicText import BasicText

class Button(Widget):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.text = kwargs.get("text", "")
        self.command = kwargs.get("command", None)
        self.pressed = False
        self.highlighted = False

        self.padding = kwargs.get("padding", [0, 0, 0, 0])
        keep_aspect_ratio = kwargs.get("keep_aspect_ratio", False)
        self.normal_image = ScaledImage(self.screen, os.path.join("images", "button.png"), keep_aspect_ratio=keep_aspect_ratio)
        self.highlighted_image = ScaledImage(self.screen, os.path.join("images", "button_highlighted.png"), keep_aspect_ratio=keep_aspect_ratio)
        self.pressed_image = ScaledImage(self.screen, os.path.join("images", "button_pressed.png"), keep_aspect_ratio=keep_aspect_ratio)

        self.rendered_text = BasicText(self.screen, **kwargs)
        self.text_width, self.text_height = self.rendered_text.size_list[-1], self.rendered_text.height
        self.rect = Rect(0, 0, kwargs.get("width", self.text_width + self.padding[0] + self.padding[2]), kwargs.get("height", self.text_height + self.padding[1] + self.padding[3]))
        self.change_image()
        self.resize_images()
    def resize(self):
        self.resize_images()
    def resize_images(self):
        for image in [self.normal_image, self.highlighted_image, self.pressed_image]:
            image.resize(width=self.rect.width, height=self.rect.height)
    def calculate_pos(self):
        for image in [self.normal_image, self.highlighted_image, self.pressed_image]:
            image.x = self.rect.x
            image.y = self.rect.y
            image.x += (self.rect.width - image.width) // 2
            image.y += (self.rect.height - image.height) // 2
    def update_screen(self, screen):
        self.screen = screen
        self.rendered_text.screen = self.screen
        for image in [self.normal_image, self.highlighted_image, self.pressed_image]:
            image.update_screen(screen)
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        button_collide = self.rect.collidepoint(mouse_pos)
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and button_collide:
            self.pressed = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            if button_collide and self.pressed and self.command != None:
                self.command()
            self.pressed = False
        elif event.type == MOUSEMOTION:
            if not self.pressed and button_collide:
                self.highlighted = True
            else:
                self.highlighted = False
        self.change_image()
    def change_image(self):
        if self.pressed:
            self.image = self.pressed_image
        elif self.highlighted:
            self.image = self.highlighted_image
        else:
            self.image = self.normal_image
    def draw(self):
        self.image.draw()
        self.rendered_text.draw((self.rect.x + (self.rect.width - self.text_width - self.padding[0] - self.padding[2]) // 2 + self.padding[0], self.rect.y + (self.rect.height - self.text_height - self.padding[1] - self.padding[3]) // 2 + self.padding[1]))
