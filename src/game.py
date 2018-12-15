import math
import random
import sys

import numpy as np
import pygame

from pgi import *
from spaceobj import SpaceObjectState

w = 512
h = 512

SPACESHIP_RADIUS = 20

COLOURS = ((0x66, 0x2d, 0x91), (0x2e, 0x31, 0x92), (0x00, 0x92, 0x45),
           (0x8c, 0xc6, 0x3f), (0x9e, 0x00, 0x5d), (0x88, 0xa8, 0x0d))


class Spaceship(SpaceObjectState):
    def __init__(self):
        super().__init__()
        self.last_x = 0
        self.last_y = 0

    def integrate(self):
        self.last_x = self.pos_x
        self.last_y = self.pos_y
        super().integrate()

    def draw(self, surface):
        aac(surface, [255, 255, 255], [self.pos_x, self.pos_y], self.radius)
        aac(surface, [192, 192, 255], [self.pos_x, self.pos_y], self.radius // 4 * 3)
        aac(surface, [255, 255, 255], [self.pos_x, self.pos_y], self.radius // 4 * 2)

        # fire
        font = pygame.font.SysFont("Comic Sans MS", 24)
        rendered = font.render("fire", True, (0xFD, 0x4E, 0x01))

        # angle
        angle = -math.degrees(math.atan((self.pos_x - self.last_x) / (self.pos_y / self.last_y)))
        rotated = pygame.transform.rotate(rendered, angle)

        rendered_rect = rotated.get_rect()
        rendered_rect.x = self.pos_x - self.radius
        rendered_rect.y = self.pos_y + self.radius
        screen.blit(rotated, rendered_rect)

    def past_top(self):
        return self.pos_y < 0


class Asteroid(SpaceObjectState):
    def __init__(self, li):
        super().__init__()
        self.radius = li[0]
        #self.colour = li[1]
        self.colour = random.choice(COLOURS)
        self.pos_x = li[2]
        self.pos_y = li[3]
        self.vel_x = random.choice((0.3, -0.3))
        self.vel_y = random.choice((0.3, -0.3))

    def draw(self, surface):
        aac(surface, self.colour, [self.pos_x, self.pos_y], self.radius)


pygame.init()
screen = pygame.display.set_mode([w, h])

clock = pygame.time.Clock()

spaceship = Spaceship()
spaceship.radius = SPACESHIP_RADIUS
spaceship.pos_x = w // 2
spaceship.pos_y = h - spaceship.radius * 2
spaceship.vel_y = 0

asteroids_data = [[15, [168, 39, 151], 307, 381], [10, [119, 224, 229], 471, 289], [15, [193, 153, 28], 143, 507],
                  [13, [184, 140, 39], 331, 238], [14, [241, 66, 166], 362, 500], [15, [216, 108, 50], 368, 112],
                  [14, [45, 123, 51], 245, 278], [15, [11, 137, 14], 217, 166], [11, [242, 123, 41], 217, 92],
                  [11, [122, 123, 59], 155, 269], [15, [191, 7, 169], 444, 34], [14, [87, 240, 8], 225, 406],
                  [15, [92, 217, 163], 490, 317], [13, [21, 252, 245], 346, 365], [10, [128, 230, 44], 44, 189],
                  [12, [214, 127, 149], 481, 136], [12, [205, 148, 66], 5, 449], [13, [20, 81, 101], 187, 509],
                  [11, [15, 142, 155], 91, 248], [14, [185, 103, 27], 33, 148]]
asteroids = [Asteroid(li) for li in asteroids_data]
game_objects = [spaceship, *asteroids]


def update_heat_map():
    heat_map = np.zeros(shape=(w, h), dtype=np.float_)
    surf2 = pygame.Surface((w, h))
    surf2arr = pygame.surfarray.pixels2d(surf2)
    as_len = len(asteroids)
    for i in range(as_len):
        for j in range(as_len):
            base = asteroids[i]
            target = asteroids[j]
            dist = math.sqrt((target.pos_x - base.pos_x) ** 2 + (target.pos_y - base.pos_y) ** 2)
            if dist > 72:
                continue
            r = max(dist, base.radius)
            surf2.fill([0, 0, 0])
            rr = round(r)
            pygame.draw.circle(surf2, [0, 0, 1], (rr, rr), rr)
            x1 = max(0, min(round(base.pos_x - r), w))
            x2 = max(0, min(round(base.pos_x + r), w))
            y1 = max(0, min(round(base.pos_y - r), h))
            y2 = max(0, min(round(base.pos_y + r), h))
            heat_map[x1:x2, y1:y2] += surf2arr[0:abs(x1 - x2), 0:abs(y1 - y2)] / r
    heat_map = np.round(heat_map / heat_map.max() * (1 << 8)) * (1 << 8)
    pygame.surfarray.blit_array(screen, heat_map)


win_font = pygame.font.SysFont("Comic Sans MS", 28)

show_hm = False
win = False

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
            elif event.key == pygame.K_h:
                show_hm = not show_hm
            elif win and event.key == pygame.K_r:
                win = False
                # restart
                spaceship.radius = SPACESHIP_RADIUS
                spaceship.pos_x = w // 2
                spaceship.pos_y = h - spaceship.radius * 2
                spaceship.vel_y = 0
                spaceship.vel_x = 0
                asteroids = [Asteroid(li) for li in asteroids_data]
                game_objects = [spaceship, *asteroids]
            elif event.key == pygame.K_q:
                sys.exit()
    screen.fill([0, 0, 0])
    for o in game_objects:
        o.integrate()
    if show_hm:
        update_heat_map()
    elif not win:
        for o in game_objects:
            o.draw(screen)
            if isinstance(o, Asteroid):
                if o.collide(spaceship):
                    print("COLLISION: ABORTING EXECUTION OF PROGRAM")
                    sys.exit()
                if o.oob(w, h):
                    o.pos_x = random.choice((0, w))
                    o.pos_y = random.randint(0, h)
                    if o.pos_x == 0:
                        o.vel_x = 0.3
                    else:
                        o.vel_x = -0.3

    if spaceship.past_top():
        win = True

    if win:
        win_text = win_font.render("You win!!! Press R to play again", True, (0, 255, 0))
        win_rect = win_text.get_rect()
        screen.blit(win_text, win_rect)

    pygame.display.flip()
    clock.tick(30)
