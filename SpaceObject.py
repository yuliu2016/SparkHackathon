import math

class spaceObject:
    vel = [0.0, 0.0] #Velocity, first is magnitude, second is angle
    pos = [0.0, 0.0] #Position, first is x, second is y
    m = 0.0 #Mass

    def __init__(self, vel, pos, m):
        self.vel = vel
        self.pos = pos
        self.m = m
    
    

class spaceShip(spaceObject):
    z = float(0)
    

def gravForce(spaceObject1, spaceObject2):
    distance = math.sqrt((spaceObject1.pos[0]-spaceObject2.pos[0])**2+(spaceObject1.pos[1]-spaceObject2.pos[1])**2) #Calcualte distance
    
p1 = spaceObject([5,5], [5,5], 5)
p2 = spaceObject([4,4], [4,4], 4)

