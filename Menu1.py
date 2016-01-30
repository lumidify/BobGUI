import pygame
from pygame.locals import*
class Menu():
    def __init__(self, position, screen_size, widgets):
        self.position = position
        self.screen_size = screen_size
        self.widgets = widgets
        self.highlighted_widget = 0
        if len(self.widgets) > 0:
            self.widgets[0].highlighted = True
            self.widgets[0].change_image()
    def append(self, widgets):
        for widget in widgets:
            self.widgets.append(widget)
        if len(self.widgets) == len(widgets):
            self.widgets[0].highlighted = True
    def insert(self, widgets, index):
        for widget in widgets:
            self.widgets.insert(widgets, index)
        if len(self.widgets) == len(widgets):
            self.widgets[0].highlighted = True
    def update(self, event):
        if event.type == KEYDOWN:
            if event.key == K_DOWN or event.key == K_RIGHT:
                self.next_menu_item()
            elif event.key == K_UP or event.key == K_LEFT:
                self.last_menu_item()
            elif event.key == K_RETURN:
                self.widgets[self.highlighted_widget].pressed = True
        elif event.type == KEYUP:
            if event.key == K_RETURN:
                temp = self.widgets[self.highlighted_widget]
                temp.pressed = False
                if temp.command != None:
                    temp.command()
        for widget in self.widgets:
            widget.update(event)
    def next_menu_item(self):
        self.widgets[self.highlighted_widget].highlighted = False
        if self.highlighted_widget == len(self.widgets) - 1:
            self.highlighted_widget = 0
        else:
            self.highlighted_widget += 1
        self.widgets[self.highlighted_widget].highlighted = True
    def last_menu_item(self):
        self.widgets[self.highlighted_widget].highlighted = False
        if self.highlighted_widget == 0:
            self.highlighted_widget = len(self.widgets) - 1
        else:
            self.highlighted_widget -= 1
        self.widgets[self.highlighted_widget].highlighted = True
    def update_screen_size(self, screen_size):
        self.screen_size = screen_size
        for widget in self.widgets:
            widget.update_screen_size(self.screen_size)
    def draw(self):
        for widget in self.widgets:
            widget.draw()
