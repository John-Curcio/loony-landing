import numpy as np
import math
import quaternions as q

class Flyer(object):
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass


class Eagle(SpaceshipComponent):
    def __init__(self, x, y, mass, fuel):
        super().__init__(x, y, 15, 15, 11, metalMass, fuel)

    def draw(self, canvas):
        #TODO
        pass

class Columbia(SpaceshipComponent):
    def __init__(self, x, y, mass, fuel):
        super().__init__(x, y, 15, 15, 35, metalMass, fuel)

    def draw(self, canvas):
        #TODO
        pass

class SIC(SpaceshipComponent):
    def __init__(self, x, y, xDiam, yDiam, mass, fuel):
        super().__init__(x, y, xDiam, yDiam, mass, fuel)

    def draw(self, canvas):
        #TODO
        pass

#TODO: add SII and SIVB classes. also figure out whether i should

class SaturnV(object):
    def __init__(self, x, y):
        self.stage1 = SIC(x, y, 50, 110, 200, 1000)
        self.stage2 = SII(x, y, 25, 50, 100, 400)
        self.stage3 = SIVB(x, y, 20, 30, 100, 600)
        #TODO: SaturnV separated into 3 stages.


class SpaceshipComponent(Flyer):
    def __init__(self, x, y, xDiam, yDiam, mass, fuel):
        super().__init__(x, y, mass + fuel)
        self.fuel = fuel
        #if you pretend it's an ellipse, the xDiam is the diameter along
        #ITS x axis, not the global x axis
        self.xDiam = xDiam 
        self.yDiam = yDiam

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
    def __init__(self, x, y, mass, name):
        super().__init__(x, y, mass)
        self.health = 100
        self.name = name

class Spaceship(object):
    def __init__(self, x, y):
        #gotta fix the initial coordinates
        self.Eagle = Eagle(x, y, 100, 1500) #magic numbers. I should get these from wikipedia
        self.Columbia = Columbia(x, y, 500, 10000) #magic numbers
        self.Armstrong = Astronaut(x, y, 160, "Armstrong") 
        self.Buzz = Astronaut(x, y, 160, "Buzz")
        self.Collins = Astronaut(x, y, 160, "Collins")
        self.stage = 0 #stage of separation I guess


def collide(Flyer A, Flyer B):
    #conservation of energy and of momentum
    #rotations? how the fuck do I do that?
    pass

