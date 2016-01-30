import pygame
from pygame.locals import*
class Image():
    def __init__(self, screen, image, position, fade_speed, screen_size, align_method):
        self.screen = screen
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.fade_speed = fade_speed
        self.opacity = 255
        self.fadein = False
        self.fadeout = False
        self.position = position
        self.screen_size = screen_size
        self.align_method = align_method
        if self.align_method == "absolute":
            self.rect.topleft = self.position
        elif self.align_method == "relative_middle":
            self.rect.center = [self.screen_size[0]//2-self.position[0], self.screen_size[1]//2-self.position[1]]
    def update(self):
        if self.fadein:
            self.opacity += self.fade_speed
            if self.opacity >= 255:
                self.fadein = False
                if self.after_fadein_func != None:
                    self.after_fadein_func()
        elif self.fadeout:
            self.opacity -= self.fade_speed
            if self.opacity <= 0:
                self.fadeout = False
                if self.after_fadeout_func != None:
                    self.after_fadeout_func()
        if self.align_method == "relative_middle":
            self.rect.center = [self.screen_size[0]//2-self.position[0], self.screen_size[1]//2-self.position[1]]
    def update_screen_size(self, screen_size):
        self.screen_size = screen_size
    def fade_in(self, function=None):
        self.fadein = True
        self.opacity = 0
        self.after_fadein_func = function
    def fade_out(self, function=None):
        self.fadeout = True
        self.opacity = 255
        self.after_fadeout_func = function
    def draw(self):
            self.image.set_alpha(self.opacity)
            self.screen.blit(self.image, self.rect)
