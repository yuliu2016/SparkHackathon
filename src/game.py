import random
import sys
import math
from typing import Tuple

import pygame

from pgi import *
from spaceobj import SpaceObjectState

w = 512
h = 512

SPACESHIP_RADIUS = 20


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
        self.pos_y = random.randint(0, h - (SPACESHIP_RADIUS * 2 + 50))
        self.vel_x = random.choice((0.3, -0.3))
        self.vel_y = random.choice((0.3, -0.3))

    def draw(self, surface):
        aac(surface, self.colour, [self.pos_x, self.pos_y], self.radius)

    def collide(self, spaceship):
        x_distance = abs(spaceship.pos_x - self.pos_x)
        y_distance = abs(spaceship.pos_y - self.pos_y)
        distance = math.sqrt(x_distance**2 + y_distance**2)
        min_distance = self.radius + spaceship.radius
        return distance <= min_distance


pygame.init()
screen = pygame.display.set_mode([w, h])

clock = pygame.time.Clock()

spaceship = Spaceship()
spaceship.radius = SPACESHIP_RADIUS
spaceship.pos_x = w // 2
spaceship.pos_y = h - spaceship.radius * 2
spaceship.vel_y = -0.1

random_objects = [RandomObject() for _ in range(20)]
game_objects = [spaceship, *random_objects]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                spaceship.vel_y -= 0.1
            elif event.key == pygame.K_s:
                spaceship.vel_y += 0.1
            elif event.key == pygame.K_a:
                spaceship.vel_x -= 0.1
            elif event.key == pygame.K_d:
                spaceship.vel_x += 0.1
            elif event.key == pygame.K_q:
                sys.exit()
    screen.fill([0, 0, 0])
    for o in game_objects:
        o.integrate()
        o.draw(screen)
        if isinstance(o, RandomObject) and o.collide(spaceship):
            print("COLLISION: ABORTING EXECUTION OF PROGRAM")
            sys.exit()
    pygame.display.flip()
    clock.tick(30)
