import math
import pygame
import time

frameRate = 30
G = 6.6*(10**(-11))

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

    #def collosion

    def gravForce(self, sO2):
        global G
        global frameRate
        if(math.abs(self.pos[0] - sO2.pos[0])<0.1 and math.abs(self.pos[1] - sO2.pos[1])<0.1):
            break
    
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

        print(self.vel)

    #Updates displacement
    def displacement(self):
        self.pos[0] = self.pos[0]+self.vel[0]/frameRate
        self.pos[1] = self.pos[1]+self.vel[1]/frameRate
        print(self.pos)
        
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


ship = SpaceShip([0,0], [0,0], kg, m, 0, False)
aD = []

while True:
    print("Input velocity x, velocity y, position x, position y, mass, and radius of the astroid in that order. Enter a letter to quit.")
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
    for astroid in aD:
        astroid.displacement()
        for atroid2 in aD:
            astroid.gravForce(astroid2)
            
    ship.displacement()
    for astroid in aD:
        ship.gravForce(astroid)

    print(ship.pos)
    time.sleep(1/frameRate)

