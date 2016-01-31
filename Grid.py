import os
import sys
import pygame
from pygame.locals import *

def autofill_list(lst, index, placeholder):
    if len(lst) <= index:
        for x in range(index - len(lst)):
            if type(placeholder) in [list, dict]:
                placeholder = placeholder.copy()
            lst.append(placeholder)
    return lst
class Grid():
    def __init__(self):
        self.widget_grid = []
        self.column_widths = []
        self.row_heights = []
        self.column_weights = {}
        self.row_weights = {}
        self.column_weights_inverse = {}
        self.row_weights_inverse = {}
    def config_column(self, column, **kwargs):
        weight = kwargs.get("weight", 0)
        self.column_weights.setdefault(weight, set())
        try:
            self.column_weights[self.column_weights_inverse[column]].remove(column)
        except:
            pass
        self.column_weights[weight].add(column)
        self.column_weights_inverse[column] = weight
        self.resize_widgets()
    def config_row(self, row, **kwargs):
        weight = kwargs.get("weight", 0)
        self.row_weights.setdefault(weight, set())
        try:
            self.row_weights[self.row_weights_inverse[row]].remove(row)
        except:
            pass
        self.row_weights[weight].add(row)
        self.row_weights_inverse[row] = weight
        self.resize_widgets()
    def resize_widgets(self, **kwargs):
        totalx = sum(self.column_weights.keys())
        totaly = sum(self.row_weights.keys())
        row_change = kwargs.get("row_change", 0)
        column_change = kwargs.get("column_change", 0)
        abs_x = kwargs.get("width", None)
        abs_y = kwargs.get("height", None)
        if abs_x is not None:
            self.rect.width = abs_x
        if abs_y is not None:
            self.rect.height = abs_y
        self.rect.width += column_change
        self.rect.height += row_change
        try:
            static_columns_width = sum([self.column_widths[index] for index, weight in enumerate(self.column_weights.get(0, set()))])
            column_change_unit = (self.rect.width - static_columns_width) / totalx
        except:
            column_change_unit = 0
        try:
            static_rows_heights = sum([self.row_heights[index] for index, weight in enumerate(self.row_weights.get(0, set()))])
            row_change_unit = (self.rect.height - static_rows_heights) / totaly
        except:
            row_change_unit = 0
        for row_index, row_height in enumerate(self.row_heights):
            row_weight = self.row_weights_inverse.get(row_index, 0)
            try:
                if row_weight != 0:
                    row_height = row_change_unit * row_weight / len(self.row_weights.get(row_weight, ()))
                    if row_height < 0:
                        row_height = 0
                    self.row_heights[row_index] = row_height
            except:
                pass
        for column_index, column_width in enumerate(self.column_widths):
            column_weight = self.column_weights_inverse.get(column_index, 0)
            try:
                if column_weight != 0:
                    column_width = column_change_unit * column_weight  / len(self.column_weights.get(column_weight, ()))
                    if column_width < 0:
                        column_width = 0
                    self.column_widths[column_index] = column_width
            except:
                pass
        self.update_widgets()
    def update_widgets(self):
        for row_index, row in enumerate(self.widget_grid):
            for column_index, column in enumerate(row):
                new_y = sum(self.row_heights[:row_index]) + self.rect.y
                new_x = sum(self.column_widths[:column_index]) + self.rect.x
                for widget in column:
                    new_width = sum(self.column_widths[column_index:column_index + widget.columnspan])
                    new_height = sum(self.row_heights[row_index:row_index + widget.rowspan])
                    if new_width != widget.bounding_rect.width or new_height != widget.bounding_rect.height:
                        self.resize_widget(widget, width=new_width, height=new_height)
                    if new_x != widget.bounding_rect.x or new_y != widget.bounding_rect.y:
                        self.move_widget_bounds(widget, x=new_x, y=new_y)
    def add_widget(self, widget, **kwargs):
        row = kwargs.get("row", 0)
        column = kwargs.get("column", 0)
        rowspan = kwargs.get("rowspan", 1)
        columnspan = kwargs.get("columnspan", 1)
        widget.boundx = 0
        widget.boundy = 0
        widget.boundwidth = 0
        widget.boundheight = 0
        widget.bounding_rect = Rect(0, 0, 0, 0)
        autofill_list(self.widget_grid, row + rowspan, [])
        for temp_row in self.widget_grid:
            autofill_list(temp_row, column + columnspan, [])
        autofill_list(self.column_widths, column + columnspan, 0)
        autofill_list(self.row_heights, row + rowspan, 0)
        current_width = sum(self.column_widths[column:column + columnspan])
        current_height = sum(self.row_heights[row:row + rowspan])
        if widget.rect.width > current_width:
            width_increment = (widget.rect.width - current_width) / columnspan
            current_width = widget.rect.width
            for index, column_width in enumerate(self.column_widths[column:column + columnspan]):
                self.column_widths[column + index] += width_increment
        if widget.rect.height > current_height:
            height_increment = (widget.rect.height - current_height) / rowspan
            current_height = widget.rect.height
            for index, row_width in enumerate(self.row_heights[row:row + rowspan]):
                self.row_heights[row + index] += height_increment
        self.resize_widget(widget, width=current_width, height=current_height)
        x = sum(self.column_widths[:column])
        y = sum(self.row_heights[:row])
        self.move_widget_bounds(widget, x=x, y=y)
        self.calculate_widget_pos(widget)
        self.widget_grid[row][column].append(widget)
        if self.row_weights_inverse.get(row, None) is None:
            self.config_row(row)
        if self.column_weights_inverse.get(column, None) is None:
            self.config_column(column)
    def update_screen(self, screen):
        for row in self.widget_grid:
            for column in row:
                for widget in column:
                    widget.update_screen(screen)
    def resize_widget(self, widget, **kwargs):
        row_change = kwargs.get("row_change", 0)
        column_change = kwargs.get("column_change", 0)
        abs_width = kwargs.get("width", None)
        abs_height = kwargs.get("height", None)
        if abs_width is not None:
            widget.boundwidth = abs_width
        if abs_height is not None:
            widget.boundheight = abs_height
        widget.boundwidth += column_change
        widget.boundheight += row_change
        widget.bounding_rect.width = widget.boundwidth
        widget.bounding_rect.height = widget.boundheight
        self.calculate_widget_pos(widget)
    def move_widget_bounds(self, widget, **kwargs):
        row_change = kwargs.get("row_change", 0)
        column_change = kwargs.get("column_change", 0)
        abs_x = kwargs.get("x", None)
        abs_y = kwargs.get("y", None)
        if abs_x is not None:
            widget.boundx = abs_x
        if abs_y is not None:
            widget.boundy = abs_y
        widget.boundx += column_change
        widget.boundy += row_change
        widget.bounding_rect.x = widget.boundx
        widget.bounding_rect.y = widget.boundy
        self.calculate_widget_pos(widget)
    def calculate_widget_pos(self, widget):
        if widget.sticky:
            if "n" in widget.sticky and "s" in widget.sticky:
                widget.rect.height = widget.bounding_rect.height
            if "e" in widget.sticky and "w" in widget.sticky:
                widget.rect.width = widget.bounding_rect.width
            if "n" in widget.sticky:
                widget.rect.top = widget.bounding_rect.top
            if "s" in widget.sticky:
                widget.rect.bottom = widget.bounding_rect.bottom
            if "e" in widget.sticky:
                widget.rect.left = widget.bounding_rect.left
            if "w" in widget.sticky:
                widget.rect.right = widget.bounding_rect.right
            if not "n" in widget.sticky and not "s" in widget.sticky:
                widget.rect.centery = widget.bounding_rect.centery
            if not "w" in widget.sticky and not "e" in widget.sticky:
                widget.rect.centerx = widget.bounding_rect.centerx
        else:
            widget.rect.center = widget.bounding_rect.center
        """
        To prevent widgets from going past the left and top borders of their columns and rows.
        if widget.rect.left < widget.bounding_rect.left:
            widget.rect.left = widget.bounding_rect.left
        if widget.rect.top < widget.bounding_rect.top:
            widget.rect.top = widget.bounding_rect.top
        """
        widget.resize()
        widget.calculate_pos()
    def update(self, **kwargs):
        event = kwargs.get("event", None)
        for row in self.widget_grid:
            for column in row:
                for widget in column:
                    widget.update(event=event)
    def draw(self):
        for row in self.widget_grid:
            for column in row:
                for widget in column:
                    widget.draw()

