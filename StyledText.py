import os
import sys
import pygame
from pygame.locals import *
from helper_functions import calc_size_list, textwrap

TAB = "\t"
TABWIDTH = 4
NEWLINE = "\n"
SOFTNEWLINE = "\s"

class BasicText():
    def __init__(self, screen, style):
        self.style = style

class Text():
    def __init__(self, screen, text, rect, **kwargs):
        self.screen = screen
        self.text = text
        self.final_text = []
        self.lines = []
        self.lines_split = []
        self.size_list = []
        self.rect = rect
        self.horiz_align = kwargs.get("horiz_align", "left")
        self.vert_align = kwargs.get("vert_align", "top")
        self.leading = kwargs.get("leading", 0)
        self.selectable = kwargs.get("selectable", True)
        self.generate()
    
    def calculate(self):
        for text in self.final_text:
            text["text"] = text["text"].split("\n")
    def generate(self):
        self.extract_styles(self.text)
        for text_index, text in enumerate(self.final_text):
            text[1] = self.mergedicts(text[1])
            text[1]["text"] = text[0]
            self.final_text[text_index] = text[1]
        for x in self.final_text:
            x["font_object"] = self.generate_font(x)
        self.calculate()
        self.calc_size_list()
            
    def generate_font(self, style):
        font = pygame.font.Font(style.get("font", None), style.get("size", 20))
        font.set_italic(style.get("italic", False))
        font.set_bold(style.get("bold", False))
        font.set_underline(style.get("underline", False))
        return font

    def extract_styles(self, text, style=[]):
        style = style
        for index, x in enumerate(text):
            if type(x) == dict:
                style.append(x)
            elif type(x) == str:
                self.final_text.append([x, list(style)])
            elif type(x) == list:
                self.extract_styles(x, style)
        try:
            style.pop()
        except:
            pass
    
    def mergedicts(self, dictlist):
        temp = {}
        for x in dictlist:
            temp.update(x)
        return temp
    
    def update(self, event):
        pass
    def calc_size_list(self):
        last_width = self.rect.x
        last_height = self.rect.y
        self.line_heights = [0]
        self.line_widths = [0]
        line_index_cumulative = 0
        
        #Generate the total height and width of each line
        for text in self.final_text:
            for line_index, line in enumerate(text["text"]):
                if line_index != 0:
                    self.line_heights.append(0)
                    self.line_widths.append(0)
                    line_index_cumulative += 1
                height = text["font_object"].get_height()
                if height > self.line_heights[line_index_cumulative]:
                    self.line_heights[line_index_cumulative] = height
                self.line_widths[line_index_cumulative] += text["font_object"].size(line)[0]
                
        #Generate the exact position of each character
        line_index_cumulative = 0
        for text in self.final_text:
            text["size_list_x"] = [[last_width]]
            final_height = self.line_heights[line_index_cumulative] - text["font_object"].get_height()
            if text.get("super", False):
                final_height = text.get("super_offset", -2)
            elif text.get("sub", False):
                final_height += text.get("sub_offset", 2)
            text["size_list_y"] = [last_height + final_height]
            for line_index, line in enumerate(text["text"]):
                if line_index != 0:
                    last_width = self.rect.x
                    last_height += text.get("leading", self.line_heights[line_index_cumulative])
                    line_index_cumulative += 1
                    text["size_list_x"].append([last_width])
                    final_height = self.line_heights[line_index_cumulative] - text["font_object"].get_height()
                    if text.get("super", False):
                        final_height = text.get("super_offset", -2)
                    elif text.get("sub", False):
                        final_height += text.get("sub_offset", 2)
                    text["size_list_y"].append(last_height + final_height)
                for char_index, char in enumerate(line):
                    width = text["font_object"].size(line[:char_index + 1])[0]
                    
                    if char == " ":
                        #TODO: Proper word spacing
                        last_width += text.get("word_spacing", 0)
                    else:
                        last_width +=  text.get("letter_spacing", 0)
                    text["size_list_x"][line_index].append(last_width + width)
            last_width += width
            
    def wrap(self):
        pass
    def get_index(self):
        pass
    def refine_index(self):
        pass
    def split(self, delimeter=" "):
        pass
    def draw(self):
        line_index_cumulative = 0
        for text_index, text in enumerate(self.final_text):
            for line_index, line in enumerate(text["text"]):
                if line != "":
                    if line_index != 0:
                        line_index_cumulative += 1
                    if text.get("background", None) != None:
                        pygame.draw.rect(self.screen, text["background"], (text["size_list_x"][line_index][0], sum(self.line_heights[:line_index_cumulative]), text["size_list_x"][line_index][-1] - text["size_list_x"][line_index][0], self.line_heights[line_index_cumulative]))
                        
                    if text.get("letter_spacing", 0) != 0:
                        for char_index, char in enumerate(line):
                            if text.get("shadow", False):
                                shadow_offset = text.get("shadow_offset", (2, 2))
                                self.screen.blit(text["font_object"].render(char, True, text.get("shadow_color", (200, 200, 200))), (text["size_list_x"][line_index][char_index] + shadow_offset[0], text["size_list_y"][line_index] + shadow_offset[1]))
                            self.screen.blit(text["font_object"].render(char, True, text.get("color", (0, 0, 0))), (text["size_list_x"][line_index][char_index], text["size_list_y"][line_index]))
                    elif text.get("word_spacing", 0) != 0:
                        word_index = 0
                        for word in line:
                            if text.get("shadow", False):
                                shadow_offset = text.get("shadow_offset", (2, 2))
                                self.screen.blit(text["font_object"].render(word, True, text.get("shadow_color", (200, 200, 200))), (text["size_list_x"][line_index][word_index] + shadow_offset[0], text["size_list_y"][line_index] + shadow_offset[1]))
                            
                            self.screen.blit(text["font_object"].render(word, True, text.get("color", (0, 0, 0))), (text["size_list_x"][line_index][word_index], text["size_list_y"][line_index]))
                            word_index += len(word)
                    else:
                        if text.get("shadow", False):
                            shadow_offset = text.get("shadow_offset", (2, 2))
                            self.screen.blit(text["font_object"].render(line, True, text.get("shadow_color", (200, 200, 200))), (text["size_list_x"][line_index][0] + shadow_offset[0], text["size_list_y"][line_index] + shadow_offset[1]))
                        self.screen.blit(text["font_object"].render(line, True, text.get("color", (0, 0, 0))), (text["size_list_x"][line_index][0], text["size_list_y"][line_index]))
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    text = Text(screen, [{"font": None, "size": 40}, "This is normal text!", [{"italic": True, "size": 30, "color": (100, 255, 255)}, " This is italic text!", [{"bold": True, "color": (0, 255, 0), "size": 50}, " This is bold italic text!"], "\n This is some more italic text!", [{"underline": True, "size": 15, "color": (255, 0, 0)}, " This is italic underlined text!"]], " This is normal text again!", [{"size": 20, "font": "Lumidify_Casual.ttf"}, [{"word_spacing": 50, "size": 30, "background": (100, 255, 100)}, "\nThis is text in ", [{"letter_spacing": 15, "bold": True, "size": 40}, "Lum", [{"shadow": True, "shadow_color": (200, 255, 200), "shadow_offset": (3, 3)}, "idify"]], [{"shadow": True}, "Casual!"], [{"super": True, "size": 20, "super_offset": 0}, "\nth"], "fdffsd"], [{"shadow": True, "size": 50, "shadow_offset": (3, 3)}, " dfsdfsdfd"]]], Rect(0, 0, 1366, 768))
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                text.update(event)
        text.draw()
        pygame.display.update()
