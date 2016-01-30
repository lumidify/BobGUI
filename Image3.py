import pygame
from pygame.locals import*
class Image():
    def __init__(self, screen, image, pos, **kwargs):
        self.screen = screen
        self.raw_image = pygame.image.load(image).convert_alpha()
        self.raw_size = [self.raw_image.get_width(), self.raw_image.get_height()]
        self.image = self.raw_image
        self.pos = pos
        self.opacity = kwargs.get("opacity", 255)
        self.area = kwargs.get("area", [0, 0, 0, 0])
        self.gen_rect()
        
        self.size = kwargs.get("size", None)
        if self.size != None:
            self.set_size(self.size)
            
        self.scale = kwargs.get("scale", None)
        if self.scale != None:
            self.set_scale(self.scale)

    def set_scale(self, scale):
        self.scale = scale
        self.image = pygame.transform.smoothscale(self.raw_image, [round(self.raw_size[0] * self.scale[0]), round(self.raw_size[1] * self.scale[1])])
        self.gen_rect()
    def set_size(self, size):
        self.size = size
        self.image = pygame.transform.smoothscale(self.raw_image, self.size)
        self.gen_rect()
    def set_pos(self, pos):
        self.pos = pos
        self.rect.topleft = self.pos
    def gen_rect(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.area[2], self.area[3] = self.rect.width, self.rect.height
    def draw(self):
        self.image.set_alpha(self.opacity)
        self.screen.blit(self.image, self.rect, self.area)

class GUISprite():
    def __init__(self, screen, pos, images, **kwargs):
        self.screen = screen
        self.pos = pos
        self.image_paths = images
        self.areas = kwargs.get("areas", [None, None, None])
        self.images = [Image(self.screen, self.image_paths["normal"], self.pos), Image(self.screen, self.image_paths["highlighted"], self.pos), Image(self.screen, self.image_paths["pressed"], self.pos)]
    def set_scale(self, scale):
        self.scale = scale
        for image in self.images:
            image.set_scale(self.scale)
    def set_pos(self, pos):
        self.pos = pos
        for image in self.images:
            image.set_pos(self.pos)
    def set_size(self, size):
        self.size = size
        for image in self.images:
            image.set_size(self.size)
    def draw(self, state):
        if state == "normal":
            self.current_image = 0
        elif state == "highlighted":
            self.current_image = 1
        else:
            self.current_image = 2
        self.images[self.current_image].draw()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    image = Image(screen, "peach/glassbutton.png", [100, 250], scale=(1.5, 1.5), size=(100, 100))
    while True:
        image.draw()
        pygame.display.update()