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
from pygame.locals import *
from MultilineText import MultilineText
from helper_functions import get_closest

#FIXME: Selection currently lags considerably, presumably because the index-getting methods of the underlying text classes are quite slow.

class SelectableText(MultilineText):
    def __init__(self, screen, **kwargs):
        super().__init__(screen, **kwargs)
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.pressed = False
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        collide_mouse = self.rect.collidepoint(mouse_pos)
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and collide_mouse:
            self.x1, self.y1 = self.x2, self.y2 = self.get_nearest_index(mouse_pos)
            self.pressed = True
        elif event.type == MOUSEMOTION and self.pressed and collide_mouse:
            self.x2, self.y2 = self.get_nearest_index(mouse_pos)
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            if not self.pressed and not collide_mouse:
                self.select_none()
            if self.x1 == self.x2 and self.y1 == self.y2:
                self.select_none()
            self.pressed = False
    def get_ordered_indeces(self):
        if self.y1 == self.y2:
            temp_x1, temp_x2 = sorted([self.x1, self.x2])
            return (temp_x1, self.y1), (temp_x2, self.y2)
        else:
            temp_y1, temp_y2 = [self.y1, self.y2]
            temp_x1, temp_x2 = [self.x1, self.x2]
            if temp_y1 > temp_y2:
                temp_y1, temp_y2 = reversed([self.y1, self.y2])
                temp_x1, temp_x2 = reversed([self.x1, self.x2])
            return (temp_x1, temp_y1), (temp_x2, temp_y2)
    def delete_selection(self):
        if not None in [self.x1, self.y1, self.x2, self.y2]:
            indeces = self.get_ordered_indeces()
            self.delete_slice(*indeces)
            self.select_none()
            return indeces[0]
        else:
            return False
    def select_none(self):
        self.x1 = self.y1 = self.x2 = self.y2 = None
    def draw(self):
        if not None in (self.x1, self.y1, self.x2, self.y2):
            real_x1, real_y1 = self.get_index_pos((self.x1, self.y1))
            real_x2, real_y2 = self.get_index_pos((self.x2, self.y2))
            if real_y1 == real_y2:
                if real_x1 != real_x2:
                    real_x1, real_x2 = sorted((real_x1, real_x2))
                    pygame.draw.rect(self.screen, (100, 200, 100), ((real_x1, real_y1), (real_x2 - real_x1, self.textheight)))
            else:
                if real_y1 > real_y2:
                    real_y1, real_y2 = reversed([real_y1, real_y2])
                    real_x1, real_x2 = reversed([real_x1, real_x2])
                if self.rect.width - real_x1 > 0:
                    pygame.draw.rect(self.screen, (100, 200, 100), (real_x1, real_y1, self.rect.width - real_x1, self.textheight))
                if self.textheight != self.lineheight:
                    pygame.draw.rect(self.screen, (100, 200, 100), (0, real_y1 + self.textheight, self.rect.width, self.lineheight - self.textheight))
                if real_y2 - real_y1 > self.lineheight:
                    pygame.draw.rect(self.screen, (100, 200, 100), (0, real_y1 + self.lineheight, self.rect.width, real_y2 - real_y1 - self.lineheight))
                if real_x2 > 0:
                    pygame.draw.rect(self.screen, (100, 200, 100), (0, real_y2, real_x2, self.textheight))
        super().draw()
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), RESIZABLE)
    text = SelectableText(screen, text="Hello! This is an amazing demo.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", width=1000, height=700, wrap=True, font="liberationserif", align="center", shadow=True, fontsize=22, shadow_offsetx=2, shadow_offsety=2, lineheight=50)
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                text.resize(event.dict["size"])
            else:
                text.update(event)
        text.draw()
        pygame.display.update()
