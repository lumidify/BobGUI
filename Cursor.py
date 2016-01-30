import pygame
from helper_functions import refine_index
class Cursor():
    """
    string: the character to be displayed as the cursor
    pos: the initial position of the cursor
    visible_time: the amount of time in milliseconds the cursor should be visible in each blink
    hidden_time: the amount of time in milliseconds the cursor should be hidden in each blink
    """
    def __init__(self, string, visible_time, hidden_time, pos):
        self.string = string
        self.x = 0
        self.y = 0
        self.pixelx = 0
        self.pixely = 0
        self.pos = pos
        self.visible_time = visible_time
        self.hidden_time = hidden_time
        self.time_passed = visible_time
        self.blink_counter = 0
        self.change_in_time = 0
        self.visible = False
        self.blinking = False
        self.current_time = pygame.time.get_ticks()
    def move_up(self, size_list):
        if self.y > 0:
            self.y += -1
            self.x = refine_index(self.x, self.pixelx, size_list[self.y])
    def move_down(self, size_list):
        if self.y < len(size_list) - 1:
            self.y += 1
            self.x = refine_index(self.x, self.pixelx, size_list[self.y])
    def calc_pixel_pos(self, size_list, font_height):
        self.pixelx = size_list[self.y][self.x] + self.pos[0]
        self.pixely = self.y * font_height + self.pos[1]
    def update(self):
        if self.blinking:
            self.change_in_time = pygame.time.get_ticks() - self.current_time
            self.current_time += self.change_in_time
            self.time_passed += self.change_in_time
            self.blink()
    def event(self):
        if self.blinking:
            self.time_passed = 0
            self.visible = True
    def blink(self):
        if self.time_passed >= self.visible_time:
            self.blink_counter += self.change_in_time
            if self.visible:
                if self.blink_counter >= self.visible_time:
                    self.visible = False
                    self.blink_counter = 0
            else:
                if self.blink_counter >= self.hidden_time:
                    self.visible = True
                    self.blink_counter = 0
    def start(self):
        self.blinking = True
        self.visible = True
        self.blink_counter = 0
        self.time_passed = self.visible_time
        self.current_time = pygame.time.get_ticks()
    def stop(self):
        self.blinking = False
        self.visible = False
