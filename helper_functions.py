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

from bisect import bisect_left

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

