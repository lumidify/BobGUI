import os
import sys
import pygame
from pygame.locals import *

class MenuItem():
    def __init__(self, screen, text, font, pos, size, command, **kwargs):
        self.screen = screen
        self.text = text
        self.font = font
        self.pos = pos
        self.size = size
        self.command = command
        self.is_submenu = kwargs.get("is_submenu", False)
        self.icon = kwargs.get("icon", None)
        self.submenu = kwargs.get("submenu", None)
        if self.is_submenu:
            self.submenu = Menu(self.screen, (0, 0), self.font, self.submenu)
        if self.icon != None:
            self.icon = os.path.join(self.icon)
        self.selected = False
        self.pressed = False
        self.disabled = False
        self.color = (30, 30, 30)
        self.text_color = (255, 255, 255)
        self.rect = Rect(self.pos, self.size)
        self.update_pos_size()
    def collide(self, mouse_pos):
        collide = False
        if self.rect.collidepoint(mouse_pos):
            collide = True
        elif self.is_submenu and self.selected:
            if self.submenu.collide(mouse_pos)[0]:
                collide = True
        return collide
    def update_pos_size(self):
        if self.is_submenu:
            self.submenu.pos = (self.pos[0] + self.size[0], self.pos[1])
            self.submenu.update_pos_size()
    def update(self, event):
        self.rect = Rect(self.pos, self.size)
        mouse_pos = pygame.mouse.get_pos()
        if not self.disabled:
            if self.collide(mouse_pos):
                self.selected = True
                if self.is_submenu:
                    self.submenu.visible = True
            else:
                if self.is_submenu and self.submenu.visible:
                    self.selected = True
                else:
                    self.selected = False
            if self.is_submenu and self.selected:
                self.submenu.update(event)
    def set_visible(self, option):
        if option:
            self.selected = True
            if self.is_submenu:
                self.submenu.set_visible(True)
        else:
            self.selected = False
            if self.is_submenu:
                self.submenu.set_visible(False)
    def draw(self):
        self.text_color = (255, 255, 255)
        if self.selected:
            self.color = (100, 200, 100)
        elif self.disabled:
            self.text_color = (50, 50, 50)
            self.color = (30, 30, 30)
        else:
            self.color = (30, 30, 30)
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.font.render(self.text, True, self.text_color), (self.pos[0] + 10, self.pos[1] + 2))
        if self.is_submenu and self.selected:
            self.submenu.draw()
class Menu():
    def __init__(self, screen, pos, font, items):
        self.screen = screen
        self.pos = pos
        self.font = font
        self.items = items
        self.width = max([self.font.size(item.text)[0] for item in self.items]) + 20
        self.height = (self.font.get_height() + 4) * len(self.items)
        self.visible = False
        self.update_pos_size()
    def collide(self, mouse_pos):
        collide = False
        coll_item = None
        for item in self.items:
            if item.collide(mouse_pos):
                collide = True
                coll_item = item
                break
        return collide, coll_item
    def update_pos_size(self):
        for count in range(len(self.items)):
            self.items[count].pos = (self.pos[0], self.pos[1] + (self.font.get_height() + 4) * count)
            self.items[count].size = (self.width, self.font.get_height() + 4)
            self.items[count].update_pos_size()
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        collide, coll_item = self.collide(mouse_pos)
        if collide:
            for item in self.items:
                if item != coll_item:
                    item.set_visible(False)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
                self.pos = mouse_pos
                self.visible = True
                self.update_pos_size()
            elif event.button == 1:
                if not collide:
                    self.set_visible(False)

        if self.visible:
            for item in self.items:
                item.update(event)
    def set_visible(self, option):
        self.visible = False
        for item in self.items:
            item.set_visible(option)
    def draw(self):
        if self.visible:
            for item in self.items:
                item.draw()
class ContextMenu():
    def __init__(self, screen, items, font, width, height):
        self.screen = screen
        self.items = items
        self.pos = (0, 0)
        self.font = font
        self.visible = False
        self.rect = Rect(0, 0, width, height * len(self.items))
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self.menu.update(event)
    def draw(self):
        if self.visible:
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect)
pygame.init()
screen = pygame.display.set_mode((500, 500))
font = pygame.font.Font(os.path.join("..", "..", "font", "Lumidify_Casual.ttf"), 20)
#test = ContextMenu(screen, ["Hello", "Bye", "Your face!", "What's up?", "Yo!", "Mwahahahaha"], font, 200, 20)
test = Menu(screen, (0, 0), font, [
    MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
    MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
    MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
    MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
    MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
    MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None, is_submenu=True, submenu=[
        MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
        MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
        MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
        MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None, is_submenu=True, submenu=[
            MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
            MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
            MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
            MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None)])]),
    MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None, is_submenu=True, submenu=[
        MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
        MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
        MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
        MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None, is_submenu=True, submenu=[
            MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
            MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
            MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None),
            MenuItem(screen, "Hi! How are you?", font, (0, 0), (0, 0), None)])])
    ])

while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        test.update(event)
    test.draw()
    pygame.display.update()
