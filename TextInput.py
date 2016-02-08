"""
This file is part of BobGUI
Copyright © 2016 Lumidify Productions

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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
                            self.delete_line(self.cursor.y_index)
                            self.cursor.y_index -= 1
                            self.cursor.x_index = len(self.final_lines[self.cursor.y_index].text)
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
