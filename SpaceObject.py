import math

frameRate = 30
G = 6.6*(10**(-11))

class SpaceObject:
    vel = [0.0, 0.0] #Velocity, first is magnitude, second is angle
    pos = [0.0, 0.0] #Position, first is x, second is y
    m = 0.0 #Mass
    r = 0.0 #Radius

    def __init__(self, vel, pos, m, r ):
        self.vel = vel
        self.pos = pos
        self.m = m
        self.r = r

    def gravForce(sO2):
        global G
        global frameRate
        distance = math.sqrt((pos[0]-sO2.pos[0])**2+(pos[1]-sO2.pos[1])**2) #Calcualte distance

        force = (G*m*s02.m)/(distance**2) #Calcualte magnitude of force

        #Calculate force
        if(pos[0]>sO2.pos[0]):
            if(pos[1]>sO2.pos[1]):
                vel[0] = (vel[0]-math.cos(math.atan((pos[1]-sO2.pos[1])/(pos[0]-sO2.pos[0])))*force)/frameRate
                vel[1] = (vel[1]-math.sin(math.atan((pos[1]-sO2.pos[1])/(pos[0]-sO2.pos[0])))*force)/frameRate
            else:
                vel[0] = (vel[0]-math.cos(math.atan((pos[1]-sO2.pos[1])/(pos[0]-sO2.pos[0])))*force)/frameRate
                vel[1] = (vel[1]+math.sin(math.atan((pos[1]-sO2.pos[1])/(pos[0]-sO2.pos[0])))*force)/frameRate
        else:
            if(pos[1]>sO2.pos[1]):
                vel[0] = (vel[0]+math.cos(math.atan((pos[1]-sO2.pos[1])/(pos[0]-sO2.pos[0])))*force)/frameRate
                vel[1] = (vel[1]-math.sin(math.atan((pos[1]-sO2.pos[1])/(pos[0]-sO2.pos[0])))*force)/frameRate
            else:
                vel[0] = (vel[0]+math.cos(math.atan((pos[1]-sO2.pos[1])/(pos[0]-sO2.pos[0])))*force)/frameRate
                vel[1] = (vel[1]+math.sin(math.atan((pos[1]-sO2.pos[1])/(pos[0]-sO2.pos[0])))*force)/frameRate
                

        
        

class SpaceShip(SpaceObject):
    z = float(0)
    




    
    
