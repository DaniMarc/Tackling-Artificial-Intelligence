# -*- coding: utf-8 -*-
# imports
import matplotlib.pyplot as plot
import numpy
from gui import *
from controller import *
from repository import *
from domain import *


class UI():
    def __init__(self, c):
        self.__controller = c
        self.__map = Map()
        self.__stats = None
        self.__path = None
        self.__batteryLevel = 3
        self.__maxIterations = 100
        self.__populationSize = 50
        self.__individualSize = 8


    def MapUI(self):
        while True:
            self.printOptionMap()
            x = input("Input your option: ")
            if x == "1":
                m = Map()
                m.randomMap()
                self.__map = m
                self.__controller.set_map(self.__map)
            elif x == "2":
                filename = input("\t>>Input the file name to load the map from:")
                self.__map.loadMap(filename);
                self.__controller.set_map(self.__map)
            elif x == "3":
                filename = input("\t>>Input the file name to save the map to:")
                self.__map.saveMap(filename)
                self.__controller.set_map(self.__map)
            elif x == "4":
                movingDrone(self.__map, [[-1,-1]])
            elif x == "5":
                return
            else:
                print("Wrong option!")


    def parametersSetUp(self):
        self.__batteryLevel = int(input("\t>>>Introduce the battery capacity:"))
        self.__maxIterations = int(input("\t>>>Introduce the number of iterations:"))
        self.__populationSize = int(input("\t>>>Introduce the size of the population:"))
        self.__individualSize = int(input("\t>>>Introduce the size of the individual:"))
        self.__controller.set_parameters(self.__batteryLevel, self.__maxIterations, self.__populationSize, self.__individualSize)
        return


    def view_statistics(self):
       plot.plot(self.__stats)
       plot.show()


    def solver(self):
        return self.__controller.solver()


    def EAUI(self):
        while True:
            self.printOptionEA()
            x = input("Input your option: ")
            if x == "1":                    # a. parameters setup
                self.parametersSetUp()
            elif x == "2":                  # b. run the solver
                fitness_over_generations = []
                # self.__stats = []
                for i in range(30):
                    numpy.random.seed(i)
                    self.__path, stat, best_fitness = self.solver()
                    if self.__stats == None:
                        self.__stats = stat
                    fitness_over_generations.append(best_fitness)
                print("-------------------")
                print("Average: "+str(numpy.average(fitness_over_generations)))
                print("Standard deviaton: "+str(numpy.std(fitness_over_generations)))
            elif x == "3":                  # c. visualize the statistics
                self.view_statistics()
            elif x == "4":                  # d. view the drone moving on a path
                movingDrone(self.__controller.get_map(), self.__path)
            elif x == "5":
                return
            else:
                print("Wrong option!")


    def printOption(self):
            print("\n>>>\t========================================\t<<<")
            print("1.Map options")
            print("2.Evolutionary Algorithm options")
            print("3.Exit")


    def printOptionMap(self):
        print("\n>>>\t================= Map options =======================\t<<<")
        print("1.Create a random map")
        print("2.Load a map")
        print("3.Save a map")
        print("4.Visualize a map")
        print("5.Exit")


    def printOptionEA(self):
        print("\n>>>\t================== Evolutionary Algorithm ======================\t<<<")
        print("1.Parameters setup")
        print("2.Run the solver")
        print("3.Visualize the statistics")
        print("4.View the drone moving on a path")
        print("5.Exit")


    def run(self):
        done = False
        while not done:
            self.printOption()
            x = input("Input your option: ")
            if x == "1":
                self.MapUI()
            elif x == "2":
                self.EAUI()
            elif x == "3":
                exit()
            else:
                print("Wrong option!")


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualize map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualize the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATTENTION! the function doesn't check if the path passes trough walls