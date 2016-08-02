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

    Player = f.TestPlayer(width/2, height/2, 1)
    Player.Surface.set_colorkey((0, 0, 0)) #black is transparent.
    Player.Surface = Player.Surface.convert_alpha()

    Collider = f.Flyer(width/3, height/3, 5)
    Collider.Surface.set_colorkey((0, 0, 0))
    Collider.Surface = Collider.Surface.convert_alpha()

    while mainloop:

        milliseconds = clock.tick(FPS)
        playtime += milliseconds
        deltaTime = milliseconds / 1000.0

        #^ clock.tick() returns number of milliseconds passed since last frame
        #FPS is otional. passing it causes a delay so that you dont go faster than FPS in your game

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                print(deltaTime)
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
                if event.key == pygame.K_DOWN:
                    Player.applyForce([0, 100], deltaTime)
                if event.key == pygame.K_UP:
                    Player.applyForce([0, -100], deltaTime)
                if event.key == pygame.K_LEFT:
                    Player.applyForce([-100, 0], deltaTime)
                if event.key == pygame.K_RIGHT:
                    Player.applyForce([100, 0], deltaTime)
   
        f.puckCollide(Player, Collider, deltaTime)
        #f.genCollide(Player, Collider, deltaTime)
        Player.move(deltaTime)
        Collider.move(deltaTime)

        screen.blit(background, (0, 0))
        Player.draw(screen)
        Collider.draw(screen)
        #TODO: wtf is get_rect?
        pygame.display.set_caption("Frame rate: {:0.2f} frames per second." 
                                   " Playtime: {:.2} seconds".format(
                                   clock.get_fps(),playtime))
        pygame.display.flip()
    pygame.quit()
main()
