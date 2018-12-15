import math
import os
import random
import sys
from random import randint

import numpy as np
import pygame
from SpaceObject import *
from pgi import *
from spaceobj import SpaceObjectState

w = 512
h = 512

SPACESHIP_RADIUS = 20

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
            mags.append(1 / dist ** 2)
            angles.append(math.degrees(math.atan2(object.pos_y - self.pos_y, object.pos_x - self.pos_x)))

        x = y = 0.
        for angle, weight in zip(angles, mags):
            x += math.cos(math.radians(angle)) * weight
            y += math.sin(math.radians(angle)) * weight

        angle = math.degrees(math.atan2(y, x))

        return angle

    def gravForce(self, sO2):
        global G
        global frameRate
        if (math.sqrt(abs(self.pos[0] - sO2.pos[0]) ** 2 + abs(self.pos[1] - sO2.pos[1]) ** 2) < 5):
            True
        else:

            distance = math.sqrt(
                (self.pos[0] - sO2.pos[0]) ** 2 + (self.pos[1] - sO2.pos[1]) ** 2)  # Calcualte distance
            force = (G * self.m * sO2.m) / (distance ** 2)  # Calcualte magnitude of force

            # Calculate force
            if (self.pos[0] > sO2.pos[0]):
                if (self.pos[1] > sO2.pos[1]):
                    self.vel[0] = (self.vel[0] - math.cos(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m)
                    self.vel[1] = (self.vel[1] - math.sin(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m)
                else:
                    self.vel[0] = (self.vel[0] - math.cos(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m)
                    self.vel[1] = (self.vel[1] + math.sin(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m)
            else:
                if (self.pos[1] > sO2.pos[1]):
                    self.vel[0] = (self.vel[0] + math.cos(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m)
                    self.vel[1] = (self.vel[1] - math.sin(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m)
                else:
                    self.vel[0] = (self.vel[0] + math.cos(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m)
                    self.vel[1] = (self.vel[1] + math.sin(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m)


asteroids1 = []

while True:
    print(
        "Input velocity x, velocity y, position x, position y, mass, and radius of the asteroid in that order. Enter a letter to quit.")
    try:
        a = float(input())
        b = float(input())
        c = float(input())
        d = float(input())
        e = float(input())
        f = float(input())
    except:
        break

    asteroids1.append(SpaceObject([a, b], [c, d], e, f))


def converter(p):
    return (p.pos[0], p.pos[1], p.vel[0], p.vel[1], 0, 0, p.r, p.m)


class Asteroid(SpaceObjectState):
    def __init__(self, li):
        super().__init__()
        self.radius = li[0]
        # self.colour = li[1]
        self.colour = random.choice(COLOURS)
        self.pos_x = li[2]
        self.pos_y = li[3]
        self.vel_x = random.choice((0.3, -0.3))
        self.vel_y = random.choice((0.3, -0.3))

    colour = [200, 200, 200]

    def gravForce(self, sO2):
        global G
        global frameRate
        if (math.sqrt(abs(self.pos[0] - sO2.pos[0]) ** 2 + abs(self.pos[1] - sO2.pos[1]) ** 2) < 5):
            True
        else:

            distance = math.sqrt(
                (self.pos[0] - sO2.pos[0]) ** 2 + (self.pos[1] - sO2.pos[1]) ** 2)  # Calcualte distance
            force = (G * self.m * sO2.m) / (distance ** 2)  # Calcualte magnitude of force

            # Calculate force
            if (self.pos[0] > sO2.pos[0]):
                if (self.pos[1] > sO2.pos[1]):
                    self.vel[0] = (self.vel[0] - math.cos(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m) * 100000
                    self.vel[1] = (self.vel[1] - math.sin(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m) * 100000
                else:
                    self.vel[0] = (self.vel[0] - math.cos(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m) * 100000
                    self.vel[1] = (self.vel[1] + math.sin(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m) * 100000
            else:
                if (self.pos[1] > sO2.pos[1]):
                    self.vel[0] = (self.vel[0] + math.cos(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m) * 100000
                    self.vel[1] = (self.vel[1] - math.sin(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m) * 100000
                else:
                    self.vel[0] = (self.vel[0] + math.cos(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m) * 100000
                    self.vel[1] = (self.vel[1] + math.sin(math.atan(
                        (self.pos[1] - sO2.pos[1]) / (self.pos[0] - sO2.pos[0]))) * force / frameRate / self.m) * 100000

    def draw(self, surface):
        aac(surface, self.colour, [self.pos_x, self.pos_y], self.radius)


pygame.init()
screen = pygame.display.set_mode([w, h])

spaceship = Spaceship()
spaceship.radius = SPACESHIP_RADIUS
spaceship.pos_x = w // 2 + 30
spaceship.pos_y = h // 3
spaceship.vel_y = -0

asteroids_data = [
    [randint(10, 25), [randint(0, 255), randint(0, 255), randint(0, 255)], randint(0, 512), randint(0, 512)]
    for _ in
    range(15)]
asteroids = [Asteroid(li) for li in asteroids_data]
game_objects = [spaceship, *asteroids]
heat_map = np.zeros(shape=(w, h), dtype=np.float_)
show_hm = True
control = True
surf2 = pygame.Surface((w, h))
surf2arr = pygame.surfarray.pixels2d(surf2)


def retrieve_block(hm, x, y, mul):
    return hm[int(x * mul), int(y * mul)]


win = False
win_font = pygame.font.SysFont("Comic Sans MS", 28)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if control:
                    spaceship.vel_y -= 1
            elif event.key == pygame.K_s:
                if control:
                    spaceship.vel_y += 1
            elif event.key == pygame.K_a:
                if control:
                    spaceship.vel_x -= 1
            elif event.key == pygame.K_d:
                if control:
                    spaceship.vel_x += 1
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
            elif event.key == pygame.K_p:
                control = not control
            elif event.key == pygame.K_q:
                sys.exit()
    screen.fill([0, 0, 0])
    if show_hm:
        heat_map = np.zeros((w, h))
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
        heat_map = heat_map / heat_map.max()
        pygame.surfarray.blit_array(screen, np.round(heat_map * (1 << 8)) * (1 << 16))
        for i in range(w // 16):
            for j in range(h // 16):
                heat_map[i * 16:i * 16 + 16, j * 16:j * 16 + 16] = np.mean(
                    heat_map[i * 16:i * 16 + 16, j * 16:j * 16 + 16])
        # block_x = spaceship.pos_x % 16
        # block_y = spaceship.pos_y % 16
        # for i in range(16):
        #     mx = min(
        #         (retrieve_block(heat_map, block_x - 1, block_y - 1, 16), -1, -1),
        #         (retrieve_block(heat_map, block_x - 1, block_y, 16), -1, 0),
        #         (retrieve_block(heat_map, block_x - 1, block_y + 1, 16), -1, +1),
        #         (retrieve_block(heat_map, block_x, block_y + 1, 16), 0, +1),
        #         (retrieve_block(heat_map, block_x + 1, block_y + 1, 16), +1, +1),
        #         (retrieve_block(heat_map, block_x + 1, block_y, 16), +1, 0),
        #         (retrieve_block(heat_map, block_x + 1, block_y - 1, 16), +1, -1),
        #         (retrieve_block(heat_map, block_x, block_y - 1, 16), 0, -1),
        #         key=lambda x: x[0])
        #     block_x += mx[1]
        #     block_y += mx[2]
        #     pygame.draw.rect(screen, [255,255,255], [block_x * 16, block_y * 16, 16, 16])
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
        pygame.draw.aaline(screen, [0, 0, 0], (spaceship.pos_x, spaceship.pos_y),
                           (spaceship.pos_x + math.cos(math.radians(min_deg)) * 150,
                            spaceship.pos_y + math.sin(math.radians(min_deg)) * 150))

        if not control:
            angle = spaceship.avoid_objects(*asteroids)
            spaceship.vel_x = -math.cos(math.radians(angle))
            spaceship.vel_y = -math.sin(math.radians(angle))

    for o in game_objects:
        o.integrate()
        o.draw(screen)
        if isinstance(o, Asteroid):
            # if o.collide(spaceship):
            #     print("COLLISION: ABORTING EXECUTION OF PROGRAM")
            #     sys.exit()
            if o.oob(w, h):
                o.pos_x = random.choice((0, w))
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
