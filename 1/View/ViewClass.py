import time
import pygame
from pygame.locals import *
from random import randint
from Controller.Drone import Drone

from Model.DMap import DMap
from Model.Environment import Environment

#Creating THE color
WHITE = (255, 255, 255)

class View:
    def __init__(self) -> None:
        pass

    def start(self):
        #we create the environment
        env = Environment()
        env.loadEnvironment("test2.map")
        #print(str(e))
        
        # we create the map for the DRONE
        labyrinth = DMap() 
        
        
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")
            
        
        
        # we position the drone somewhere in the area
        x = randint(0, 19)
        y = randint(0, 19)
        
        #cream drona
        drone = Drone(x, y)
        
        
        
        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((800,400))
        screen.fill(WHITE)
        screen.blit(env.image(), (0,0))
        
        # define a variable to control the main loop
        running = True
        
        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
                
            drone.moveDSF(labyrinth)

            labyrinth.markDetectedWalls(env, drone.x, drone.y)
            time.sleep()
            screen.blit(labyrinth.image(drone.x,drone.y),(400,0))
            pygame.display.flip()
        
        pygame.quit()