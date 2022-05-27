from itertools import count
from locale import currency
import pygame
from pydoc import visiblename
from pygame.locals import *


class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gotoStack = [(x,y)]
        self.trackBack = []
        self.visitedAreas = []
        self.flags = [0,0,0,0]
    
    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x-1][self.y]==0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x+1][self.y]==0:
                self.x = self.x + 1
        
        if self.y > 0:
              if pressed_keys[K_LEFT]and detectedMap.surface[self.x][self.y-1]==0:
                  self.y = self.y - 1
        if self.y < 19:        
              if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y+1]==0:
                  self.y = self.y + 1
                  

    def moveDSF(self, detectedMap):
        self.flags = [0,0,0,0]
        self.visitedAreas.append((self.x, self.y))

        if self.y > 0:
            if (self.x, self.y-1) not in self.visitedAreas and detectedMap.surface[self.x][self.y-1]==0:
                self.gotoStack.append((self.x, self.y-1))
            elif detectedMap.surface[self.x][self.y-1]==1:
                self.flags[0] = 1

        if self.x < 19:
            if (self.x+1, self.y) not in self.visitedAreas and detectedMap.surface[self.x+1][self.y]==0:
                self.gotoStack.append((self.x+1, self.y))
            elif detectedMap.surface[self.x+1][self.y]==1:
                self.flags[1] = 1

        if self.y < 19:        
            if (self.x, self.y+1) not in self.visitedAreas and detectedMap.surface[self.x][self.y+1]==0:
                self.gotoStack.append((self.x, self.y+1))
            elif detectedMap.surface[self.x][self.y+1]==1:
                self.flags[2] = 1

        if self.x > 0:
            if (self.x-1, self.y) not in self.visitedAreas and detectedMap.surface[self.x-1][self.y]==0:
                self.gotoStack.append((self.x-1, self.y))
            elif detectedMap.surface[self.x-1][self.y]==1:
                self.flags[3] = 1        

        # if 1 in self.flags and ((self.x-1,self.y) not in self.gotoStack and (self.x+1,self.y) not in self.gotoStack and (self.x,self.y-1) not in self.gotoStack and (self.x,self.y+1) not in self.gotoStack):
        #     if len(self.trackBack) != 0:
        #         self.x, self.y = self.trackBack.pop()
        # else:
        #     self.trackBack.clear()
        if len(self.gotoStack) != 0:
            self.x, self.y = self.gotoStack.pop()
            self.trackBack.append((self.x, self.y))
        
