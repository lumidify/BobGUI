import os
import sys
import math
import Widget
import pygame
from pygame.locals import *

class TiledImage():
    def __init__(self, screen, image, **kwargs):
        self.screen = screen
        self.image = pygame.image.load(image).convert_alpha()
        self.image_width, self.image_height = self.image.get_size()
        self.width = kwargs.get("width", self.image_width)
        self.height = kwargs.get("height", self.image_height)
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.gen_tiled_image()
    def gen_tiled_image(self):
        self.tiled_image = pygame.surface.Surface((self.width, self.height))
        for y in range(math.ceil(self.height / self.image_height)):
            for x in range(math.ceil(self.width / self.image_width)):
                self.tiled_image.blit(self.image, (x * self.image_width, y * self.image_height))
    def resize(self, **kwargs):
        changex = kwargs.get("changex", 0)
        changy = kwargs.get("changey", 0)
        absx = kwargs.get("width", None)
        absy = kwargs.get("height", None)
        if absx is not None:
            self.width = absx
        if absy is not None:
            self.height = absy
        self.width += changex
        self.height += changy
        self.gen_tiled_image()
    def update_screen(self, screen):
        self.screen = screen
    def draw(self):
        self.screen.blit(self.tiled_image, (self.x, self.y))

class ScaledImage():
    def __init__(self, screen, image, **kwargs):
        self.screen = screen
        self.image = pygame.image.load(image).convert_alpha()
        self.region = kwargs.get("region", None)

        if self.region:
            temp_surf = pygame.surface.Surface(Rect(self.region).size)
            temp_surf.blit(self.image, (0, 0), self.region)
            self.image = temp_surf

        self.scaled_image = self.image
        self.keep_aspect_ratio = kwargs.get("keep_aspect_ratio", False)
        image_width, image_height = self.image.get_size()
        self.width = kwargs.get("width", image_width)
        self.height = kwargs.get("height", image_height)
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.gen_scaled_image()
    def gen_scaled_image(self):
        current_w, current_h = self.image.get_size()
        new_width = 0
        new_height = 0
        if self.keep_aspect_ratio:
            if self.width > self.height:
                scale_factor = self.width / current_w
                new_height = scale_factor * current_h
                if new_height > self.height:
                    scale_factor = self.height / current_h
                    new_width = scale_factor * current_w
                    new_height = self.height
                else:
                    new_width = self.width
            else:
                scale_factor = self.height / current_h
                new_width = scale_factor * current_w
                if new_width > self.width:
                    scale_factor = self.width / current_w
                    new_height = scale_factor * current_h
                    new_width = self.width
                else:
                    new_height = self.height
        else:
            scalex = self.width / current_w
            scaley = self.height / current_h
            new_width = scalex * current_w
            new_height = scaley * current_h
        try:
            self.width = new_width
            self.height = new_height
            self.scaled_image = pygame.transform.scale(self.image, (int(new_width), int(new_height)))
        except ValueError:
            pass
    def update_screen(self, screen):
        self.screen = screen
    def resize(self, **kwargs):
        changex = kwargs.get("changex", 0)
        changey = kwargs.get("changey", 0)
        absx = kwargs.get("width", None)
        absy = kwargs.get("height", None)
        if absx is not None:
            self.width = absx
        if absy is not None:
            self.height = absy
        self.width += changex
        self.height += changey
        self.gen_scaled_image()
    def update_screen(self, screen):
        self.screen = screen
    def draw(self):
        self.screen.blit(self.scaled_image, (self.x, self.y))

class Image():
    def __init__(self, screen, config, **kwargs):
        self.screen = screen
        self.config = config
        self.width = kwargs.get("width", 0)
        self.height = kwargs.get("height", 0)
        self.load_config()
    def load_config(self):
        self.images = []
        for image in self.config:
            if image[0] == "scaled":
                self.images.append(ScaledImage(self.screen, image[1]))
            elif image[0] == "tiled":
                self.image.append(TiledImage(self.screen, image[1]))
        self.gen_image()
    def gen_image(self):
        for index, image in enumerate(self.config):
            if image[2] == "resize":
                pass
if __name__ == "__main__":
    pygame.init()
    screen_info = pygame.display.Info()
    #screen_size = [screen_info.current_w, screen_info.current_h]
    screen_size = [750, 200]
    screen = pygame.display.set_mode(screen_size, RESIZABLE)
    fullscreen = False
    last_size = screen_size
    #image = Image(screen, [["scaled", "./left.png", "static"], ["scaled", "./center.png", "resize"], ["scaled",
    #                                                                              "./right.png",
    #                                                                                                  "static"]], keep_aspect_ratio=False)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                screen_size = event.dict["size"]
                screen = pygame.display.set_mode(screen_size, RESIZABLE)
                image.resize(width=screen_size[0], height=screen_size[1])
            elif event.type == KEYDOWN:
                if event.key == K_F11:
                    #pygame.display.toggle_fullscreen()
                    pygame.display.quit()
                    pygame.display.init()
                    if fullscreen:
                        screen_size = last_size
                        screen = pygame.display.set_mode(screen_size, RESIZABLE)
                    else:
                        last_size = screen_size
                        screen_size = (screen_info.current_w, screen_info.current_h)
                        screen = pygame.display.set_mode(screen_size, FULLSCREEN)
                    fullscreen = not fullscreen
                    image.resize(width=screen_size[0], height=screen_size[1])
                    image.update_screen(screen)
        image.draw()
        pygame.display.update()
