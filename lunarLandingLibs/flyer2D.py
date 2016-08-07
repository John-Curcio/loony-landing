import numpy as np 
import pygame
import math

import os
if os.getcwd() == 'C:\\Users\\Nardo\\Documents\\GitHub\\loony-landing\\lunarLandingLibs':
    import vectorAlgebra as va
else:
    import lunarLandingLibs.vectorAlgebra as va 
    #I FUCKING HATE THIS SO MUCH.


class Edge(object):
    def __init__(self, a, b):
        # V TODO: can't rely on slope anymore i guess? maybe store slope as tuple (numerator, denominator). save some precision too!
        if a[0] == b[0]: self.slope = 0 
        else: self.slope = (a[1] - b[1]) / (a[0] - b[0]) 
        self.xIntercept = b[1] - self.slope * b[0]
        self.endpoints = [a, b]

    def draw(self, background):
        #pygame.draw.polygon(background, color, pointlist, line_thickness(optional)) 
        getUsableEndpoint = lambda a: (round(a[0]), round(a[1]))
        pygame.draw.line(background, (255, 0, 0), getUsableEndpoint(self.endpoints[0]), getUsableEndpoint(self.endpoints[1]), 3)

class Flyer(object):
    #Flyer is a class that captures all the general, foundational information
    #required to do calculations involving rigid bodies. 
    
    #A rigid body models a physical object with size, shape, and mass, that 
    #doesn't bend or break. It's a good approximation of, say, a wrench, and a
    #bad approximation of a water balloon. Unlike a particle (think a point with 
    #mass and position and velocity and nothing else), since it has size and 
    #shape, it can rotate and collide at angles and shit like that.
    
    #tbh idk why i named it "Flyer." Maybe it sounds friendlier than RB?
    def __init__(self, x, y, mass, vertices=None): 
        self.pos = np.array([x, y])
        self.mass = mass
        self.angle = 0
        self.angularV = 0        
        self.v = np.array([0, 0])

        self.vertices = vertices
        if vertices == None: 
            self.r = 10
            self.edges = None
        else: 
            self.edges = []
            self.r = np.linalg.norm(self.pos - np.array(vertices[0]))
            for i in range(0, len(vertices)):
                self.edges.append(Edge(vertices[i], vertices[i - 1])) 
                # ^ this assumes that edges are ordered clockwise or ccwise - gotta be convex!
                #TODO: should have a way to make sure they're ordered
                self.r = max(np.linalg.norm(self.pos - np.array(vertices[i])), self.r)
            self.r = round(self.r)

        self.momentOfInertia = None #TODO: how to calculate for polygons? and need a better variable name
        self.Surface = pygame.Surface((2 * self.r, 2 * self.r))
        self.Surface.convert_alpha()
        self.Surface.set_colorkey((0, 0, 0)) #black is transparent.

    def applyForce(self, force, deltaTime):
        #print("v was", self.v, end="")
        for i in range(2): self.v[i] += force[i] * deltaTime / self.mass
        #print(" adding", (force[0] * deltaTime / self.mass, force[1] * deltaTime / self.mass), " and now v is", self.v)

    def applyImpulse(self, impulse):
        for i in range(2): self.v[i] += impulse[i] / self.mass

    def draw(self, background):
        background.blit(self.Surface, (int(self.pos[0]) - self.r, int(self.pos[1]) - self.r))
        if(self.vertices == None):
            pygame.draw.circle(background, (255, 255, 255), (int(round(self.pos[0])), int(round(self.pos[1]))), self.r)
        else:
            getIntPointList = lambda a: [(round(a[i][0]), round(a[i][1])) for i in range(len(a))]
            pygame.draw.polygon(background,(255, 255, 255), getIntPointList(self.vertices))

    def move(self, deltaTime):

        updatedPos = lambda a, v, dt: [a[i] + v[i] * dt for i in range(2)]

        self.pos = updatedPos(self.pos, self.v, deltaTime)
        self.vertices = [updatedPos(vert, self.v, deltaTime) for vert in self.vertices]

class SpaceshipComponent(Flyer): 
    #TODO: need to break this up into engines, capsules, rockets, struts?, etc
    def __init__(self, x, y, xDiam, yDiam, mass, fuel):
        super().__init__(x, y, mass + fuel)
        self.fuel = fuel
        
        #if you pretend it's an ellipse, the xDiam is the diameter along
        #ITS x axis, not the global x axis.
        #Also, it's probably not going to be an ellipse - usually a cone or rectangle
        #or something like that, i expect.
        self.dims = [xDiam, yDiam]

    def steer(self, force):
        #fuel burned has a linear relationship with force produced. It really does! Proportion depends on fuel though.F
        pass

