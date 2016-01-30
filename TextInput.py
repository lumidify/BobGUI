import os
import sys
import pygame
from Cursor import Cursor
from SelectableText import SelectableText
from pygame.locals import *
class TextInput():
    def __init__(self, screen, position, dimensions, command=None):
        self.screen = screen
        self.x = position[0]
        self.y = position[1]
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.rect = Rect((self.x, self.y), (self.width, self.height))
        self.command = command
        self.message = []
        #self.font = pygame.font.Font(os.path.join("data", "font", "Lumidify_Casual.ttf"), 25)
        self.font = pygame.font.Font(os.path.join("..", "..", "font", "Lumidify_Casual.ttf"), 25)
        self.text = SelectableText(screen, "", self.font, [5, 5])
        self.focused = False
        self.highlighted = False
        self.cursor = Cursor("|", 0, 700, 500)
    def update(self, event):
        significant_event = False
        mouse_pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(mouse_pos):
            self.focused = True
            self.cursor.start()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1 and not self.rect.collidepoint(mouse_pos):
            self.focused = False
            self.cursor.stop()
        elif event.type == MOUSEMOTION:
            if self.rect.collidepoint(mouse_pos):
                self.highlighted = True
            else:
                self.highlighted = False
        elif event.type == KEYDOWN and self.focused:
            significant_event = True
            if event.key == K_BACKSPACE:
                if self.cursor.pos > 0:
                    self.message.pop(self.cursor.pos - 1)
                    self.cursor.pos -= 1
            elif event.key == K_DELETE:
                if self.cursor.pos < len(self.message):
                    self.message.pop(self.cursor.pos)
            elif event.key == K_RETURN:
                if self.command != None:
                    self.command()
            elif event.key == K_LEFT:
                if self.cursor.pos > 0:
                    self.cursor.pos -= 1
            elif event.key == K_RIGHT:
                if self.cursor.pos < len(self.message):
                    self.cursor.pos += 1
            else:
                self.message.insert(self.cursor.pos, event.unicode)
                self.cursor.pos += 1
        if significant_event:
            self.cursor.event()
        self.change_color()
        self.text.update(event)
    def change_color(self):
        if self.highlighted:
            self.color = (0, 0, 200)
        elif self.focused:
            self.color = (0, 0, 150)
        else:
            self.color = (0, 0, 100)
    def draw(self):
        self.text.change_text("".join(self.message))
        self.cursor.update()
        self.before_cursor_width = self.font.size("".join(self.message[:self.cursor.pos]))[0]
        self.text_width, self.text_height = self.font.size(self.text.text)
        #self.screen.blit(self.font.render(self.text, 1, (255, 255, 255)), (self.x + 5, self.y + (self.height - self.text_height)//2))
        if self.cursor.visible:
            self.screen.blit(self.font.render(self.cursor.string, 1, (255, 255, 255)), (self.x + 5 + self.before_cursor_width, self.y + (self.height - self.text_height)//2))
        pygame.draw.rect(self.screen, self.color, self.rect, 2)
        self.text.draw()
if __name__ == "__main__":
    pygame.init()
    pygame.key.set_repeat(500, 20)
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    gui = [TextInput(screen, [0, 0], [200, 30])]
    while True:
        clock.tick(30)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                for widget in gui:
                    widget.update(event)
        for widget in gui:
            widget.draw()
        pygame.display.update()
