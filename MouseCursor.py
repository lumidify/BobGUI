import os
import pygame
class MouseCursor():
    def __init__(self, screen, image):
        self.screen = screen
        self.image = image
        self.update()
    def update(self):
        self.pos = pygame.mouse.get_pos()
    def draw(self):
        self.screen.blit(self.image, self.pos)
