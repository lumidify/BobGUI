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

from bisect import bisect_left

def get_closest(lst, num):
    #Taken from: http://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
    pos = bisect_left(lst, num)
    if pos == 0:
        return 0
    if pos == len(lst):
        return pos - 1
    if lst[pos] - num < num - lst[pos - 1]:
        return pos
    else:
        return pos - 1

def calc_size_list(lines, font):
    size_list = []
    for line_index, line in enumerate(lines):
        size_list.append([0])
        for letter_index, letter in enumerate(line):
            size_list[line_index].append(font.size(line[0:letter_index + 1])[0])
    return size_list
def get_index(mouse_pos, size_list, font_height):
    if len(size_list) == 1:
        return [0, 0]
    y = mouse_pos[1] // font_height
    if y >= len(size_list):
        y = len(size_list) - 1
    avg_x = round(size_list[y][-1] / len(size_list))
    if avg_x == 0:
        return [avg_x, y]
    est_index = round(mouse_pos[0] / avg_x)
    real_index = refine_index(est_index, mouse_pos[0], size_list[y])
    return [real_index, y]
def refine_index(est_index, pixel_pos, size_list):
    if est_index <= 0:
        est_index = 0
        direction = "right"
    elif est_index >= len(size_list) - 1:
        est_index = len(size_list) - 1
        direction = "left"
    elif size_list[est_index] == pixel_pos:
        return est_index
    else:
        if size_list[est_index] - pixel_pos < 0:
            direction = "right"
        else:
            direction = "left"
    if direction == "right":
        for x in range(est_index, len(size_list)):
            if x == len(size_list) - 1:
                return x
            elif abs(size_list[x] - pixel_pos) < abs(size_list[x + 1] - pixel_pos):
                return x
    else:
        for x in range(est_index, -1, -1):
            if abs(size_list[x] - pixel_pos) < abs(size_list[x - 1] - pixel_pos):
                return x
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
def textwrap(text, max_width, font, cursor_pos=[0, 0]):
    lines = []
    temp_list = []
    words = split(text)
    for word in words:
        if font.size(word)[0] > max_width:
            if temp_list != []:
                lines += list("".join(temp_list))
                lines.append("\\s")
                temp_list = []
            for index, char in enumerate(list(word)):
                if font.size("".join(temp_list + [char]))[0] > max_width:
                    lines += list("".join(temp_list))
                    lines.append("\\s")
                    if cursor_pos[0] >= len(temp_list) - 1:
                        cursor_pos[0] -= len(temp_list)
                        cursor_pos[1] += 1
                    temp_list = [char]
                else:
                    temp_list.append(char)
        elif font.size("".join(temp_list) + word)[0] > max_width:
            lines += list("".join(temp_list))
            lines.append("\\s")
            if cursor_pos[0] >= len("".join(temp_list)) - 1:
                cursor_pos[0] -= len("".join(temp_list))
                cursor_pos[1] += 1
            temp_list = [word]
        else:
            temp_list.append(word)
    if temp_list != []:
        lines += list("".join(temp_list))
    return lines, cursor_pos
