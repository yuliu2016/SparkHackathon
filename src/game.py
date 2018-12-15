import math
import sys

import numpy as np
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


class Asteroid(SpaceObjectState):
    def __init__(self, li):
        super().__init__()
        self.radius = li[0]
        self.colour = li[1]
        self.pos_x = li[2]
        self.pos_y = li[3]

    def draw(self, surface):
        aac(surface, self.colour, [self.pos_x, self.pos_y], self.radius)

pygame.init()
screen = pygame.display.set_mode([w, h])

clock = pygame.time.Clock()

spaceship = Spaceship()
spaceship.radius = 20
spaceship.pos_x = w // 2
spaceship.pos_y = h - spaceship.radius * 2
spaceship.vel_y = -0


asteroids_data = [[15, [168, 39, 151], 307, 381], [10, [119, 224, 229], 471, 289], [15, [193, 153, 28], 143, 507],
                  [13, [184, 140, 39], 331, 238], [14, [241, 66, 166], 362, 500], [15, [216, 108, 50], 368, 112],
                  [14, [45, 123, 51], 245, 278], [15, [11, 137, 14], 217, 166], [11, [242, 123, 41], 217, 92],
                  [11, [122, 123, 59], 155, 269], [15, [191, 7, 169], 444, 34], [14, [87, 240, 8], 225, 406],
                  [15, [92, 217, 163], 490, 317], [13, [21, 252, 245], 346, 365], [10, [128, 230, 44], 44, 189],
                  [12, [214, 127, 149], 481, 136], [12, [205, 148, 66], 5, 449], [13, [20, 81, 101], 187, 509],
                  [11, [15, 142, 155], 91, 248], [14, [185, 103, 27], 33, 148]]
asteroids = [Asteroid(li) for li in asteroids_data]
game_objects = [spaceship, *asteroids]

heat_map = np.zeros(shape=(w, h), dtype=np.float_)


for i in range(w):
    for j in range(h):
        s = 0
        for asteroid in asteroids:
            k = math.sqrt((i - asteroid.pos_x) ** 2 + (j - asteroid.pos_y) ** 2)
            if k:
                s += 1 / k ** 2
        heat_map[i, j] = s

heat_map = heat_map / heat_map.max() * (1 << 24)

show_hm = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                show_hm = not show_hm
    screen.fill([0, 0, 0])
    for o in game_objects:
        o.integrate()
    if show_hm:
        pygame.surfarray.blit_array(screen, heat_map)
    else:
        for o in game_objects:
            o.draw(screen)
    pygame.display.flip()
    clock.tick(24)
