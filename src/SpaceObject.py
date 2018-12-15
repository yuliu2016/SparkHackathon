import math

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
