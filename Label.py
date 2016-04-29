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
from Widget import Widget
from pygame.locals import *
from helper_functions import split


class Label(Widget):
    def __init__(self, parent, **kwargs):
        super().__init__(Label)
        self.italic = kwargs.get("italic", False)
        self.bold = kwargs.get("bold", False)
        self.underline = kwargs.get("underline", False)
        self.color = kwargs.get("color", (0, 0, 0))
        self.letter_spacing = kwargs.get("letter_spacing", None)
        self.word_spacing = kwargs.get("word_spacing", None)
        self.text = kwargs.get("text", "")
        self.font = kwargs.get("font", None)
        self.fontsize = kwargs.get("fontsize", 20)
        self.shadow = kwargs.get("shadow", False)
        self.shadow_offsetx = kwargs.get("shadow_offsetx", 2)
        self.shadow_offsety = kwargs.get("shadow_offsety", 2)
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
        self.split_surfaces = [self.textsurf]
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
    def split(self, indeces):
        self.split_surfaces = []
        for index_index, index in enumerate(indeces):
            if index_index == 0:
                temp_surf = pygame.surface.Surface((self.size_list[index], self.height)).convert_alpha()
                temp_surf.fill((0, 0, 0, 0))
                temp_surf.blit(self.textsurf, (0, 0), (0, 0, self.size_list[index], self.height))
            else:
                temp_surf = pygame.surface.Surface((self.size_list[index] - self.size_list[indeces[index_index - 1]], self.height)).convert_alpha()
                temp_surf.fill((0, 0, 0, 0))
                temp_surf.blit(self.textsurf, (0, 0), (self.size_list[indeces[index_index - 1]], 0, self.size_list[index] - self.size_list[indeces[index_index - 1]], self.height))
            self.split_surfaces.append(temp_surf)
    def draw(self, **kwargs):
        y = kwargs.get("y", 0)
        x = kwargs.get("x", 0)
        splits = kwargs.get("indeces", [])
        current_pos = 0
        for split in splits:
            self.screen.blit(self.textsurf, (x, y), (current_pos, 0, self.size_list[split] - current_pos, self.height))
            current_pos += self.size_list[split] - current_pos
            y += self.height

