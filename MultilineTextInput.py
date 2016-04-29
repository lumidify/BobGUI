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
from SelectableText import SelectableText
from helper_functions import calc_size_list, get_index, refine_index, textwrap
from pygame.locals import *

SHIFT = 1
CTRL = 64
ALT = 256

class TextInput():
    def __init__(self, screen, pos, size, font, **kwargs):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.rect = Rect(self.pos, self.size)
        self.font = font
        self.font_height = self.font.get_height()
        self.command = kwargs.get("command", None)
        self.maxlines = kwargs.get("maxlines", -1)
        self.maxlinelength = kwargs.get("maxlinelength", -1)
        self.focused = False
        self.highlighted = False
        self.cursor = Cursor("|", 700, 500, self.pos)
        self.text = SelectableText(self.screen, "", self.font, self.pos, textwrap=kwargs.get("textwrap", False), maxlinelength=kwargs.get("maxlinelength", -1))
        self.update_text("")
        pygame.key.set_repeat(500, 20)
    def update_text(self, text):
        self.text.change_text(text)
    def get_text(self):
        return self.text.text.get_text()
    def update(self, event):
        significant_event = False
        mouse_pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(mouse_pos):
            self.focused = True
            self.cursor.start()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1 and not self.rect.collidepoint(mouse_pos):
            self.focused = False
            self.cursor.stop()
        elif event.type == MOUSEMOTION:
            if self.rect.collidepoint(mouse_pos):
                self.highlighted = True
            else:
                self.highlighted = False
        elif event.type == KEYDOWN and self.focused:
            mod = event.mod
            mods = pygame.key.get_mods()
            significant_event = True
            if event.key == K_BACKSPACE:
                if self.text.get_selected_text() != None:
                    points = self.text.get_ordered_points()
                    self.cursor.x, self.cursor.y = points[0]
                    self.text.removeslice(points)
                else:
                    if self.cursor.x > 0:
                        self.text.remove([self.cursor.x - 1, self.cursor.y])
                        self.cursor.x -= 1
                    else:
                        if self.cursor.y > 0:
                            self.cursor.x = len(self.text.lines[self.cursor.y - 1])
                            self.text.remove([-1, self.cursor.y])
                            self.cursor.y -= 1
            elif event.key == K_DELETE:
                if self.text.get_selected_text() != None:
                    points = self.text.get_ordered_points()
                    self.cursor.x, self.cursor.y = points[0]
                    self.text.removeslice(points)
                else:
                    self.text.remove((self.cursor.x, self.cursor.y))
            elif event.key == K_RETURN:
                self.text.insertline((self.cursor.x, self.cursor.y))
                self.cursor.y += 1
                self.cursor.x = 0
                #if self.command != None:
                #    self.command()
            elif event.key == K_LEFT:
                if self.cursor.x > 0:
                    self.cursor.x -= 1
                else:
                    if self.cursor.y > 0:
                        self.cursor.y -= 1
                        self.cursor.x = len(self.text.lines[self.cursor.y])
            elif event.key == K_RIGHT:
                if self.cursor.x < len(self.text.lines[self.cursor.y]):
                    self.cursor.x += 1
                else:
                    if self.cursor.y < len(self.text.lines) - 1:
                        self.cursor.y += 1
                        self.cursor.x = 0
            elif event.key == K_UP:
                self.cursor.move_up(self.text.size_list)
                if self.cursor.x > len(self.text.lines[self.cursor.y]):
                    self.cursor.x = len(self.text.lines[self.cursor.y]) - 1
            elif event.key == K_DOWN:
                self.cursor.move_down(self.text.size_list)
                if self.cursor.x > len(self.text.lines[self.cursor.y]):
                    self.cursor.x = len(self.text.lines[self.cursor.y]) -1
            else:
                if event.unicode != "" and mods in [0, 1, 2, 4096, 8192, 4097, 4098, 8193, 8194]:
                    if self.text.get_selected_text() != None:
                        self.text.replaceslice(self.text.get_ordered_points(), event.unicode)
                        self.cursor.x = self.text.get_ordered_points()[0][0] + 1
                        self.cursor.y = self.text.get_ordered_points()[0][1]
                    else:
                        self.text.insert((self.cursor.x, self.cursor.y), event.unicode)
                        self.cursor.x += 1
            if mods == 0:
                self.text.selectnone()
        if significant_event:
            self.cursor.event()
        self.change_color()
        self.text.update(event)
    def change_color(self):
        if self.highlighted:
            self.color = (0, 0, 200)
        elif self.focused:
            self.color = (0, 0, 150)
        else:
            self.color = (0, 0, 100)
    def draw(self):
        self.cursor.x, self.cursor.y = self.text.wrap([self.cursor.x, self.cursor.y])
        self.cursor.update()
        if self.cursor.visible:
            if self.text.get_selected_text() != None:
                self.cursor.x = self.text.x2
                self.cursor.y = self.text.y2
            self.cursor.calc_pixel_pos(self.text.size_list, self.font.get_height())
            self.screen.blit(self.font.render(self.cursor.string, 1, (255, 255, 255)), (self.cursor.pixelx, self.cursor.pixely))

        pygame.draw.rect(self.screen, self.color, self.rect, 2)
        self.text.draw()

if __name__ == "__main__":
    pygame.init()
    font = pygame.font.Font(os.path.join("Lumidify_Casual.ttf"), 25)
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    gui = [TextInput(screen, [0, 0], [400, 200], font, textwrap=True, maxlinelength=400)]
    while True:
        clock.tick(30)
        screen.fill((0, 0, 0))
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
