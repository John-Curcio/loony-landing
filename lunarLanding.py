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

size = width, height = 700, 700
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
    # vertices = [[width/2 + sideLen/2, height/2 + sideLen/2],
    #         [width/2 - sideLen/2, height/2 + sideLen/2],
    #         [width/2 - sideLen/2, height/2 - sideLen/2],
    #         [width/2 + sideLen/2, height/2 - sideLen/2]]

    vertices = getVertices(width/2, height/2, 50, 6)
    Player = f.TestPlayer(width/2, height/2, 1, vertices)
    #Player = f.TestPlayer(width/2, height/2, 1, None)

    vertices = getVertices(width/3, height/3, 50, 4)
    Collider = f.Flyer(width/3, height/3, 5, vertices)
    Collider.Surface.set_colorkey((0, 0, 0))
    Collider.Surface = Collider.Surface.convert_alpha()

    bodiesOnScreen = {Player, Collider}

    arrowsToDirs = {pygame.K_DOWN:[0,1], 
                    pygame.K_UP:[0,-1], 
                    pygame.K_LEFT:[-1,0], 
                    pygame.K_RIGHT:[1,0]}
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
                force = [ arrowsToDirs[arrow][i] * 100 for i in range(2)]
                Player.applyForce(force, deltaTime)
   
        
        #collisions
        seen = set()
        tangent = None
        for A in bodiesOnScreen:
            seen.add(A)
            for B in bodiesOnScreen.difference(seen):
                # f.puckCollide(A, B, deltaTime)
                # f.genCollide(A, B, deltaTime)
                tangent = f.testCollide(A, B, deltaTime)


        Player.move(deltaTime)
        # Collider.move(deltaTime)

        screen.blit(background, (0, 0)) 
        Player.draw(screen)
        Collider.draw(screen)
        drawEdges(Collider, screen)
        drawEdges(Player, screen)
        if tangent != None:
            pygame.draw.line(screen, (255, 0, 0), tangent[0], tangent[1], 2)
        #TODO: wtf is get_rect?
        pygame.display.set_caption("Frame rate: {:0.2f} frames per second." 
                                   " Playtime: {:.2} seconds".format(
                                   clock.get_fps(),playtime))
        pygame.display.flip()
    pygame.quit()
main()
