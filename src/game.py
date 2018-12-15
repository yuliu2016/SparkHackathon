import random
import sys

import pygame

from src.pgi import *
from src.spaceobj import SpaceObjectState

w = 512
h = 512


class Spaceship(SpaceObjectState):
    def draw(self, surface):
        aac(surface, [255, 255, 255], [self.pos_x, self.pos_y], self.radius)
        aac(surface, [192, 192, 255], [self.pos_x, self.pos_y], self.radius // 4 * 3)
        aac(surface, [255, 255, 255], [self.pos_x, self.pos_y], self.radius // 4 * 2)


class RandomObject(SpaceObjectState):
    def __init__(self):
        super().__init__()
        self.radius = random.randint(10, 30)
        self.colour = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        self.pos_x = random.randint(0, w)
        self.pos_y = random.randint(0, h)

    def draw(self, surface):
        aac(surface, self.colour, [self.pos_x, self.pos_y], self.radius)


pygame.init()
screen = pygame.display.set_mode([w, h])

clock = pygame.time.Clock()

spaceship = Spaceship()
spaceship.radius = 20
spaceship.pos_x = w // 2
spaceship.pos_y = h - spaceship.radius * 2
spaceship.vel_y = -0.1

random_objects = [RandomObject() for _ in range(20)]
game_objects = [spaceship, *random_objects]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    screen.fill([0, 0, 0])
    for o in game_objects:
        o.integrate()
        o.draw(screen)
    pygame.display.flip()
    clock.tick(24)
