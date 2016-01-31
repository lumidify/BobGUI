import os
import pygame
from pygame.locals import *
import Widget
from Image import ScaledImage
class RadioButtonGroup():
    def __init__(self, **kwargs):
        self.selected = None
        self.callback = kwargs.get("callback", None)
    def select(self, button):
        if self.selected:
            self.selected.selected = False
        self.selected = button
        self.selected.selected = True
        if self.callback:
            self.callback(self.selected)
class RadioButton(Widget.Widget):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.screen = self.parent.screen

        #self.label = kwargs.get("text", None)
        #self.font = pygame.font.Font(os.path.join("..", "..", "font", "Lumidify_Casual.ttf"), 20)
        self.normal_image = ScaledImage(self.screen, os.path.join("..", "..", "images", "radiobutton_normal.png"))
        self.selected_image = ScaledImage(self.screen, os.path.join("..", "..", "images", "radiobutton_selected.png"))
        self.boundwidth = kwargs.get("width", self.normal_image.width)
        self.boundheight = kwargs.get("height", self.normal_image.height)
        self.rect = Rect(0, 0, self.boundwidth, self.boundheight)
        self.bounding_rect = Rect(0, 0,  self.boundwidth, self.boundheight)
        self.pressed = False
        self.selected = kwargs.get("selected", False)
        self.group = kwargs.get("group", None)
        if self.selected and self.group:
            self.group.select(self)
        self.resize_images()
    def update_screen(self, screen):
        self.screen = screen
        for image in [self.normal_image, self.selected_image]:
            image.screen = screen
    def resize_images(self):
        for image in [self.normal_image, self.selected_image]:
            image.resize(width=self.rect.width, height=self.rect.height)
    def resize(self, **kwargs):
        temp_width, temp_height = self.rect.width, self.rect.height
        super().resize(**kwargs)
        if temp_width != self.rect.width or temp_height != self.rect.height:
            self.resize_images()
    def calculate_pos(self):
        super().calculate_pos()
        for image in [self.normal_image, self.selected_image]:
            image.x = self.rect.x
            image.y = self.rect.y
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        collide_button = self.rect.collidepoint(mouse_pos)
        if event.type == MOUSEBUTTONDOWN:
            if collide_button:
                self.pressed = True
            else:
                self.pressed = False
        elif event.type == MOUSEBUTTONUP:
            if self.pressed:
                if collide_button:
                    self.selected = True
                    if self.group:
                        self.group.select(self)
            self.pressed = False
    def draw(self):
        if self.selected:
            image = self.selected_image
        else:
            image = self.normal_image
        image.draw()
