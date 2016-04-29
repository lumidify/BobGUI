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
