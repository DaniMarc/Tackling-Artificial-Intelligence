# -*- coding: utf-8 -*-

import pickle
from random import *
import numpy as np
from utils import *
import copy

# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]
START_POSITION = [0, 0]


class Gene:
    def __init__(self):
        r_value = randint(0,3)
        self.__direction = v[r_value]


    @property
    def direction(self):
        return self.__direction

    
    def __getitem__(self, item):
        return self.__direction[item]


    def __setitem__(self, item):
        self.__direction = item


class Individual:
    def __init__(self, size, mappy):
        self.__map = mappy
        self.__originalMap = mappy
        self.__size = size
        self.__x = [Gene() for i in range(self.__size)]
        self.__f = 0
        self.__seen_zones = []
        self.drone_explore() #TODO


    def __mark_seen_squares_visited(self, drone_position):
        sensors_reading = self.__map.readUDMSensors(drone_position[0], drone_position[1])
        
        dummy_position = [0,0]    

        # MARKING UPWARD
        dummy_position[0] = drone_position[0]
        dummy_position[1] = drone_position[1]
        for square in range(sensors_reading[UP]):
            dummy_position[0] += v[UP][0]
            if [dummy_position[0], dummy_position[1]] not in self.__seen_zones:
                self.__seen_zones.append([dummy_position[0], dummy_position[1]])

        # MARKING RIGHTWARD
        dummy_position[0] = drone_position[0]
        dummy_position[1] = drone_position[1]
        for square in range(sensors_reading[RIGHT]):
            dummy_position[1] += v[RIGHT][1]
            if [dummy_position[0], dummy_position[1]] not in self.__seen_zones:
                self.__seen_zones.append([dummy_position[0], dummy_position[1]]) 

        # MARKING DOWNWARD
        dummy_position[0] = drone_position[0]
        dummy_position[1] = drone_position[1]
        for square in range(sensors_reading[DOWN]):
            dummy_position[0] += v[DOWN][0]
            if [dummy_position[0], dummy_position[1]] not in self.__seen_zones:
                self.__seen_zones.append([dummy_position[0], dummy_position[1]]) 

        # MARKING LEFTWARD
        dummy_position[0] = drone_position[0]
        dummy_position[1] = drone_position[1]
        for square in range(sensors_reading[LEFT]):
            dummy_position[1] += v[LEFT][1]
            if [dummy_position[0], dummy_position[1]] not in self.__seen_zones:
                self.__seen_zones.append([dummy_position[0], dummy_position[1]]) 
        return


    def drone_explore(self):
        drone_position = [0,0]
        drone_position[0] = START_POSITION[0]
        drone_position[1] = START_POSITION[1]       

        self.__mark_seen_squares_visited(copy.deepcopy(drone_position))
        for gene in self.__x:
            drone_position[0] += gene[0]
            drone_position[1] += gene[1]
            self.__mark_seen_squares_visited(copy.deepcopy(drone_position))


    def fitness(self):
        # compute the fitness for the individual
        # and save it in self.__f
        for i in range(self.__originalMap.n):
            for j in range(self.__originalMap.m):
                if self.__originalMap.surface[i][j] == 1 and [i,j] in self.__seen_zones:
                    self.__f -= 100
        self.__f += len(self.__seen_zones)
        return self.__f


    def get_fitness(self):
        return self.fitness()


    def mutate(self, mutateProbability = 0.04):
        # perform a mutation with respect to the representation
        if random() < mutateProbability:
            ind = randint(0, self.__size-1)
            new_dir = v[randint(0,3)]
            while self.__x[ind] == new_dir:
                new_dir = v[randint(0,3)]
            self.__x[ind] = new_dir
        self.drone_explore()
        return
        
    
    def get_genome(self):
        return self.__x


    def crossover(self, otherParent, crossoverProbability = 0.8):
        # perform the crossover between the self and the otherParent 
        offspring1, offspring2 = Individual(self.__size, self.__map), Individual(self.__size, self.__map) 
        if random() < crossoverProbability:
            cross_length = randint(1, self.__size)
            dummy_ind1 = []
            real_parent1 = copy.deepcopy(self.__x)

            dummy_ind2 = []
            real_parent2 = copy.deepcopy(otherParent.__x)

            for i in range(cross_length):
                dummy_ind1.append(real_parent2[i])
                dummy_ind2.append(real_parent1[i])
            for i in range(cross_length, self.__size):
                dummy_ind1.append(real_parent1[i])
                dummy_ind2.append(real_parent2[i])
        return offspring1, offspring2
    

class Population():
    def __init__(self, dmap, populationSize = 0, individualSize = 0):
        self.__populationSize = populationSize
        self.__v = [Individual(individualSize, dmap) for x in range(populationSize)]
        

    def append(self, other):
        self.__v.append(other)


    def evaluate(self):
        # evaluates the population
        for x in self.__v:
            x.fitness()
            
            
    def selection(self, k = 0):
        # perform a selection of k individuals from the population
        # and returns that selection
        n = len(self.__v)
        for step in range(len(self.__v)//2):
            individuals = []
            for i in range(k):
                nr = randint(0, n - 1)
                individuals.append(self.__v[nr])

            selection = sorted(individuals, key=lambda x : x.get_fitness())
            self.__v.remove(selection[0])
            n -= 1
        return self
    

    def get_best(self):
        for i in self.__v:
            i.get_fitness()
        selection = sorted(self.__v, key=lambda x : x.get_fitness())
        return selection[len(self.__v)-1]


    def __len__(self):
        return len(self.__v)


    def __getitem__(self, item):
        return self.__v[item]


class Map():
    def __init__(self, n = 20, m = 20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
    
    
    def randomMap(self, fill = 0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill :
                    self.surface[i][j] = 1
                

    def loadMap(self, numfile = "test.map"):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()


    def saveMap(self, numFile = "test.map"):
        with open(numFile,'wb') as f:
            pickle.dump(self, f)
            f.close()


    def __str__(self):
        string=""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    
    def readUDMSensors(self, x, y):
        # Method taken from lab1

        readings = [0, 0, 0, 0]
        # UP
        xf = x - 1
        while ((xf >= 0) and (self.surface[xf][y] == 0)):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while ((xf < self.n) and (self.surface[xf][y] == 0)):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while ((yf < self.m) and (self.surface[x][yf] == 0)):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.surface[x][yf] == 0)):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1

        return readings


    def check_drone_pos(self, x, y):
        if x >= 0 and x < self.n and y>=0 and y < self.m and self.surface[x][y] == 0:
            return True
        return False