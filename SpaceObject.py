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

        #Calculate direciton
        if(pos[0]>sO2.pos[0]):
            if(pos[1]>sO2.pos[1]):
                direction1 = math.atan((pos[1]-sO2.pos[1])/(pos[0]-sO2.pos[0]))
            else:
                direction1 = 2*math.pi-math.atan((sO2.pos[1]-pos[1])/(pos[0]-sO2.pos[0]))
        else:
            if(pos[1]>sO2.pos[1]):
                direction1 = math.pi/2+math.atan((pos[1]-sO2.pos[1])/(sO2.pos[0]-pos[0]))
            else:
                direction1 = math.pi+math.atan((sO2.pos[1]-pos[1])/(sO2.pos[0]-pos[0]))
                
        if direction1>math.pi:
            direciton2 = direction1-math.pi
        else:
            direction2 = direction1+pi
        

class SpaceShip(SpaceObject):
    z = float(0)
    




    
    
