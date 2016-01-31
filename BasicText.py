"""
BobGUI 1.0
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
from pygame.locals import *

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

class BasicText():
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.italic = kwargs.get("italic", False)
        self.bold = kwargs.get("bold", False)
        self.underline = kwargs.get("underline", False)
        self.color = kwargs.get("color", (0, 0, 0))
        self.letter_spacing = kwargs.get("letter_spacing", None)
        self.word_spacing = kwargs.get("word_spacing", None)
        self.text = kwargs.get("text", "")
        self.font = kwargs.get("font", None)
        self.fontsize = kwargs.get("fontsize", 20)
        self.size_list = []
        self.height = 0
        self.load_font()
        self.gen_surf()
    def load_font(self):
        try:
            self.font = pygame.font.Font(self.font, self.fontsize)
        except:
            self.font = pygame.font.SysFont(self.font, self.fontsize)
        self.font.set_underline(self.underline)
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
    def gen_surf(self):
        self.gen_size_list()
        if self.letter_spacing:
            self.textsurf = pygame.surface.Surface((self.size_list[-1], self.height)).convert_alpha()
            self.textsurf.fill((0, 0, 0, 0))
            for index, letter in enumerate(self.text):
                self.textsurf.blit(self.font.render(letter, True, self.color), (self.size_list[index], 0))
        elif self.word_spacing:
            self.textsurf = pygame.surface.Surface((self.size_list[-1], self.height)).convert_alpha()
            self.textsurf.fill((0, 0, 0, 0))
            index = 0
            for word in split(self.text):
                self.textsurf.blit(self.font.render(word, True, self.color), (self.size_list[index], 0))
                index += len(word)
        else:
            self.textsurf = self.font.render(self.text, True, self.color)
    def gen_size_list(self):
        extra = 0
        self.size_list = [0]
        self.height = self.font.size(self.text)[1]
        for index, letter in enumerate(self.text):
            if self.letter_spacing:
                extra += self.letter_spacing
            if self.word_spacing and letter == " ":
                extra += self.word_spacing
            self.size_list.append(self.font.size(self.text[:index + 1])[0] + extra)
    def draw(self, pos):
        self.screen.blit(self.textsurf, pos)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    text = BasicText(screen, text="Hello, World!", color=(255, 0, 100), fontsize=50, letter_spacing=50, underline=True)
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        text.draw()
        pygame.display.update()