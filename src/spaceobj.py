import math


class SpaceObjectState:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.vel_x = 0
        self.vel_y = 0
        self.acc_x = 0
        self.acc_y = 0
        self.radius = 0
        self.mass = 0

        self.max_acc = .1

    def integrate(self):
        self.vel_x += self.acc_x
        self.vel_y += self.acc_y
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

    def heading(self):
        return math.atan(self.vel_y / self.vel_x) - 2 * math.pi

    def mag_vel(self):
        return math.sqrt(self.vel_x ** 2 + self.vel_y ** 2)

    def mag_acc(self):
        return math.sqrt(self.acc_x ** 2 + self.acc_y ** 2)

    def draw(self, surface):
        pass

    def collide(self, spaceobj):
        x_distance = abs(spaceobj.pos_x - self.pos_x)
        y_distance = abs(spaceobj.pos_y - self.pos_y)
        distance = math.sqrt(x_distance**2 + y_distance**2)
        min_distance = self.radius + spaceobj.radius
        return distance <= min_distance

    def oob(self, width, height):
        return self.pos_x < 0 or self.pos_x > width or \
               self.pos_y < 0 or self.pos_y > height
