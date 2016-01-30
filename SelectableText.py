import os
import sys
import pygame
from pygame.locals import *
from Text import Text
from helper_functions import calc_size_list, get_index, refine_index, textwrap

SHIFT = 0b1
RSHIFT = 0b10
CTRL = 0b1000000
RCTRL = 0b10000000
ALT = 0b100000000
NUMLOCK = 0b1000000000000
CAPSLOCK = 0b10000000000000

class SelectableText():
    def __init__(self, screen, text, font, pos, **kwargs):
        self.screen = screen
        self.text = text
        self.font = font
        self.pos = pos
        self.cursor_image = pygame.image.load(os.path.join("..", "..", "images", "text_cursor.png")).convert_alpha()
        self.cursor_image = pygame.transform.smoothscale(self.cursor_image, (24, 24))
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.pressed = False
        self.lines = []
        self.lines_wrapped = []
        self.lines_split = []
        self.lines_split_wrapped = []
        self.size_list = [[0]]
        self.size_list = [[0]]
        self.textwrap = kwargs.get("textwrap", False)
        self.maxlinelength = kwargs.get("maxlinelength", -1)
        self.leading = kwargs.get("leading", 0)
        self.font_height = self.font.get_height()
        self.calculate()
    def calculate(self):
        try:
            self.lines = self.text.split("\n")
        except:
            self.lines = [self.text]
        self.lines_split = [list(line) for line in self.lines]
        self.text = "\n".join(["".join(line) for line in self.lines_split])
        self.size_list = calc_size_list(self.lines, self.font)
        try:
            self.rect = Rect((0, 0), (max(x[-1] for x in self.size_list), self.font.size(self.lines[0])[1] * len(self.lines)))
        except:
            self.rect = Rect((0, 0), (0, 0))
    def gen_text(self):
        self.text = "\n".join(["".join(line) for line in self.lines_split])
        self.calculate()
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        mods_bin = format(pygame.key.get_mods(), '014b')
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
                self.pressed = True
                self.x1, self.y1 = get_index(mouse_pos, self.size_list, self.font.get_height())
                self.x2 = self.x1
                self.y2 = self.y1
        elif event.type == MOUSEMOTION and self.pressed and self.rect.collidepoint(mouse_pos):
            self.x2, self.y2 = get_index(mouse_pos, self.size_list, self.font.get_height())
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            if self.pressed == False and not self.rect.collidepoint(mouse_pos):
                self.selectnone()
            self.pressed = False
        elif event.type == KEYDOWN:
            if mods_bin[7] == '1' and event.key == K_a:
                self.selectall()
        test = pygame.key.get_pressed()
        if test[99] and test[306]:
            print(self.get_selected_text())
    def selectall(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = len(self.lines[-1])
        self.y2 = len(self.lines) - 1
    def selectnone(self):
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
    def get_selected_text(self):
        if not None in [self.x1, self.x2, self.y1, self.y2] and [self.x1, self.y1] != [self.x2, self.y2]:
            return self.getslice(self.get_ordered_points())
        else:
            return None
    def get_ordered_points(self):
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
    def change_text(self, text):
        self.text = text
        self.calculate()
    def get_text(self):
        return self.text
    def insert(self, pos, string):
        self.lines_split[pos[1]].insert(pos[0], string)
        self.gen_text()
    def remove(self, pos):
        if pos[0] >= len(self.lines_split[pos[1]]):
            if pos[1] + 1 < len(self.lines_split):
                self.lines_split[pos[1]:pos[1] + 2] = [self.lines_split[pos[1]] + self.lines_split[pos[1] + 1]]
        elif pos[0] < 0:
            self.lines_split[pos[1] - 1:pos[1] + 1] = [self.lines_split[pos[1] - 1] + self.lines_split[pos[1]]]
        else:
            if self.lines_split[pos[1]] == []:
                del self.lines_split[pos[1]]
            else:
                del self.lines_split[pos[1]][pos[0]]
        self.gen_text()
    def insertline(self, pos):
        self.lines_split[pos[1]].insert(pos[0], "\n")
        self.gen_text()
    def removeline(self, pos):
        del self.lines_split[pos]
        self.gen_text()
    def removeslice(self, pos):
        pos1, pos2 = pos
        if pos1[1] == pos2[1]:
            del self.lines_split[pos1[1]][pos1[0]:pos2[0]]
        else:
            del self.lines_split[pos1[1]][pos1[0]:]
            del self.lines_split[pos2[1]][0:pos2[0]]
            self.lines_split[pos1[1]:pos2[1] + 1] = [self.lines_split[pos1[1]] + self.lines_split[pos2[1]]]
        self.gen_text()
    def replaceslice(self, pos, string):
        self.removeslice(pos)
        self.insert(pos[0], string)
    def getslice(self, pos):
        pos1, pos2 = pos
        if pos1[1] == pos2[1]:
            sortedx = sorted([pos1[0], pos2[0]])
            return self.lines[pos1[1]][sortedx[0]:sortedx[1]]
        else:
            temp_text = [self.lines[pos1[1]][pos1[0]:]]
            for x in range(pos1[1] + 1, pos2[1]):
                temp_text.append(self.lines[x])
            temp_text.append(self.lines[pos2[1]][:pos2[0]])
            return "\n".join(temp_text)
    def wrap(self, cursor_pos):
        self.lines_wrapped = self.lines
        if self.textwrap:
            for index, size_list in enumerate(self.size_list):
                if size_list[-1] > self.maxlinelength and self.maxlinelength != -1:
                    self.lines_wrapped[index:index + 1], cursor_pos = textwrap(self.lines[index], self.maxlinelength, self.font, cursor_pos)
        self.size_list = calc_size_list(self.lines_wrapped, self.font)
        return cursor_pos
    def draw(self):
        selected_text = self.get_selected_text()
        if selected_text != None:
            font_height = self.font.size("a")[1]
            if self.y1 == self.y2:
                temp_x1, temp_x2 = sorted([self.x1, self.x2])
                before_width = self.font.size(self.lines[self.y1][0:temp_x1])[0]
                width = self.font.size(self.lines[self.y1][temp_x1:temp_x2])[0]
                pygame.draw.rect(self.screen, (100, 200, 100), ((before_width, font_height * self.y1), (width, font_height)))
            else:
                temp_y1, temp_y2 = [self.y1, self.y2]
                temp_x1, temp_x2 = [self.x1, self.x2]
                if temp_y1 > temp_y2:
                    temp_y1, temp_y2 = reversed([self.y1, self.y2])
                    temp_x1, temp_x2 = reversed([self.x1, self.x2])
                selected_size_x1 = self.font.size(self.lines[temp_y1][0:temp_x1])[0]
                selected_size_x2 = self.font.size(self.lines[temp_y2][0:temp_x2])[0]
                pygame.draw.rect(self.screen, (100, 200, 100), ((selected_size_x1, font_height * temp_y1), (self.rect.width - selected_size_x1, font_height)))
                if temp_y2 != temp_y1 + 1:
                    pygame.draw.rect(self.screen, (100, 200, 100), ((0, font_height * (temp_y1 + 1)), (self.rect.width, font_height * (temp_y2 - temp_y1 - 1))))
                pygame.draw.rect(self.screen, (100, 200, 100), ((0, font_height * temp_y2), (selected_size_x2, font_height)))
        for index, line in enumerate(self.lines):
            self.screen.blit(self.font.render(line, True, (255, 255, 255)), (self.pos[0], self.pos[1] + index * (self.font_height + self.leading)))
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.mouse.set_visible(False)
            self.screen.blit(self.cursor_image, (mouse_pos[0] - 8, mouse_pos[1] - 8))
        else:
            pygame.mouse.set_visible(True)
if __name__ == "__main__":
    pygame.init()
    font = pygame.font.Font(os.path.join("..", "..", "font", "Lumidify_Casual.ttf"), 40)
    screen = pygame.display.set_mode((500, 500))
    test = SelectableText(screen, "Hello, how are you? I'm fine!\nI hope you are fine too!\nI don't know what else to say.\nThis is another line!\nWow, this is amazing, isn't it?\nI love writing random stuff!", font, [0, 0])
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            test.update(event)
        test.draw()
        pygame.display.update()
