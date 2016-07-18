import numpy as np
import math
import quaternions as q

class Flyer(object):
    def __init__(self, x, y, z, mass):
        self.x = x
        self.y = y
        self.z = z
        self.mass = mass

    def get2D(self): 
        #idk how to do this for arbitrary camera angles but 
        #i could probably just fool around with scalars on the y
        #component (assuming i can only rotate along pitch)
        x = self.y - self.x
        y = self.z - self.y - self.x
        return (x, y)


class Eagle(SpaceshipComponent):
    def __init__(self, x, y, z, mass, fuel):
        super().__init__(x, y, z, 15, 15, 11, metalMass, fuel)

    def draw(self, canvas):
        #TODO
        pass

class Columbia(SpaceshipComponent):
    def __init__(self, x, y, z, mass, fuel):
        super().__init__(x, y, z, 15, 15, 35, metalMass, fuel)

    def draw(self, canvas):
        #TODO
        pass

class SIC(SpaceshipComponent):
    def __init__(self, x, y, z, xDiam, yDiam, zDiam, mass, fuel):
        super().__init__(x, y, z, xDiam, yDiam, zDiam, mass, fuel)

    def draw(self, canvas):
        #TODO
        pass

#TODO: add SII and SIVB classes. also figure out whether i should

class SaturnV(object):
    def __init__(self, x, y, z):
        self.stage1 = SIC(x, y, z, 50, 50, 110, 200, 1000)
        self.stage2 = SII(x, y, z, 25, 25, 50, 100, 400)
        self.stage3 = SIVB(x, y, z, 20, 20, 30, 100, 600)
        #TODO: SaturnV separated into 3 stages.


class SpaceshipComponent(Flyer):
    def __init__(self, x, y, z, xDiam, yDiam, zDiam, mass, fuel):
        super().__init__(x, y, z, mass + fuel)
        self.fuel = fuel
        #if you pretend it's an ellipse, the xDiam is the diameter along
        #ITS x axis, not the global x axis
        self.xDiam = xDiam 
        self.yDiam = yDiam
        self.zDiam = zDiam

    def steer(self, force): #force is a force 3-vector of variable magnitude
        self.fuel -= np.linalg.norm(force) #idk how this works tbh. TODO
        #               ^ vector magnitude

        #so I'm burning fuel, which produces a force in one direction
        #and there's an equal and opposite force in the direction I want to go in
        #which is the force vector of my input

        #i don't see why fuel burned would be anything but linearly correlated
        #with force applied to the craft
        pass

class Astronaut(Flyer):
    def __init__(self, x, y, z, mass, name):
        super().__init__(x, y, z, mass)
        self.health = 100
        self.name = name

class Spaceship(object):
    def __init__(self, x, y, z):
        #gotta fix the initial coordinates
        self.Eagle = Eagle(x, y, z, 100, 1500) #magic numbers. I should get these from wikipedia
        self.Columbia = Columbia(x, y, z, 500, 10000) #magic numbers
        self.Armstrong = Astronaut(x, y, z, 160, "Armstrong") 
        self.Buzz = Astronaut(x, y, z, 160, "Buzz")
        self.Collins = Astronaut(x, y, z, 160, "Collins")
        self.stage = 0 #stage of separation I guess


def collide(Flyer A, Flyer B):
    #conservation of energy and of momentum
    #rotations? how the fuck do I do that?
    pass

