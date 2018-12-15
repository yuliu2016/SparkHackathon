import math
import random
import sys
import os

import numpy as np
import pygame

from src.pgi import *
from src.spaceobj import SpaceObjectState

w = 512
h = 512

SPACESHIP_RADIUS = 20
ASTEROID_SPEED = .5

COLOURS = ((0x66, 0x2d, 0x91), (0x2e, 0x31, 0x92), (0x00, 0x92, 0x45),
           (0x8c, 0xc6, 0x3f), (0x9e, 0x00, 0x5d), (0x88, 0xa8, 0x0d))
RES = "res"


class Spaceship(SpaceObjectState):
    spaceship_img = pygame.image.load(os.path.join(RES, "spaceship.png"))
    fire_imgs = (
        pygame.image.load(os.path.join(RES, "fire1.png")),
        pygame.image.load(os.path.join(RES, "fire2.png")),
        pygame.image.load(os.path.join(RES, "fire3.png")),
        pygame.image.load(os.path.join(RES, "fire4.png")),
    )

    def __init__(self):
        super().__init__()
        self.last_x = 0
        self.last_y = 0

    def integrate(self):
        self.last_x = self.pos_x
        self.last_y = self.pos_y
        super().integrate()

    def draw(self, surface):
        aac(surface, [54, 54, 54], [self.pos_x, self.pos_y], self.radius)
        # aac(surface, [192, 192, 255], [self.pos_x, self.pos_y], self.radius // 4 * 3)
        # aac(surface, [255, 255, 255], [self.pos_x, self.pos_y], self.radius // 4 * 2)

        # fire
        # font = pygame.font.SysFont("Comic Sans MS", 24)
        # rendered = font.render("fire", True, (0xFD, 0x4E, 0x01))
        fire_img = random.choice(self.fire_imgs)

        # anglea
        angle = math.atan((self.pos_x - self.last_x) / (self.pos_y / self.last_y))
        pygame_angle = -math.degrees(angle)
        rotated_fire = pygame.transform.rotate(fire_img, pygame_angle)
        rotated_img = pygame.transform.rotate(self.spaceship_img, pygame_angle)

        new_x = self.pos_x - math.sin(angle) * self.radius
        new_y = self.pos_y + math.cos(angle) * self.radius
        rendered_rect = rotated_fire.get_rect(center=(new_x, new_y))
        # rendered_rect.x = self.pos_x - self.radius
        spaceship_rect = rotated_img.get_rect(center=(self.pos_x, self.pos_y))
        screen.blit(rotated_img, spaceship_rect)
        screen.blit(rotated_fire, rendered_rect)

    def past_top(self):
        return self.pos_y < 0

    def avoid_objects(self, *objects: SpaceObjectState):
        mags = []
        angles = []
        for object in objects:
            dist = math.sqrt((object.pos_x - self.pos_x) ** 2 + (object.pos_y - self.pos_y) ** 2) \
                   - self.radius - object.radius
            mags.append(2 / dist ** 4)
            angles.append(math.degrees(math.atan2(object.pos_y - self.pos_y, object.pos_x - self.pos_x)))

        x = y = 0.
        for angle, weight in zip(angles, mags):
            x += math.cos(math.radians(angle)) * weight
            y += math.sin(math.radians(angle)) * weight

        angle = math.degrees(math.atan2(y, x))

        return angle

    def avoid_sides(self):
        dist = w / 2 - abs(self.pos_x - w / 2)
        return 2 * math.copysign(1, self.pos_x - w / 2) / dist ** 4

    def avoid_bottom(self):
        dist = h - self.pos_y
        return 1 / dist

    def oob(self, width, height):
        return self.pos_x+self.radius < 0 or self.pos_x-self.radius > width or \
               self.pos_y-self.radius > height

class Asteroid(SpaceObjectState):
    def __init__(self, li):
        super().__init__()
        self.radius = li[0]
        # self.colour = li[1]
        self.colour = random.choice(COLOURS)
        self.pos_x = li[2]
        self.pos_y = li[3]
        self.vel_x = random.choice((ASTEROID_SPEED, -ASTEROID_SPEED))
        self.vel_y = random.choice((ASTEROID_SPEED, -ASTEROID_SPEED))

    def draw(self, surface):
        aac(surface, self.colour, [self.pos_x, self.pos_y], self.radius)


pygame.init()
screen = pygame.display.set_mode([w, h])

clock = pygame.time.Clock()

