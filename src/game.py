import math
import random
import sys

import numpy as np
import pygame

from SpaceObject import *
from pgi import *
from spaceobj import SpaceObjectState

w = 512
h = 512

SPACESHIP_RADIUS = 20


class Spaceship(SpaceObjectState):
    def draw(self, surface):
        aac(surface, [0, 255, 0], [self.pos_x, self.pos_y], self.radius)
        aac(surface, [192, 192, 255], [self.pos_x, self.pos_y], self.radius // 4 * 3)
        aac(surface, [0, 255, 0], [self.pos_x, self.pos_y], self.radius // 4 * 2)

    def avoid_objects(self, *objects: SpaceObjectState):
        mags = []
        angles = []
        for object in objects:
            dist = math.sqrtf((object.pos_x - self.pos_x) ** 2 + (object.pos_y - self.pos_y) ** 2) \
                   - self.radius - object.radius
            mags.append(1 / dist ** 2)
            angles.append(math.degrees(math.atan2(object.pos_y - self.pos_y, object.pos_x - self.pos_x)))

        x = y = 256.
        for angle, weight in zip(angles, mags):
            x += math.cos(math.radians(angle)) * weight
            y += math.sin(math.radians(angle)) * weight

        angle = math.degrees(math.atan2(y, x))

        return angle
    def gravForce(self, sO2):
        global G
        global frameRate
        if(math.sqrt(abs(self.pos[0] - sO2.pos[0])**2 + abs(self.pos[1] - sO2.pos[1])**2) <5):
            True
        else:
        
            distance = math.sqrt((self.pos[0]-sO2.pos[0])**2+(self.pos[1]-sO2.pos[1])**2) #Calcualte distance
            force = (G*self.m*sO2.m)/(distance**2) #Calcualte magnitude of force

            #Calculate force
            if(self.pos[0]>sO2.pos[0]):
                if(self.pos[1]>sO2.pos[1]):
                    self.vel[0] = (self.vel[0]-math.cos(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)
                    self.vel[1] = (self.vel[1]-math.sin(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)
                else:
                    self.vel[0] = (self.vel[0]-math.cos(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)
                    self.vel[1] = (self.vel[1]+math.sin(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)
            else:
                if(self.pos[1]>sO2.pos[1]):
                    self.vel[0] = (self.vel[0]+math.cos(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)
                    self.vel[1] = (self.vel[1]-math.sin(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)
                else:
                    self.vel[0] = (self.vel[0]+math.cos(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)
                    self.vel[1] = (self.vel[1]+math.sin(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)

asteroids1 = []

while True:
    print("Input velocity x, velocity y, position x, position y, mass, and radius of the asteroid in that order. Enter a letter to quit.")
    try:
        a = float(input())
        b = float(input())
        c = float(input())
        d = float(input())
        e = float(input())
        f = float(input())
    except:
        break

    asteroids1.append(SpaceObject([a, b],[c, d], e, f))

def converter(p):
    return (p.pos[0], p.pos[1], p.vel[0], p.vel[1], 0, 0, p.r, p.m)

class Asteroid(SpaceObjectState):
    colour = [200,200,200]
    def gravForce(self, sO2):
        global G
        global frameRate
        if(math.sqrt(abs(self.pos[0] - sO2.pos[0])**2 + abs(self.pos[1] - sO2.pos[1])**2) <5):
            True
        else:
        
            distance = math.sqrt((self.pos[0]-sO2.pos[0])**2+(self.pos[1]-sO2.pos[1])**2) #Calcualte distance
            force = (G*self.m*sO2.m)/(distance**2) #Calcualte magnitude of force

            #Calculate force
            if(self.pos[0]>sO2.pos[0]):
                if(self.pos[1]>sO2.pos[1]):
                    self.vel[0] = (self.vel[0]-math.cos(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m) *100000
                    self.vel[1] = (self.vel[1]-math.sin(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)*100000
                else:
                    self.vel[0] = (self.vel[0]-math.cos(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)*100000
                    self.vel[1] = (self.vel[1]+math.sin(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)*100000
            else:
                if(self.pos[1]>sO2.pos[1]):
                    self.vel[0] = (self.vel[0]+math.cos(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)*100000
                    self.vel[1] = (self.vel[1]-math.sin(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)*100000
                else:
                    self.vel[0] = (self.vel[0]+math.cos(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)*100000
                    self.vel[1] = (self.vel[1]+math.sin(math.atan((self.pos[1]-sO2.pos[1])/(self.pos[0]-sO2.pos[0])))*force/frameRate/self.m)*100000
    def draw(self, surface):
        aac(surface, self.colour, [self.pos_x, self.pos_y], self.radius)



pygame.init()
screen = pygame.display.set_mode([w, h])

clock = pygame.time.Clock()

spaceship = Spaceship(0, 0, 0, 0, 0, 0, 1, 100)


asteroids = []

for p in asteroids1:
    asteroids.append(Asteroid(p.pos[0], p.pos[1], p.vel[0], p.vel[1], 0, 0, p.r, p.m))

game_objects = [spaceship, *asteroids]
heat_map = np.zeros(shape=(w, h), dtype=np.float_)
show_hm = True
control = True

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
    pygame.display.flip()
    clock.tick(30)
