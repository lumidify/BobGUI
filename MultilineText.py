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
from helper_functions import get_closest

def split(text, delimiter=" "):
    temp_list = []
    final_list = []
    for char in text:
        if char == delimiter:
            if "".join(temp_list) != "":
                final_list.append("".join(temp_list))
                temp_list = []
            final_list.append(delimiter)
        else:
            temp_list.append(char)
    if "".join(temp_list) != "":
        final_list.append("".join(temp_list))
    return final_list
#TODO: Only rerender from point of insertion
#TODO: Justify text
class Line():
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.font = self.parent.font
        self.text = kwargs.get("text", "")
        self.size_list = [0]
        self.text_splits = []
        self.offsets = []
        self.gen_surf()
        self.wrap_text()
        self.gen_offsets()
    def delete_slice(self, start, end):
        self.text = self.text[:start] + self.text[end:]
    def insert(self, index, text):
        self.text = self.text[:index] + text + self.text[index:]
    def delete(self, index):
        self.text = self.text[:index] + self.text[index + 1:]
    def regenerate(self):
        self.gen_surf()
        self.wrap_text()
        self.gen_offsets()
    def gen_offsets(self):
        self.offsets = []
        for split in self.text_splits:
            width = self.size_list[split[1]] - self.size_list[split[0]]
            extra = 0
            if self.parent.align == "center":
                extra = (self.parent.inner_width - width) // 2
            elif self.parent.align == "right":
                extra = self.parent.inner_rect.width - width
            self.offsets.append(extra)
    def get_nearest_index(self, pos, y=0):
        if y <= 0:
            y_index = 0
        else:
            y_index = y // self.parent.lineheight
            if y_index >= len(self.text_splits):
                y_index = len(self.text_splits) - 1
        if pos < self.offsets[y_index]:
            pos = self.offsets[y_index]
        line_width = self.size_list[self.text_splits[y_index][1]] - self.size_list[self.text_splits[y_index][0]]
        if pos > line_width + self.offsets[y_index]:
            pos = line_width + self.offsets[y_index]
        pos += self.size_list[self.text_splits[y_index][0]]
        pos -= self.offsets[y_index]
        return get_closest(self.size_list, pos)
    def get_index_pos(self, index):
        x = self.size_list[index]
        #FIXME: Kind of ugly here
        if self.parent.wrap:
            for split_index, split in enumerate(self.text_splits):
                if self.size_list[split[0]] <= x <= self.size_list[split[1]]:
                    y_index = split_index
                    break
            else:
                y_index = 0
            y = y_index * self.parent.lineheight
            x -= self.size_list[self.text_splits[y_index][0]]
        else:
            y = 0
            y_index = 0
        x += self.offsets[y_index]
        return (x, y)
    def resize(self):
        self.wrap_text()
        self.gen_offsets()
    def wrap_text(self):
        if not self.text:
            self.text_splits = [(0, 0)]
            return
        self.text_splits = []
        start = 0
        if self.parent.wrap:
            current_width = 0
            current_total_width = 0
            letter_index = 0
            for index, word in enumerate(split(self.text)):
                letter_index += len(word)
                width_change = self.size_list[letter_index] - current_total_width
                current_total_width += width_change
                if current_width + width_change > self.parent.inner_width:
                    current_width = 0
                    #Skip over the spaces which are used for wrapping
                    #Otherwise the spaces which span over two lines would still be visible,
                    #introducing pretty weird behavior
                    end = letter_index - len(word)
                    if self.text[start] == " ":
                        start += 1
                    if self.text[end - 1] == " ":
                        end -= 1
                    if end != start:
                        self.text_splits.append((start, end))
                    start = end
                current_width += width_change
        if self.text[start] == " ":
            start += 1
        self.text_splits.append((start, len(self.text)))
    def gen_surf(self, startindex=0):
        #TODO: Only rerender from startindex onwards
        #TODO: Maybe create separate functions for creating different effects
        #so that it is easy to add new effects.
        #FIXME: Underlines are currently broken when letter or word spacing is set.
        self.gen_size_list(startindex)
        startpos = self.size_list[startindex]
        self.textsurf = pygame.surface.Surface((self.size_list[-1], self.parent.lineheight)).convert_alpha()
        self.textsurf.fill((0, 0, 0, 0))
        if self.parent.shadow:
            self.shadowsurf = pygame.surface.Surface((self.size_list[-1], self.parent.lineheight)).convert_alpha()
            self.shadowsurf.fill((0, 0, 0, 0))
        if self.parent.letter_spacing:
            for index, letter in enumerate(self.text):
                if self.parent.shadow:
                    self.shadowsurf.blit(self.font.render(letter, self.parent.antialias, self.parent.shadow_color), (self.size_list[index], 0))
                self.textsurf.blit(self.font.render(letter, self.parent.antialias, self.parent.text_color), (self.size_list[index], 0))
        elif self.parent.word_spacing:
            index = 0
            for word in split(self.text):
                if self.parent.shadow:
                    self.shadowsurf.blit(self.font.render(word, self.parent.antialias, self.parent.shadow_color), (self.size_list[index], 0))
                self.textsurf.blit(self.font.render(word, self.parent.antialias, self.parent.text_color), (self.size_list[index], 0))
                index += len(word)
        else:
            if self.parent.shadow:
                self.shadowsurf.blit(self.font.render(self.text, self.parent.antialias, self.parent.shadow_color), (0, 0))
            self.textsurf.blit(self.font.render(self.text, self.parent.antialias, self.parent.text_color), (0, 0))
    def gen_size_list(self, startindex=0):
        extra = 0
        self.size_list = self.size_list[:startindex + 1]
        for index, letter in enumerate(self.text[startindex:]):
            #FIXME: Should letter_spacing affect spaces or not?
            if self.parent.letter_spacing:
                extra += self.parent.letter_spacing
            if self.parent.word_spacing and letter == " ":
                extra += self.parent.word_spacing
            self.size_list.append(self.font.size(self.text[:index + startindex + 1])[0] + extra)
    def get_full_height(self):
        return self.parent.lineheight * len(self.text_splits)
    def draw(self, screen, **kwargs):
        y = kwargs.get("y", 0)
        x = kwargs.get("x", 0)
        for index, split in enumerate(self.text_splits):
            #FIXME: A shadow with a large negative offset covers the text in the line above.
            width = self.size_list[split[1]] - self.size_list[split[0]]
            extra = self.offsets[index]
            if self.parent.shadow:
                screen.blit(self.shadowsurf, (x + extra + self.parent.shadow_offsetx, y + self.parent.shadow_offsety), (self.size_list[split[0]], 0, width, self.parent.lineheight))
            screen.blit(self.textsurf, (x + extra, y), (self.size_list[split[0]], 0, width, self.parent.lineheight))
            y += self.parent.lineheight

