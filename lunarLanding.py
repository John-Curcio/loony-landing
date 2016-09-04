import random
import numpy
import tkinter
import math

import pygame
from pygame.locals import *
#import sys

#custom modules
from lunarLandingLibs import flyer2D as f

################################################################################


pygame.init()
################################################################################
#set up the window

size = width, height = 1000, 1000
screen = pygame.display.set_mode(size) #set size of game window
background = pygame.Surface(screen.get_size()) #create empty surface
background.fill((0, 100, 230)) #fill surface with some color
background = background.convert()   
#^ not 100% necessary, just makes things faster.
#surfaces with transparency need .convert_alpha() instead

#after creating the background, the surface isn't visible yet.
#need to blit (~paint) it in order to see it V
screen.blit(background, (0, 0)) #(0,0) is upper left corner


################################################################################
#the main loop. also handles view, except for setting up the screen.

def getVertices(x, y, r, numVerts):
    vertices = []
    for i in range(numVerts):
        angle = i * 2 * math.pi / numVerts
        vertices.append([x + r * math.cos(angle), y + r * math.sin(angle)])
    return vertices

def drawEdges(A, screen):
    if (len(A.getEdges()) != len(A.vertices)):
        print(len(A.getEdges()))
        print(len(A.vertices))
        assert(False)
    for edge in A.getEdges():
        pygame.draw.line(screen, (0, 255, 0), edge[0], edge[1], 3)

def main():
    
    FPS = 15 #desired frame rate in frames per second.
    clock = pygame.time.Clock() #create a pygame clock object
    playtime = 0.0 #milliseconds elapsed since start of game.
    
    mainloop = True

    # sideLen = 25
    # vertices = [
    #         [width/2 + 3 * sideLen, height/2 + 3 * sideLen],
    #         [width/2 - sideLen/2, height/2 + sideLen/2],
    #         [width/2 - sideLen/2, height/2 - sideLen/2],
    #         [width/2 + sideLen/2, height/2 + sideLen/2],
    #         [width/2 + sideLen/2, height/2 - sideLen/2]]

    vertices = getVertices(width/2, height/2, 80, 3)
    Player = f.TestPlayer(width/2, height/2, 4, vertices)
    #Player = f.TestPlayer(width/2, height/2, 1, None)

    vertices = getVertices(width/3, height/3, 100, 3)
    Collider = f.Flyer(width/3, height/3, 4, vertices)
    Collider.Surface.set_colorkey((0, 0, 0))
    Collider.Surface = Collider.Surface.convert_alpha()

    vertices = getVertices(2 * width/3, 2 * height/3, 50, 4)
    Ass = f.Flyer(2 * width/3, 2 * height/3, 4, vertices)

    vertices = getVertices(2 * width/3, height/3, 50, 5)
    Butt = f.Flyer(2 * width/3, height/3, 4, vertices)

    bodiesOnScreen = {Player, Collider, Ass, Butt}

    arrowsToDirs = {pygame.K_DOWN:[0,1], 
                    pygame.K_UP:[0,-1], 
                    pygame.K_LEFT:[-1,0], 
                    pygame.K_RIGHT:[1,0]}

    wasdToDirs = {pygame.K_s:arrowsToDirs[pygame.K_DOWN],
                    pygame.K_w: arrowsToDirs[pygame.K_UP],
                    pygame.K_a: arrowsToDirs[pygame.K_LEFT],
                    pygame.K_d: arrowsToDirs[pygame.K_RIGHT]}

    #print(Player.momentOfInertia, Collider.momentOfInertia)
    while mainloop:

        milliseconds = clock.tick(FPS)
        playtime += milliseconds
        deltaTime = milliseconds / 1000.0

        #^ clock.tick() returns number of milliseconds passed since last frame
        #FPS is otional. passing it causes a delay so that you dont go faster than FPS in your game

        #keyboard actions
        pygame.event.get()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]: mainloop = False #TODO: how to check if user clicks on window X?
        for arrow in arrowsToDirs.keys():
            if pressed[arrow]:
                force = [ arrowsToDirs[arrow][i] * 1000 for i in range(2)]
                Player.applyForce(force, deltaTime)
        for arrow in wasdToDirs.keys():
            if pressed[arrow]:
                force = [wasdToDirs[arrow][i] * 1000 for i in range(2)]
                Collider.applyForce(force, deltaTime)

        if pressed[pygame.K_z]: # need a method for applying torque...how do legit spaceships do it?
            Player.angularV += math.pi / 100
        elif pressed[pygame.K_c]:
            Player.angularV -= math.pi / 100
        if pressed[pygame.K_b]:
            Player.v *= 0
            Player.angularV = 0
            # when i want my ship to rotate, can i use a reaction chain (?) or do i need to use thrusters?
        
        #collisions
        seen = set()
        tangent = None
        for A in bodiesOnScreen:
            seen.add(A)
            for B in bodiesOnScreen.difference(seen):
                # f.puckCollide(A, B, deltaTime)
                # f.genCollide(A, B, deltaTime)
                tangent = f.testCollide(A, B, deltaTime)


        screen.blit(background, (0, 0)) 
        for Body in bodiesOnScreen:
            Body.move(deltaTime)        
            Body.draw(screen)

        #drawEdges(Collider, screen) 
        #drawEdges(Player, screen) 
        if tangent != None:
            pygame.draw.line(screen, (255, 0, 0), tangent[0], tangent[1], 2)
            n = f.getNorm(tangent, Player)
            mid = [(tangent[0][i] + tangent[1][i]) / 2 for i in range(2)]
            pygame.draw.line(screen, (0, 255, 0), mid, [mid[i] + n[i] for i in range(2)], 3)
        #TODO: wtf is get_rect?
        pygame.display.set_caption("Frame rate: {:0.2f} frames per second." 
                                   " Playtime: {:.2} seconds".format(
                                   clock.get_fps(),playtime))
        pygame.display.flip()
    pygame.quit()
main()

# Vertices: [array([ 400.,  350.]), array([ 365.45084972,  397.55282581]), array([ 309.54915028,  379.38926261]), array([ 309.54915028,  320.61073739]), array([ 365.45084972,  302.44717419])]
# Vertices: [array([ 400.,  350.]), array([ 365.45084972,  397.55282581]), array([ 390.45084972,  379.38926261]), array([ 390.45084972,  320.61073739]), array([ 365.45084972,  302.44717419])]
