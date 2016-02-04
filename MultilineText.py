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

#TODO: Font manager

import os
import sys
import pygame
from pygame.locals import *
from BasicText import BasicText

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
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.wrap = kwargs.get("wrap", True)
        self.antialias = kwargs.get("antialias", True)
        self.italic = kwargs.get("italic", False)
        self.bold = kwargs.get("bold", False)
        self.underline = kwargs.get("underline", False)
        self.color = kwargs.get("color", (0, 0, 0))
        self.letter_spacing = kwargs.get("letter_spacing", None)
        self.word_spacing = kwargs.get("word_spacing", None)
        self.text = kwargs.get("text", "")
        self.font = kwargs.get("font", None)
        self.fontsize = kwargs.get("fontsize", 20)
        self.align = kwargs.get("align", "left")
        self.shadow = kwargs.get("shadow", False)
        self.shadow_color = kwargs.get("shadow_color", (150, 150, 150))
        self.shadow_offsetx = kwargs.get("shadow_offsetx", 2)
        self.shadow_offsety = kwargs.get("shadow_offsety", 2)
        self.size_list = [0]
        self.load_font()
        self.height = self.font.get_height()
        self.text_splits = []
        self.width = 0
        self.gen_surf()
    def resize(self, **kwargs):
        self.width = kwargs.get("width", self.width)
        if self.wrap:
            self.wrap_text()
    def wrap_text(self):
        self.text_splits = []
        current_width = 0
        current_total_width = 0
        letter_index = 0
        start = 0
        for index, word in enumerate(split(self.text)):
            letter_index += len(word)
            width_change = self.size_list[letter_index] - current_total_width
            current_total_width += width_change
            if current_width + width_change > self.width:
                current_width = 0
                #Skip over the spaces which are used for wrapping
                #Otherwise the spaces which span over two lines would still be visible,
                #introducing pretty weird behavior
                if self.text_splits and self.text[self.text_splits[-1][1]] == " ":
                    start = self.text_splits[-1][1] + 1
                end = letter_index - len(word)
                if end != start:
                    self.text_splits.append((start, end))
                start = end
            current_width += width_change
        self.text_splits.append((start, len(self.text)))
    def load_font(self):
        try:
            self.font = pygame.font.Font(self.font, self.fontsize)
        except:
            self.font = pygame.font.SysFont(self.font, self.fontsize)
        self.font.set_underline(self.underline)
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
    def gen_surf(self, startindex=0):
        #TODO: Maybe create separate functions for creating different effects
        #so that it is easy to add new effects.
        #FIXME: Underlines are currently broken when letter or word spacing is set.
        self.gen_size_list(startindex)
        startpos = self.size_list[startindex]
        self.textsurf = pygame.surface.Surface((self.size_list[-1], self.height)).convert_alpha()
        self.textsurf.fill((0, 0, 0, 0))
        if self.shadow:
            self.shadowsurf = pygame.surface.Surface((self.size_list[-1], self.height)).convert_alpha()
            self.shadowsurf.fill((0, 0, 0, 0))
        if self.letter_spacing:
            for index, letter in enumerate(self.text):
                if self.shadow:
                    self.shadowsurf.blit(self.font.render(letter, self.antialias, self.shadow_color), (self.size_list[index], 0))
                self.textsurf.blit(self.font.render(letter, self.antialias, self.color), (self.size_list[index], 0))
        elif self.word_spacing:
            index = 0
            for word in split(self.text):
                if self.shadow:
                    self.shadowsurf.blit(self.font.render(word, self.antialias, self.shadow_color), (self.size_list[index], 0))
                self.textsurf.blit(self.font.render(word, self.antialias, self.color), (self.size_list[index], 0))
                index += len(word)
        else:
            if self.shadow:
                self.shadowsurf.blit(self.font.render(self.text, self.antialias, self.shadow_color), (0, 0))
            self.textsurf.blit(self.font.render(self.text, self.antialias, self.color), (0, 0))
    def gen_size_list(self, startindex=0):
        extra = 0
        self.size_list = self.size_list[:startindex + 1]
        for index, letter in enumerate(self.text[startindex:]):
            #FIXME: Should letter_spacing affect spaces or not?
            if self.letter_spacing:
                extra += self.letter_spacing
            if self.word_spacing and letter == " ":
                extra += self.word_spacing
            self.size_list.append(self.font.size(self.text[:index + startindex + 1])[0] + extra)
    def draw(self, **kwargs):
        y = kwargs.get("y", 0)
        x = kwargs.get("x", 0)
        if self.wrap:
            for split in self.text_splits:
                width = self.size_list[split[1]] - self.size_list[split[0]]
                extra = 0
                if self.align == "center":
                    extra = (self.width - width) // 2
                elif self.align == "right":
                    extra = self.width - width
                if self.shadow:
                    self.screen.blit(self.shadowsurf, (x + extra + self.shadow_offsetx, y + self.shadow_offsety), (self.size_list[split[0]], 0, width, self.height))
                self.screen.blit(self.textsurf, (x + extra, y), (self.size_list[split[0]], 0, width, self.height))
                y += self.height
        else:
            extra = 0
            if self.align == "center":
                extra = (self.width - self.size_list[-1]) // 2
            elif self.align == "right":
                extra = self.width - self.size_list[-1]
            if self.shadow:
                self.screen.blit(self.shadowsurf, (x + extra + self.shadow_offsetx, y + shadow_offsety))
            self.screen.blit(self.textsurf, (x + extra, y))

class MultilineText():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.text = kwargs.get("text", "")
        self.wrap = kwargs.get("wrap", False)
        self.lines = self.text.splitlines()
        self.rect = Rect(0, 0, kwargs.get("width", 0), kwargs.get("height", 0))
        self.textsurface = pygame.surface.Surface(self.rect.size).convert_alpha()
        self.textsurface.fill((0, 0, 0, 0))
        self.offsetx = 0
        self.final_lines = []
        #TODO: Add special handler for empty lines so no extra processing power is used
        #creating empty Line objects.
        for line in self.lines:
            kwargs.update({"text": line})
            self.final_lines.append(Line(self.textsurface, **kwargs))
    def resize(self, size):
        self.rect.size = size
        self.textsurface = pygame.surface.Surface(size).convert_alpha()
        self.textsurface.fill((0, 0, 0, 0))
        for line in self.final_lines:
            line.screen = self.textsurface
            line.resize(width=self.rect.width)
    def draw(self):
        self.textsurface.fill((0, 0, 0, 0))
        y = 0
        for index, line in enumerate(self.final_lines):
            line.draw(x=self.rect.x, y=y)
            y += len(line.text_splits) * line.height
        self.screen.blit(self.textsurface, self.rect)
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), RESIZABLE)
    text = MultilineText(screen, text="Hello! This is an amazing demo.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", width=1000, height=700, wrap=True, font="liberationserif", align="center", shadow=True, fontsize=22)
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
