import pygame
from pygame.locals import *
screen = pygame.display.set_mode((0, 0), RESIZABLE)
while True:
    for event in pygame.event.get():
        print(pygame.event.event_name(event.type))
        if event.type == KEYDOWN:
            print(pygame.key.name(event.key))
            print(repr(event.unicode))