class Astronaut(Flyer):
    def __init__(self, x, y, mass, name):
        super().__init__(x, y, mass)
        self.health = 100
        self.name = name

class Spaceship(object):
    def __init__(self, x, y):
        self.pos = [x, y]
        self.stage = 0 #stage of separation I guess

class TestPlayer(Flyer):
    def __init__(self, x, y, mass, vertices):
        super().__init__(x, y, mass, vertices)

def puckCollide(A, B, deltaTime): #should i make deltaTime a global?
    dist = np.linalg.norm(A.pos - B.pos)
    if dist <= A.r + B.r: 
        deltaAVcoeff = (-2 * B.mass / (A.mass + B.mass)) * np.dot(A.v - B.v, A.pos - B.pos) / np.dot(A.pos - B.pos, A.pos - B.pos)
        deltaAV = deltaAVcoeff * (A.pos - B.pos) 
        #^if you stare at the above two lines for a while and ignore all the 
        #mass terms, this is really just a projection of relative velocity vector
        #onto the line connecting the centers of A and B.
        FBonA = A.mass * deltaAV / deltaTime #newton's second law
        FAonB = -FBonA #newton's third law
        A.applyForce(FBonA, deltaTime)
        B.applyForce(FAonB, deltaTime)

def boundsIntersect(A, B):
    #TODO: use pygame bounding boxes for sake of speed
    return np.linalg.norm(A.pos - B.pos) > A.r + B.r #yes, strictly greater than

def getEdgeIntersect(a, b): 
    
    x = (b.xIntercept - a.xIntercept) / (a.slope - b.slope)
    y = a.slope * x + a.xIntercept
    #make sure it's btw both pairs of endpoints!
    if (x <= max(a.endpoints[0][0], a.endpoints[1][0]) and 
        x >= min(a.endpoints[0][0], a.endpoints[1][0]) and
        y <= max(b.endpoints[0][1], b.endpoints[1][1]) and 
        y >= min(b.endpoints[0][1], b.endpoints[1][1])):
        return (x, y)
    return None

def rewindPosAndAng(A, deltaTime):
    A.pos += A.v * deltaTime
    A.angle += A.angularV * deltaTime

def getIntersects(A, B, deltaTime): 
    #TODO: think this is going to be troublesome with numpy's precision. Bug waiting to occur

    rewindPosAndAng(A, deltaTime)
    rewindPosAndAng(B, deltaTime) #DO NOT UNDO THIS BEFORE RETURNING. 
    #TODO: this isn't very clear, but i think this saves a lil time... refactor getNorm and getIntersects for clarity

    if boundsIntersect(A, B):
        intersects = []
        for edgeA in A.edges:
            for edgeB in B.edges:
                edgeIntersect = getEdgeIntersect(edgeA, edgeB)
                if edgeIntersect != None: intersects.append(edgeIntersect)
                if len(intersects) == 2: 
                    return intersects
    return None

def getNorm(intersects, facing):
    tangent = intersects[1] - intersects[0]
    n = np.array([tangent[1], -tangent[0]])
    
    mid = (intersects[0] + intersects[1])/2
    n = va.proj(facing.pos - mid, n)
    n /= va.dot(n, n)

    return n

def genCollide(A, B, deltaTime):
    intersects = getIntersects(A, B, 0)
    if intersects == None: return
    hi = deltaTime
    lo = 0
    i = 0
    timeEdit = 0
    while(i < 4 or (intersects == None and len(intersects) != 2)): 
        #TODO: 4 is a magic number. Should make desired iters a function of relative speed or something
        #iterate as desired, but better have 2 intersect points!

        if intersects == None or len(intersects) != 2: 
            lo = (lo + hi)/2
            timeEdit = (lo + hi)/2
        else:
            hi = (lo + hi)/2
            timeEdit = -(lo + hi)/2
        intersects = getIntersects(A, B, timeEdit)
    n = getNorm(intersects)
    #TODO: apply the crazy formula to A
    n = -n
    #now apply to B

def getSysKE(A, B):
    return 0.5 * (A.mass * np.linalg.norm(A.v)**2) + 0.5 * (B.mass * np.linalg.norm(B.v)**2)

def getSysMomentum(A, B):
    return A.mass * A.v + B.mass * B.v

def almostEqual(a, b, alpha=0.001):
    return abs(a - b) <= alpha

