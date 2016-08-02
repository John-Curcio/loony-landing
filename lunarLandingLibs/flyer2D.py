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
        self.slope = (a[1] - b[1]) / (a[0] - b[0])
        self.xIntercept = b[1] - self.slope * b[0]
        self.endpoints = [a, b]

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
    #TODO: a Flyer's shape should be discretized as a set of vertices. makes collision detection easier
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
            self.r = np.linalg.norm(self.pos - np.array(vertices[i]))
            for i in range(1, len(vertices)):
                self.edges.append(Edge(vertices[i], vertices[i - 1])) 
                # ^ this assumes that edges are ordered clockwise or ccwise - gotta be convex!
                #TODO: should have a way around this...
                self.r = max(np.linalg.norm(self.pos - np.array(vertices[i])), self.r)
            self.r = int(round(self.r))


        self.Surface = pygame.Surface((2 * self.r, 2 * self.r))
        self.momentOfInertia = None #TODO: how to calculate for polygons? and need a better variable name


    def applyForce(self, force, deltaTime):
        #print("v was", self.v, end="")
        self.v[0] += force[0] * deltaTime / self.mass
        self.v[1] += force[1] * deltaTime / self.mass
        #print(" adding", (force[0] * deltaTime / self.mass, force[1] * deltaTime / self.mass), " and now v is", self.v)

    def applyImpulse(self, impulse):
        self.v[0] += impulse[0] / self.mass
        self.v[1] += impulse[1] / self.mass

    def draw(self, background):
        background.blit(self.Surface, (int(self.pos[0]) - self.r, int(self.pos[1]) - self.r))
        if(self.vertices == None):
            pygame.draw.circle(background, (255, 255, 255), (int(self.pos[0]), int(self.pos[1])), self.r)
        else:
            pygame.draw.polygon(surface,color,lmap(lambda l: lmap(int, l),self.vertices),int(round(width)))
            #pygame.draw.polygon(surface, color, pointlist, line_thickness(optional)) 
            #alternatively, could draw every line. 

    def move(self, deltaTime):
        self.pos[0] += self.v[0] * deltaTime
        self.pos[1] += self.v[1] * deltaTime

    #TODO: need to describe the shape and mass distribution of a Flyer. 
    #   default should be a uniform distribution.
    #   or do i just have to calculate the moment of inertia? Shouldn't have to 
    #   work with the distribution of mass explicitly.
    #   Then again, fuel is ejected from fuel tanks and mass distribution changes accordingly...




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

    def steer(self, force): #force is a force 2-vector of variable magnitude
        #TODO: force should be applied to specific points on the spaceship's surface.
        #   fuel is ejected from thrusters. 
        self.fuel -= np.linalg.norm(force) #idk how this works tbh. TODO
        #               ^ vector magnitude

        #so I'm burning fuel, which produces a force in one direction
        #and there's an equal and opposite force in the direction I want to go in
        #which is the force vector of my input

        #fuel burned has a linear relationship with force produced
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
    def __init__(self, x, y, mass = 10):
        super().__init__(x, y, mass)

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
    #TODO: use pygame bounding boxes for speed
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

