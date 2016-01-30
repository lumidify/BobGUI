import sys
import pygame
import Widget
from pygame.locals import *
from Image import ScaledImage
class ScrollBar(Widget.Widget):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.highlighted = False
        self.selected = False

        self.axis = kwargs.get("axis", "vertical")
        self.scrollarea_size = kwargs.get("scrollarea_size", (0, 0))

        self.boundwidth = kwargs.get("width", 0)
        self.boundheight = kwargs.get("height", 0)
        self.rect = Rect(0, 0, self.boundwidth, self.boundheight)
        self.bounding_rect = Rect(0, 0, self.boundwidth, self.boundheight)
        self.handle_rect = Rect(0, 0, 0, 0)

        if self.axis == "vertical":
            self.background_image = ScaledImage(self.screen, "./peach/glassspinner.png", region=(97, 1, 62, 89))
            self.normal_image = ScaledImage(self.screen, "./peach/glassspinner_focus.png", region=(97, 1, 62, 89))
            self.highlighted_image = ScaledImage(self.screen, "./peach/glassspinner_halo.png", region=(97, 1, 62, 89))
            self.pressed_image = ScaledImage(self.screen, "./peach/glassspinner_focus.png", region=(97, 1, 62, 89))
        elif self.axis == "horizontal":
            self.background_image = ScaledImage(self.screen, "./peach/glassspinner.png", region=(97, 1, 62, 89))
            self.normal_image = ScaledImage(self.screen, "./peach/glassspinner_focus.png", region=(97, 1, 62, 89))
            self.highlighted_image = ScaledImage(self.screen, "./peach/glassspinner_halo.png", region=(97, 1, 62, 89))
            self.pressed_image = ScaledImage(self.screen, "./peach/glassspinner_focus.png", region=(97, 1, 62, 89))

        self.calculate_handle_size()
        self.selected_point = []
        self.pos = 0
    def update_screen(self, screen):
        self.screen = screen
        for image in [self.normal_image, self.highlighted_image, self.pressed_image, self.background_image]:
            image.screen = self.screen
    def calculate_handle_size(self):
        if self.axis == "vertical":
            try:
                self.handle_rect.height = self.rect.height / self.scrollarea_size[1] * self.rect.height
            except ZeroDivisionError:
                self.handle_rect.height = 0
            self.handle_rect.width = self.rect.width
        elif self.axis == "horizontal":
            try:
                self.handle_rect.width = self.rect.width / self.scrollarea_size[0] * self.rect.width
            except ZeroDivisionError:
                self.handle_rect.width = 0
            self.handle_rect.height = self.rect.height
        if self.handle_rect.width > self.rect.width:
            self.handle_rect.width = self.rect.width
        if self.handle_rect.height > self.rect.height:
            self.handle_rect.height = self.rect.height
        for image in [self.normal_image, self.highlighted_image, self.pressed_image]:
            image.resize(width=self.handle_rect.width, height=self.handle_rect.height)
    def update_box_size(self, new_size):
        self.scrollarea_size = new_size
        self.calculate_handle_size()
    def scroll(self, **kwargs):
        decimal_change = kwargs.get("decimal", None)
        real_change = kwargs.get("pixel_change", None)
        abs_decimal = kwargs.get("pos", None)
        abs_pixel = kwargs.get("pixel_pos", None)

        if decimal_change is not None:
            self.pos += decimal_change

        elif real_change is not None:
            if self.axis == "vertical":
                try:
                    self.pos += real_change / (self.rect.height - self.handle_rect.height)
                except ZeroDivisionError:
                    self.pos = 0
            elif self.axis == "horizontal":
                try:
                    self.pos += real_change / (self.rect.width - self.handle_rect.width)
                except ZeroDivisionError:
                    self.pos = 0

        elif abs_decimal is not None:
            self.pos = abs_decimal

        elif abs_pixel is not None:
            if self.axis == "vertical":
                try:
                    self.pos = (abs_pixel - self.rect.y) / (self.rect.height - self.handle_rect.height)
                except ZeroDivisionError:
                    self.pos = 0
            elif self.axis == "horizontal":
                try:
                    self.pos = (abs_pixel - self.rect.x) / (self.rect.width - self.handle_rect.width)
                except ZeroDivisionError:
                    self.pos = 0

        if self.pos < 0:
            self.pos = 0
        elif self.pos > 1:
            self.pos = 1

        if self.axis == "vertical":
            self.handle_rect.y = self.pos * (self.rect.height - self.handle_rect.height) + self.rect.y
            self.handle_rect.x = self.rect.x
        elif self.axis == "horizontal":
            self.handle_rect.x = self.pos * (self.rect.width - self.handle_rect.width) + self.rect.x
            self.handle_rect.y = self.rect.y

        for image in [self.normal_image, self.highlighted_image, self.pressed_image]:
            image.x = self.handle_rect.x
            image.y = self.handle_rect.y
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        collide_handle = self.handle_rect.collidepoint(mouse_pos)
        collide_background_rect = self.rect.collidepoint(mouse_pos)

        if collide_handle:
            self.highlighted = True
        else:
            self.highlighted = False
        if event.type == MOUSEMOTION:
            if self.selected:
                if self.axis == "vertical":
                    self.scroll(pixel_pos=mouse_pos[1] - self.selected_point[1])
                elif self.axis == "horizontal":
                    self.scroll(pixel_pos=mouse_pos[0] - self.selected_point[0])
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            if collide_handle:
                self.set_selected(mouse_pos)
            elif collide_background_rect and not collide_handle:
                if self.axis == "vertical":
                    self.scroll(pixel_change=mouse_pos[1] - self.handle_rect.centery)
                elif self.axis == "horizontal":
                    self.scroll(pixel_change=mouse_pos[0] - self.handle_rect.centerx)
                self.set_selected(mouse_pos)
            else:
                self.selected = False
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            self.selected = False
    def resize(self, **kwargs):
        super().resize(**kwargs)
        self.calculate_handle_size()
        self.background_image.resize(width=self.rect.width, height=self.rect.height)
        self.scroll()
    def calculate_pos(self):
        super().calculate_pos()
        self.background_image.x = self.rect.x
        self.background_image.y = self.rect.y
    def set_selected(self, mouse_pos):
        self.selected = True
        self.selected_point = [mouse_pos[0] - self.handle_rect.x, mouse_pos[1] - self.handle_rect.y]
    def draw(self):
        image = self.normal_image
        if self.highlighted:
            image = self.highlighted_image
        if self.selected:
            image = self.pressed_image
        self.background_image.draw()
        image.draw()
