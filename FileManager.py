import os
import sys
import pygame
import locale
import functools
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Choose a file...")
screen = pygame.display.set_mode((1000, 500))
font = pygame.font.SysFont(None, 20)
class Button():
    def __init__(self, text, command, left, top):
        self.normal_color = (255, 255, 255)
        self.current_color = self.normal_color
        self.highlighted_color = (100, 100, 100)
        self.clicked_color = (255, 0, 0)
        self.text = text
        self.highlighted = False
        self.clicked = False
        self.left = left
        self.top = top
        self.rect = font.render(self.text, True, self.current_color).get_rect()
        self.rect.left = self.left
        self.rect.top = self.top
        self.command = command
    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == MOUSEMOTION:
            if self.rect.collidepoint(mouse_pos):
                self.highlighted = True
            else:
                self.highlighted = False
        elif event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mouse_pos):
                self.clicked = True
        elif event.type == MOUSEBUTTONUP:
            if self.rect.collidepoint(mouse_pos):
                self.clicked = False
                if self.command != None:
                    self.command()
    def draw(self):
        self.current_color = self.normal_color
        if self.highlighted:
            self.current_color = self.highlighted_color
        if self.clicked:
            self.current_color = self.clicked_color
        screen.blit(font.render(self.text, True, self.current_color), (self.left, self.top))
class fileManager():
    def __init__(self):
        self.current_dir = "/"
        self.gui = []
        self.create_gui()
    def list_files(self):
        files_folders = os.listdir(self.current_dir)
        files = []
        folders = []
        for file_or_folder in files_folders:
            full_path = os.path.join(self.current_dir, file_or_folder)
            if os.path.isfile(full_path):
                files.append(file_or_folder)
            elif os.path.isdir(full_path):
                folders.append(file_or_folder)
            #for case-insensitive sorting - wouldn't work for all languages
            #files = sorted(files, key=str.lower)
            #folders = sorted(folders, key=str.lower)
        return (sorted(files, key=functools.cmp_to_key(locale.strcoll)), sorted(folders, key=functools.cmp_to_key(locale.strcoll)))
    def create_gui(self):
        (files, folders) = self.list_files()
        self.gui = []
        counter = 45
        for folder in folders:
            self.gui.append(Button(folder, lambda folder = folder: self.change_directory(folder), 5, counter))
            counter += 15
        counter = 45
        for file in files:
            self.gui.append(Button(file, lambda file = file: self.open_file(file), 500, counter))
            counter += 15
        self.gui.append(Button("Back", self.go_back, 5, 5))
    def change_directory(self, folder):
        try:
            os.listdir(os.path.join(self.current_dir, folder))
            self.current_dir = os.path.join(self.current_dir, folder)
            self.create_gui()
        except:
            return
    def go_back(self):
        try:
            self.current_dir = os.path.split(self.current_dir)[0]
            self.create_gui()
        except:
            return
    def open_file(self, file):
        os.system('xdg-open ' + os.path.join(self.current_dir, file))
    def update(self, event):
        for button in self.gui:
            button.update(event)
    def draw(self):
        for button in self.gui:
            button.draw()
fileManager = fileManager()
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        else:
            fileManager.update(event)
    fileManager.draw()
    pygame.display.update()
