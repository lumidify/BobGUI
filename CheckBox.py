import os
import Widget
import pygame
from pygame.locals import *
from Image import ScaledImage
class CheckBox(Widget.Widget):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.screen = self.parent.screen
        self.normal_image = ScaledImage(self.screen, os.path.join("..", "..", "images", "checkbox_normal.png"))
        self.checked_image = ScaledImage(self.screen, os.path.join("..", "..", "images", "checkbox_checked.png"))

        self.boundwidth = kwargs.get("width", self.normal_image.width)
        self.boundheight = kwargs.get("height", self.normal_image.height)
        self.rect = Rect(0, 0, self.boundwidth, self.boundheight)
        self.bounding_rect = Rect(0, 0, self.boundwidth, self.boundheight)
        self.checked = kwargs.get("checked", False)
        self.pressed = False
    def update_screen(self, screen):
        self.screen = screen
        for image in [self.normal_image, self.checked_image]:
            image.screen = screen
    def resize_images(self):
        for image in [self.normal_image, self.checked_image]:
            image.resize(width=self.rect.width, height=self.rect.height)
    def resize(self, **kwargs):
        temp_width, temp_height = self.rect.width, self.rect.height
        super().resize(**kwargs)
        if temp_width != self.rect.width or temp_height != self.rect.height:
            self.resize_images()
    def calculate_pos(self):
        super().calculate_pos()
        for image in [self.normal_image, self.checked_image]:
            image.x = self.rect.x
            image.y = self.rect.y
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        collide_button = self.rect.collidepoint(mouse_pos)
        if event.type == MOUSEBUTTONDOWN:
            if collide_button:
                self.pressed = True
        elif event.type == MOUSEBUTTONUP:
            if collide_button:
                if self.pressed:
                    if self.checked:
                        self.checked = False
                    else:
                        self.checked = True
                    self.pressed = False
    def draw(self):
        if self.checked:
            image = self.checked_image
        else:
            image = self.normal_image
        image.draw()

