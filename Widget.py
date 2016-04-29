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

class Widget():
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.screen = self.parent.screen
    def update_screen(self, screen):
        self.screen = screen
    def update(self, **kwargs):
        pass
    def resize(self):
        pass
    def calculate_pos(self):
        pass
    def grid(self, **kwargs):
        self.row = kwargs.get("row", 0)
        self.column = kwargs.get("column", 0)
        self.rowspan = kwargs.get("rowspan", 1)
        self.columnspan = kwargs.get("columnspan", 1)
        self.sticky = kwargs.get("sticky", "").lower()
        self.parent.add_widget(self, row=self.row, column=self.column, rowspan=self.rowspan, columnspan=self.columnspan)
    def flow(self, **kwargs):
        self.parent.add_widget(self, **kwargs)
    def place(self, **kwargs):
        self.parent.add_widget(self, **kwargs)

