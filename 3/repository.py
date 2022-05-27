# -*- coding: utf-8 -*-

import pickle

from attr import attributes
from domain import *


class repository():
    def __init__(self):
        self.__populations = []
        self.drone_map = None
        
    def createPopulation(self, popSize, indSize):
        # args = [populationSize, individualSize] -- you can add more args    
        self.__populations = Population(self.drone_map, popSize, indSize)
        return self.__populations

    
    def get_population(self):
        return self.__populations

    
    def set_population(self, newPop):
        self.__populations = newPop
        
            