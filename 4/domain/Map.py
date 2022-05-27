import imp
from random import randint, random
from utilities import Util
import numpy as np
import pygame


class Map:
    def __init__(self):
        self.n = Util.mapLength
        self.m = Util.mapLength
        self.surface = np.zeros((self.n, self.m))
        self.randomMap()
        self.x, self.y = Util.initialPosition
        self.battery = Util.batteryCapacity

    
    def randomMap(self, wall_chance=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= wall_chance:
                    self.surface[i][j] = 1
        
        for i in range(Util.numberOfSensors):
            sx = randint(0, self.n - 1)
            sy = randint(0, self.m - 1)
            while self.surface[sx][sy] == 1:
                sx = randint(0, self.n - 1)
                sy = randint(0, self.m - 1)
            self.surface[sx][sy] = 2

    def isWall(self, var):
        if var[0] < 0 or var[0] > Util.mapLength - 1 or var[1] < 0 or var[1] > Util.mapLength - 1 or self.surface[var[0]][var[1]] == 1:
            return True
        return False