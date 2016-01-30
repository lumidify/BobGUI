import sys
import pygame
import random
from pygame.locals import *

class QuadTree():
    def __init__(self, screen, rect, level, maxlevels, maxitems, particles=[], color = (255, 100, 100)):
        '''Quadtree box at with a current level, rect, list of particles, and color(if displayed)
        level: set to zero for "trunk" of quadtree
        rect: should be entire display for "trunk" of quadtree
        particles: list of all particles for collision testing'''
        self.screen = screen
        self.maxlevel = maxlevels#max number of subdivisions
        self.level = level#current level of subdivision
        self.maxparticles = maxitems#max number of particles without subdivision
        self.rect = rect#pygame rect object
        self.particles = particles#list of particles
        self.color = color#color of box if displayed
        self.branches = []#empty list that is filled with four branches if subdivided

    def subdivide(self):
        '''Subdivides quadtree into four branches'''
        for rect in self.rect_quad_split(self.rect):
            branch = QuadTree(self.screen, rect, self.level+1, self.maxlevel, self.maxparticles, [], self.color)
            self.branches.append(branch)
    def rect_quad_split(self, rect):
        '''Splits rect object into four smaller rect objects'''
        w=rect.width/2.0
        h=rect.height/2.0
        rl=[]
        rl.append(pygame.Rect(rect.left, rect.top, w, h))
        rl.append(pygame.Rect(rect.left+w, rect.top, w, h))
        rl.append(pygame.Rect(rect.left, rect.top+h, w, h))
        rl.append(pygame.Rect(rect.left+w, rect.top+h, w, h))
        return rl

    def add_particle(self, particle):
        '''Adds a particle to the list of particles inside quadtree box'''
        self.particles.append(particle)

    def subdivide_particles(self):
        '''Subdivides list of particles in current box to four branch boxes'''
        for particle in self.particles:
            for branch in self.branches:
                if branch.rect.colliderect(particle.rect):
                    branch.add_particle(particle)
        self.particles = []

    def draw(self):
        '''Displays quadtree box on the display surface given'''
        pygame.draw.rect(self.screen, self.color, self.rect, 1)
        for branch in self.branches:
            branch.draw()

    def test_collisions(self):
        '''Tests for collisions between all particles in the particle list'''
        for i, particle in enumerate(self.particles):
            for particle2 in self.particles[i+1:]:
                collide(particle, particle2)
    def clear(self):
        self.particles = []
        self.branches = []
    def update(self):
        '''Updates the quadtree and begins recursive process of subdividing or collision testing'''
        if len(self.particles) > self.maxparticles and self.level <= self.maxlevel:
            self.subdivide()
            self.subdivide_particles()
            for branch in self.branches:
                branch.update()
        else:
            pass
            #self.test_collisions()

class Particle():
    def __init__(self, screen, rect, vel, color=(255, 255, 255)):
        self.screen = screen
        self.rect = rect
        self.vel = vel
        self.color = color
    def update(self):
        if self.rect.x + self.rect.width >= 1000 or self.rect.x <= 0:
            self.vel[0] = -self.vel[0]
        if self.rect.y + self.rect.height >= 700 or self.rect.y <= 0:
            self.vel[1] = -self.vel[1]
            
        self.rect.move_ip(self.vel)
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

pygame.init()
screen = pygame.display.set_mode((1000, 700))
quadtree = QuadTree(screen, pygame.rect.Rect(0, 0, 1000, 700), 0, 5, 5)
particles = []
for x in range(0, 1000):
    particles.append(Particle(screen, Rect(random.randint(0, 500), random.randint(0, 500), random.randint(10, 20), random.randint(10, 20)), [random.randint(1, 5), random.randint(1, 5)]))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(30)
    screen.fill((0, 0, 0))
    quadtree.clear()
    quadtree.particles = particles
    quadtree.update()
    quadtree.draw()
    for particle in particles:
        particle.update()
        particle.draw()
    pygame.display.update()