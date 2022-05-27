import pickle, pygame, time
from Controller.Controller import Controller
from Model.Drone import Drone
from Model.Map import Map
from pygame.locals import *
from random import random, randint
import numpy as np
import time


#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations 
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]



class View:
    def __init__(self) -> None:
        pass

    def start(self):
        # we create the map
        m = Map() 
        #m.randomMap()
        #m.saveMap("test2.map")
        m.loadMap("test1.map")
            
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")
            
        # we position the drone somewhere in the area
        # x = randint(0, 19)
        # y = randint(0, 19)
        x = 2
        y = 3
        finalx = 19
        finaly = 18
        
        #create drona
        d = Drone(x, y)
        c = Controller()
        
        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((400,400))
        screen.fill(WHITE)
            
        # define a variable to control the main loop
        running = True
        
        algorithm = int(input("Choose 1.A* or 2.Greedy: \n"))
        # algorithm = 2

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
                    
            screen.blit(d.mapWithDrone(m.image()),(0,0))
            pygame.display.flip()

        path = {}
        if algorithm == 1:
            try:
                now = time.time()
                path = c.searchAStar(m, x, y, finalx, finaly)
                print("A* HAS BEEN DONE IN "+str(time.time()-now))
                screen.blit(c.displayWithPath(m.image(), path.keys(), path.values(), (finalx, finaly)), (0,0))
            except TypeError:
                print("A* couldn't make it?...")
                path = c.getGreedyParents()
                screen.blit(c.displayWithPath(m.image(), path.keys(), path.values(), (x, y)), (0,0))
        elif algorithm == 2:
            try:
                now = time.time()
                path = c.searchGreedy(m, x, y, finalx, finaly)
                print("GREEDY HAS BEEN DONE IN "+str(time.time()-now))
                screen.blit(c.displayWithPath(m.image(), path.keys(), path.values(), (finalx, finaly)), (0,0))
            except TypeError:
                print("Greedy couldn't make it...")
                path = c.getGreedyParents()
                screen.blit(c.displayWithPath(m.image(), path.keys(), path.values(), (x, y)), (0,0))
            except IndexError:
                print("Greedy couldn't make it...")
                path = c.getGreedyParents()
                screen.blit(c.displayWithPath(m.image(), path.keys(), path.values(), (x, y)), (0,0))
        else:
            print("Excuse me?")

        
        
        
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()