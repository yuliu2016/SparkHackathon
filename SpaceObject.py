import math
import pygame
import time

frameRate = 30
G = 6.6*(10**(-11))

w = 512
h = 512

pygame.init()
screen = pygame.display.set_mode([w, h])

clock = pygame.time.Clock()

class SpaceObject:
    vel = [0.0, 0.0] #Velocity, first is x, second is y
    pos = [0.0, 0.0] #position, first is x, second is y
    m = 0.0 #Mass
    r = 0.0 #Radius

    def __init__(self, vel, pos, m, r ):
        self.vel = vel
        self.pos = pos
        self.m = m
        self.r = r

    #def collision

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


    #Updates displacement
    def displacement(self):
        self.pos[0] = self.pos[0]+self.vel[0]/frameRate
        self.pos[1] = self.pos[1]+self.vel[1]/frameRate
        
#Class for spaceship
class SpaceShip(SpaceObject):
    direct = 0
    a = True

    def __init__(self, vel, pos, m, r, direct, a):
        self.vel = vel
        self.pos = pos
        self.m = m
        self.r = r
        self.direct = direct
        self.a = True

kg = float(input("Enter the mass in kg of the spaceship"))
m = float(input("Enter the radius in meters of the spaceship"))

class SpaceSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        img = pygame.image.load('/Users/victorma/Downloads/ship.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.x / 2, self.rect.y / 2)
        self.rect.x = x
        self.rect.y = y

    def control(self, x, y):
        self.movex+=x
        self.movey+=y

    
    def update (self, angle):
        self.image = pygame.transform.rotate(img, angle)
        self.rectx += self.movex
        self.recty += self.movey


ship = SpaceShip([0,0], [0,0], kg, m, 0, False)
sprite = SpaceSprite (0, 0)
aD = []

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

    aD.append(SpaceObject([a, b],[c, d], e, f))


        
        
while True:
    for asteroid in aD:
        asteroid.displacement()
        for asteroid2 in aD:
            asteroid.gravForce(asteroid2)
            
    ship.displacement()
    for asteroid in aD:
        ship.gravForce(asteroid)

    print(ship.pos)
    time.sleep(1/frameRate)
    pygame.display.flip()

