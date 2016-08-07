import random
import numpy
import tkinter

import pygame
from pygame.locals import *
#import sys

#custom modules
from lunarLandingLibs import flyer2D as f

################################################################################


pygame.init()
################################################################################
#set up the window

size = width, height = 500, 500
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
def main():
    
    FPS = 15 #desired frame rate in frames per second.
    clock = pygame.time.Clock() #create a pygame clock object
    playtime = 0.0 #milliseconds elapsed since start of game.
    
    mainloop = True

    sideLen = 25
    vertices = [[width/2 + sideLen/2, height/2 + sideLen/2],
            [width/2 - sideLen/2, height/2 + sideLen/2],
            [width/2 - sideLen/2, height/2 - sideLen/2],
            [width/2 + sideLen/2, height/2 - sideLen/2]]

    Player = f.TestPlayer(width/2, height/2, 1, vertices)
    #Player = f.TestPlayer(width/2, height/2, 1, None)

    # Collider = f.Flyer(width/3, height/3, 5)
    # Collider.Surface.set_colorkey((0, 0, 0))
    # Collider.Surface = Collider.Surface.convert_alpha()

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

        pygame.event.get()
        #     if event.type == pygame.K_ESCAPE or event.type==pygame.QUIT: 
        #         mainloop = False # pygame window closed by user

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]: mainloop = False
        for arrow in arrowsToDirs.keys():
            if pressed[arrow]:
                # print(deltaTime)
                force = [ arrowsToDirs[arrow][i] * 100 for i in range(2)]
                Player.applyForce(force, deltaTime)
   
        #f.puckCollide(Player, Collider, deltaTime)
        #f.genCollide(Player, Collider, deltaTime)
        Player.move(deltaTime)
        # Collider.move(deltaTime)

        screen.blit(background, (0, 0)) 
        Player.draw(screen)
        # Collider.draw(screen)
        #TODO: wtf is get_rect?
        pygame.display.set_caption("Frame rate: {:0.2f} frames per second." 
                                   " Playtime: {:.2} seconds".format(
                                   clock.get_fps(),playtime))
        pygame.display.flip()
    pygame.quit()
main()
