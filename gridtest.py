import os
import sys
#import pygame_sdl2 as pygame
#from pygame_sdl2.locals import *
import pygame
from pygame.locals import *
from Button import Button
from CheckBox import CheckBox
from ScrollBar import ScrollBar
from Grid import Grid
from RadioButton import RadioButton, RadioButtonGroup

if __name__ == "__main__":
    pygame.init()
    screen_info = pygame.display.Info()
    #screen_size = [screen_info.current_w, screen_info.current_h]
    screen_size = [750, 200]
    screen = pygame.display.set_mode(screen_size, RESIZABLE)
    root = Grid(None, screen)
    """
    button1 = Button(root, text="Hello, World! How are you?", command=sys.exit)
    button2 = Button(root, text="Hello!", command=sys.exit, padding=[10, 5, 10, 5])
    button3 = Button(root, text="Hello!", command=sys.exit)
    button4 = Button(root, text="Hello!", command=sys.exit)
    button5 = Button(root, text="Hello!", command=sys.exit)
    button6 = Button(root, text="Hello!", command=sys.exit)
    button7 = Button(root, text="Hello!", command=sys.exit)
    button8 = Button(root, text="Hello!", command=sys.exit)
    button9 = Button(root, text="Hello!", command=sys.exit)
    button10 = Button(root, text="Hello!", command=sys.exit)
    button1.grid(row=0, column=0)
    button2.grid(row=1, column=0)
    button3.grid(row=2, column=0)
    button4.grid(row=0, column=1)
    button5.grid(row=1, column=1, sticky="nswe")
    button6.grid(row=2, column=1)
    button7.grid(row=0, column=2)
    button8.grid(row=1, column=2)
    button9.grid(row=2, column=2)
    button10.grid(row=3, column=2)
    root.config_row(1, weight=1)
    root.config_row(2, weight=2)
    root.config_row(3, weight=3)
    root.config_column(1, weight=1)
    root.config_column(2, weight=2)
    """
    button = Button(root, text="Hello!", command=sys.exit)
    button.grid(row=0, column=0)
    widget4 = ScrollBar(root, width=200, height=20, scrollarea_size=(9000, 20), axis="horizontal")
    widget4.grid(row=0, column=2, sticky="we")
    widget = RadioButtonGroup()
    widget1 = RadioButton(root, group=widget, selected=True)
    widget2 = RadioButton(root, group=widget)
    widget3 = CheckBox(root)
    widget1.grid(row=1, column=1)
    widget2.grid(row=2, column=1)
    widget3.grid(row=2, column=2)
    root.config_column(2, weight=1)
    fullscreen = False
    last_size = screen_size
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                screen_size = event.dict["size"]
                screen = pygame.display.set_mode(screen_size, RESIZABLE)
                root.resize(width=screen_size[0], height=screen_size[1])
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
                    root.resize(width=screen_size[0], height=screen_size[1])
                    root.update_screen(screen)

            else:
                button.update(event)
                widget1.update(event)
                widget2.update(event)
                widget3.update(event)
                widget4.update(event)
                """
                button1.update(event)
                button2.update(event)
                button3.update(event)
                button4.update(event)
                button5.update(event)
                button6.update(event)
                button7.update(event)
                button8.update(event)
                button9.update(event)
                button10.update(event)
                """
        screen.fill((255, 255, 255))
        root.draw()
        pygame.display.update()