spaceship = Spaceship()
spaceship.radius = SPACESHIP_RADIUS
spaceship.pos_x = w // 2 + 30
spaceship.pos_y = h - SPACESHIP_RADIUS * 4
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
show_hm = True
control = True
win = False
win_font=pygame.font.SysFont("Comic Sans MS",28)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if control:
                    spaceship.vel_y -= 0.1
            elif event.key == pygame.K_s:
                if control:
                    spaceship.vel_y += 0.1
            elif event.key == pygame.K_a:
                if control:
                    spaceship.vel_x -= 0.1
            elif event.key == pygame.K_d:
                if control:
                    spaceship.vel_x += 0.1
            elif event.key == pygame.K_h:
                show_hm = not show_hm
            elif event.key == pygame.K_r:
                win = False
                # restart
                spaceship.radius = SPACESHIP_RADIUS
                spaceship.pos_x = w // 2
                spaceship.pos_y = h - spaceship.radius * 2
                spaceship.vel_y = 0
                spaceship.vel_x = 0
                asteroids = [Asteroid(li) for li in asteroids_data]
                game_objects = [spaceship, *asteroids]
            elif event.key == pygame.K_p:
                control = not control
            elif event.key == pygame.K_q:
                sys.exit()
    screen.fill([0, 0, 0])
    if show_hm:
        surf2 = pygame.Surface((w, h))
        surf2arr = pygame.surfarray.pixels2d(surf2)
        as_len = len(asteroids)
        for i in range(as_len):
            for j in range(as_len):
                base = asteroids[i]
                target = asteroids[j]
                dist = math.sqrt((target.pos_x - base.pos_x) ** 2 + (target.pos_y - base.pos_y) ** 2)
                if dist > 128:
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
        """
        heat_map = heat_map / heat_map.max()
        pygame.surfarray.blit_array(screen, np.round(heat_map * (1 << 8)) * (1 << 16))
        spaceship_vel = max(spaceship.mag_vel(), 150)
        min_deg = 0
        min_risk = 10000
        for i in range(24):
            deg = i * 15
            x = spaceship.pos_x + math.cos(math.radians(deg)) * spaceship_vel
            y = spaceship.pos_y + math.sin(math.radians(deg)) * spaceship_vel
            px = heat_map[max(0, min(round(x), w)), max(0, min(round(y), h))]
            if px < min_risk:
                min_risk = px
                min_deg = deg
        # spaceship.acc_x = math.cos(math.radians(min_deg)) * 0.01
        # spaceship.acc_y = math.sin(math.radians(min_deg)) * 0.01
        pygame.draw.aaline(screen, [0, 255, 0], (spaceship.pos_x, spaceship.pos_y),
                           (spaceship.pos_x + math.cos(math.radians(min_deg)) * 150,
                            spaceship.pos_y + math.sin(math.radians(min_deg)) * 150))
        """
    if not control:
        angle = spaceship.avoid_objects(*asteroids)

        spaceship.vel_x += -(math.cos(math.radians(angle)))
        spaceship.vel_y += -(math.sin(math.radians(angle)))

        spaceship.vel_x += -spaceship.avoid_sides() * 10
        spaceship.vel_y += -spaceship.avoid_bottom() * 10

    for o in game_objects:
        o.integrate()
        o.draw(screen)
        if isinstance(o, Asteroid):
            if o.collide(spaceship):
                print("COLLISION: ABORTING EXECUTION OF PROGRAM")
                sys.exit()
            if o.oob(w, h):
                o.pos_x = random.choice((0, w))
                if o.pos_x == 0:
                    o.vel_x = ASTEROID_SPEED
                else:
                    o.vel_x = -ASTEROID_SPEED
    else:
        for o in game_objects:
            o.draw(screen)
            if isinstance(o, Asteroid):
                if o.collide(spaceship):
                    print("COLLISION: ABORTING EXECUTION OF PROGRAM")
                    sys.exit()
                if o.oob(w, h):
                    o.pos_x = random.choice((0, w))
                    if o.pos_x == 0:
                        o.vel_x = ASTEROID_SPEED
                    else:
                        o.vel_x = -ASTEROID_SPEED
                    o.vel_x = -0.3
    if spaceship.past_top():
        win = True

    if win:
        win_text = win_font.render("You win!!! Press R to play again", True, (0, 255, 0))
        win_rect = win_text.get_rect()
        screen.blit(win_text, win_rect)

    if spaceship.oob(w,h):
        win_text = win_font.render("Press R to play again", True, (0, 255, 0))
        win_rect = win_text.get_rect()
        screen.blit(win_text, win_rect)
        win=True

    pygame.display.flip()
    clock.tick(30)
