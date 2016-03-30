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
# class
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pygame
from pygame.locals import *

class FontManager():
    def __init__(self):
        #Family, size, bold, italic, underline
        #TODO: Implement underline in actual text class so that
        #it doesn't break when setting word or letter spacing.
        self.fonts = {}
    def get_font(self, style={}):
        if style in self.fonts:
            return self.fonts[style]
        else:
            font_name = style.get("font", None)
            try:
                font = pygame.font.Font(font_name, self.fontsize)
            except:
                font = pygame.font.SysFont(font_name, self.fontsize)
            font.set_underline(self.underline)
            font.set_bold(self.bold)
            font.set_italic(self.italic)
        self.fonts[style] = font
        return font

class Font():
    def __init__(self, **kwargs):
        self.italic = kwargs.get("italic", False)
        self.bold = kwargs.get("bold", False)
        self.underline = kwargs.get("underline", False)
        self.family = kwargs.get("family", None)
        self.size = kwargs.get("size", 20)

    def load_font(self):
        try:
            self.font = pygame.font.Font(self.family, self.size)
        except:
            self.font = pygame.font.SysFont(self.family, self.size)
        self.font.set_underline(self.underline)
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)

    def get_size_list(self, **kwargs):
        text = kwargs.get("text", "")
        letter_spacing = kwargs.get("letter_spacing", 0)
        word_spacing = kwargs.get("word_spacing", 0)
        extra = 0
        size_list = [0]
        for index, letter in enumerate(self.text[startindex:]):
            if letter_spacing:
                extra += letter_spacing
            if word_spacing and letter == " ":
                extra += word_spacing
            size_list.append(self.font.size(self.text[:index + startindex + 1])[0] + extra)

    def render(self, **kwargs):
        #TODO: Render underline manually so as not to break it when word or letter spacing is set.
        pass
