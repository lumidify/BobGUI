import pygame
from pygame.locals import*
class basicText():
    def __init__(self, screen, text, font, color, position, fade_speed, centerx=True, centery=True):
        self.screen = screen
        self.text = font.render(text, 1, color)
        self.position = position
        self.size = font.size(text)
        if centerx:
            self.position[0] -= self.size[0]//2
        if centery:
            self.position[1] -= self.size[1]//2
        self.fade_speed = fade_speed
        self.opacity = 255
        self.fadein = False
        self.fadeout = False
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
    def fade_in(self, function=None):
        self.fadein = True
        self.opacity = 0
        self.after_fadein_func = function
    def fade_out(self, function=None):
        self.fadeout = True
        self.opacity = 255
        self.after_fadeout_func = function
    def draw(self):
            temp = pygame.Surface(self.size).convert()
            temp.blit(self.screen, (-self.position[0], -self.position[1]))
            temp.blit(self.text, (0, 0))
            temp.set_alpha(self.opacity)        
            self.screen.blit(temp, self.position)
