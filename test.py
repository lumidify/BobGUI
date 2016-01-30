import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500, 500))
font = pygame.font.Font("nastaleeq.ttf", 20)
font.set_underline(True)
print(font.get_height())
print(font.size("Hello, World!"))
surface = font.render(" نچلا پانی اوپر کے پانی سے الگ ہو جائے۔", True, (255, 255, 255))
print(len(" نچلا پانی اوپر کے پانی سے الگ ہو جائے۔"))
surf_rect = surface.get_rect()
print(surf_rect.width, surf_rect.height)

running = True

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    screen.blit(surface, (50, 50))
    #screen.blit(surface, (52, 52))
    pygame.display.update()