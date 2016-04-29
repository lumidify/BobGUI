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
from Cursor import Cursor
from pygame.locals import *
from SelectableText import SelectableText

class TextInput(SelectableText):
    def __init__(self, screen, **kwargs):
        super().__init__(screen, **kwargs)
        self.rect = Rect(0, 0, kwargs.get("height", 0), kwargs.get("width", 0))
        self.multiline = kwargs.get("multiline", True)
        self.cursor = Cursor(height=self.textheight)
        self.focused = False
        self.highlighted = False
    def update(self, event=None):
        super().update(event)
        if not None in [self.x2, self.y2]:
            self.cursor.x_index = self.x2
            self.cursor.y_index = self.y2
        significant_event = False
        mouse_pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(mouse_pos):
            self.focused = True
            self.cursor.start()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1 and not self.rect.collidepoint(mouse_pos):
            self.focused = False
            self.cursor.stop()
        elif event.type == MOUSEMOTION:
            if self.pressed:
                significant_event = True
            if self.rect.collidepoint(mouse_pos):
                self.highlighted = True
            else:
                self.highlighted = False
        elif event.type == KEYDOWN and self.focused:
            significant_event = True
            if event.key == K_BACKSPACE:
                new_indeces = self.delete_selection()
                if not new_indeces:
                    self.cursor.x_index -= 1
                    if self.cursor.x_index < 0:
                        if self.cursor.y_index > 0:
                            self.cursor.y_index -= 1
                            self.cursor.x_index = len(self.final_lines[self.cursor.y_index].text)
                            self.join_lines(self.cursor.y_index, self.cursor.y_index + 1)
                        else:
                            self.cursor.x_index = 0
                    else:
                        self.delete((self.cursor.x_index, self.cursor.y_index))
                else:
                    self.cursor.x_index, self.cursor.y_index = new_indeces
            elif event.key == K_DELETE:
                new_indeces = self.delete_selection()
                if not new_indeces:
                    if self.cursor.x_index < len(self.final_lines[self.cursor.y_index].text):
                        self.delete((self.cursor.x_index, self.cursor.y_index))
                    else:
                        if self.cursor.y_index < len(self.final_lines) - 1:
                            self.join_lines(self.cursor.x_index, self.cursor.y_index + 1)
                else:
                    self.cursor.x_index, self.cursor.y_index = new_indeces
            elif event.key == K_RETURN:
                if self.multiline:
                    new_indeces = self.delete_selection()
                    if new_indeces:
                        self.cursor.x_index, self.cursor.y_index = new_indeces
                    self.split_line((self.cursor.x_index, self.cursor.y_index))
                    self.cursor.x_index = 0
                    self.cursor.y_index += 1
            elif event.key == K_UP:
                pos = self.get_index_pos((self.cursor.x_index, self.cursor.y_index))
                self.cursor.x_index, self.cursor.y_index = self.get_nearest_index((pos[0], pos[1] - self.textheight))
            elif event.key == K_DOWN:
                pos = self.get_index_pos((self.cursor.x_index, self.cursor.y_index))
                self.cursor.x_index, self.cursor.y_index = self.get_nearest_index((pos[0], pos[1] + self.lineheight))
            elif event.key == K_LEFT:
                if self.cursor.x_index > 0:
                    self.cursor.x_index -= 1
                elif self.cursor.y_index > 0:
                    self.cursor.y_index -= 1
                    self.cursor.x_index = len(self.final_lines[self.cursor.y_index].text)
            elif event.key == K_RIGHT:
                if self.cursor.x_index < len(self.final_lines[self.cursor.y_index].text):
                    self.cursor.x_index += 1
                elif self.cursor.y_index < len(self.final_lines) - 1:
                    self.cursor.y_index += 1
                    self.cursor.x_index = 0
            else:
                new_indeces = self.delete_selection()
                if new_indeces:
                    self.cursor.x_index, self.cursor.y_index = new_indeces
                character = event.unicode
                if len(character) > 0:
                    self.select_none()
                    self.insert((self.cursor.x_index, self.cursor.y_index), character)
                    self.cursor.x_index += 1
        if significant_event:
            self.cursor.event()
        self.change_color()
    def change_color(self):
        if self.highlighted:
            self.color = (0, 0, 200)
        elif self.focused:
            self.color = (0, 0, 150)
        else:
            self.color = (0, 0, 100)
    def draw(self):
        self.cursor.update()
        pygame.draw.rect(self.screen, self.color, self.rect, 2)
        super().draw()
        self.cursor.draw(self.screen, self.get_index_pos((self.cursor.x_index, self.cursor.y_index)))
if __name__ == "__main__":
    pygame.init()
    pygame.key.set_repeat(500, 20)
    screen = pygame.display.set_mode((500, 500))
    gui = [TextInput(screen, width=500, height=500, text="Hello, how are you?dsfjsdafsdkl;fjsdlafjkasd;lfjs;lfj; sdfjksdl;jf dfsdfj safljsdfj sdfkjsdl sdjfsdklfjas jfj klajsdfklja lfdj sdfa kjdlsf\nsfsdfkshdfjklshka fhsdk dfj asdfhklh kfhasdfkj", align="center")]
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                for widget in gui:
                    widget.update(event)
        for widget in gui:
            widget.draw()
        pygame.display.update()