class MultilineText():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.wrap = kwargs.get("wrap", True)
        self.antialias = kwargs.get("antialias", True)
        self.italic = kwargs.get("italic", False)
        self.bold = kwargs.get("bold", False)
        self.underline = kwargs.get("underline", False)
        self.text_color = kwargs.get("color", (0, 0, 0))
        self.letter_spacing = kwargs.get("letter_spacing", None)
        self.word_spacing = kwargs.get("word_spacing", None)
        self.font = kwargs.get("font", None)
        self.fontsize = kwargs.get("fontsize", 20)
        self.load_font()
        self.textheight = self.font.get_linesize()
        self.lineheight = kwargs.get("lineheight", self.textheight)
        self.align = kwargs.get("align", "left")
        self.shadow = kwargs.get("shadow", False)
        self.shadow_color = kwargs.get("shadow_color", (150, 150, 150))
        self.shadow_offsetx = kwargs.get("shadow_offsetx", 2)
        self.shadow_offsety = kwargs.get("shadow_offsety", 2)
        self.text = kwargs.get("text", "")
        self.lines = self.text.splitlines()
        self.rect = Rect(0, 0, kwargs.get("width", 0), kwargs.get("height", 0))
        self.padding = kwargs.get("padding", [0, 0, 0, 0])
        self.calc_inner_size()
        self.create_surface()
        self.final_lines = []
        for line in self.lines:
            self.final_lines.append(Line(self, text=line))
        self.gen_height_size_list()
    def calc_inner_size(self):
        self.inner_width = self.rect.width - self.padding[0] - self.padding[2]
        self.inner_height = self.rect.height - self.padding[1] - self.padding[3]
        if self.inner_width < 0:
            self.inner_width = 0
        if self.inner_height < 0:
            self.inner_height = 0
    def create_surface(self):
        self.textsurface = pygame.surface.Surface((self.inner_width, self.inner_height)).convert_alpha()
        self.textsurface.fill((0, 0, 0, 0))
    def delete_slice(self, start, end):
        if start[1] == end[1]:
            self.final_lines[start[1]].delete_slice(start[0], end[0])
            self.final_lines[start[1]].regenerate()
        else:
            text = self.final_lines[start[1]].text[:start[0]] + self.final_lines[end[1]].text[end[0]:]
            self.final_lines[start[1]:end[1] + 1] = [Line(self, text=text)]
        self.gen_height_size_list()
    def split_line(self, pos):
        text1 = self.final_lines[pos[1]].text[:pos[0]]
        text2 = self.final_lines[pos[1]].text[pos[0]:]
        self.final_lines[pos[1]] = Line(self, text=text1)
        self.final_lines.insert(pos[1] + 1, Line(self, text=text2))
        self.gen_height_size_list()
    def join_lines(self, index1, index2):
        text = self.final_lines[index1].text + self.final_lines[index2].text
        self.final_lines[index1:index2 + 1] = [Line(self, text=text)]
        self.gen_height_size_list()
    def delete_line(self, index):
        self.final_lines.pop(index)
        self.gen_height_size_list()
    def add_line(self, index):
        self.final_lines.insert(index, Line(self, text=""))
        self.gen_height_size_list()
    def insert(self, pos, text):
        self.final_lines[pos[1]].insert(pos[0], text)
        self.final_lines[pos[1]].regenerate()
        self.gen_height_size_list()
    def delete(self, pos):
        self.final_lines[pos[1]].delete(pos[0])
        self.final_lines[pos[1]].regenerate()
        self.gen_height_size_list()
    def load_font(self):
        try:
            self.font = pygame.font.Font(self.font, self.fontsize)
        except:
            self.font = pygame.font.SysFont(self.font, self.fontsize)
        self.font.set_underline(self.underline)
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
    def gen_height_size_list(self):
        self.height_size_list = [0]
        for line in self.final_lines:
            self.height_size_list.append(self.height_size_list[-1] + line.get_full_height())
    def get_nearest_index(self, pos):
        if pos[1] < 0:
            return (0, 0)
        y = 0
        past_boundaries = False
        for index, height in enumerate(self.height_size_list):
            try:
                if height <= pos[1] < self.height_size_list[index + 1]:
                    y = index
                    break
            except:
                y = len(self.final_lines) - 1
                past_boundaries = True
        if not past_boundaries:
            x = self.final_lines[y].get_nearest_index(pos[0], y=pos[1] - self.height_size_list[y])
        else:
            x = len(self.final_lines[y].text)
        return (x, y)
    def get_index_pos(self, index_pos):
        pos = self.final_lines[index_pos[1]].get_index_pos(index_pos[0])
        pos = (pos[0], pos[1] + self.height_size_list[index_pos[1]])
        return pos
    def resize(self, size):
        self.rect.size = size
        self.calc_inner_size()
        self.create_surface()
        for line in self.final_lines:
            line.resize()
        self.gen_height_size_list()
    def draw(self):
        self.textsurface.fill((0, 0, 0, 0))
        for index, line in enumerate(self.final_lines):
            y = self.height_size_list[index]
            line.draw(self.textsurface, x=0, y=y)
        self.screen.blit(self.textsurface, (self.rect.x + self.padding[0], self.rect.y + self.padding[1]))
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), RESIZABLE)
    text = MultilineText(screen, text="Hello! This is an amazing demo.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", width=1000, height=700, wrap=True, font="liberationserif", align="center", shadow=True, fontsize=22, shadow_offsetx=2, shadow_offsety=2, padding=[10, 0, 20, 0])
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                text.resize(event.dict["size"])
        text.draw()
        pygame.display.update()
