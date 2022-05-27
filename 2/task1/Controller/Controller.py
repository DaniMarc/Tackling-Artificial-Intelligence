import math 
from heapq import heappop, heappush
import imp
from mimetypes import init
from operator import index
import pickle,pygame,time
from turtle import distance
from Model.PriorityQ import PriorityQ
from pygame.locals import *
from random import random, randint
import numpy as np

from queue import PriorityQueue

GREEN = (0, 255, 0)
RED = (255, 0, 0)

# indexVar = [[-1, 0], [0, 1], [1, 0], [0, -1]] #VERY WEIRD
indexVar = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]

indexVarGreedy = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
# indexVarGreedy = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]


class Controller:
    def __init__(self):
        self.__greedyParents = {}

    # For A*
    # Euclidean |  # Manhattan
    # 0.0087    |     # 0.0104
    # 0.0089    |     # 0.0128
    # 0.0099    |     # 0.0099
    # 0.0097    |     # 0.0105
    # 0.0089    |     # 0.0103
    # 0.0059    |     # 0.0079

    def __heuristic(self, cell1, cell2):
        x1,y1 = cell1[0], cell1[1]
        x2,y2 = cell2[0], cell2[1]
        # return abs(x1-x2) + abs(y1-y2)
        return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))


    def searchAStar(self, mapM, initialX, initialY, finalX, finalY):
        pathToGoal = PriorityQ()        #HERE IS F
        distanceSinceStart = {}         #HERE IS G
        self.__greedyParents = {}

        start = (initialX, initialY)
        goal = (finalX, finalY)

        pathToGoal.push((0, start))         
        distanceSinceStart[start] = 0       

        while pathToGoal:
            currentCell = pathToGoal.pop()[1]
            print(currentCell)
            for index in indexVar:
                if currentCell[0] > 0 and currentCell[0] < 19 and currentCell[1] > 0 and currentCell[1] < 19: 
                    nextCell = (currentCell[0]+index[0], currentCell[1]+index[1])
                    if mapM.surface[nextCell[0]][nextCell[1]] == 0:
                        if nextCell not in distanceSinceStart.keys() or distanceSinceStart[currentCell] + 1 < distanceSinceStart[nextCell]:
                            self.__greedyParents[nextCell] = currentCell
                            distanceSinceStart[nextCell] = distanceSinceStart[currentCell] + 1
                            pathToGoal.push((distanceSinceStart[nextCell] + self.__heuristic(nextCell, goal), nextCell))
            if currentCell == goal:
                return self.__greedyParents
        return "NO WAY"


    def searchGreedy(self, mapM, initialX, initialY, finalX, finalY):
        pathToGoal = PriorityQ()
        self.__greedyParents = {}

        start = (initialX, initialY)
        goal = (finalX, finalY)

        pathToGoal.push((0, start))

        while pathToGoal:
            currentCell = pathToGoal.pop()[1]
            print(currentCell)
            for index in indexVarGreedy:
                if currentCell[0] > 0 and currentCell[0] < 19 and currentCell[1] > 0 and currentCell[1] < 19:
                    nextCell = (currentCell[0]+index[0], currentCell[1]+index[1])
                    if mapM.surface[nextCell[0]][nextCell[1]] == 0:
                        if nextCell not in self.__greedyParents.keys():
                            self.__greedyParents[nextCell] = currentCell
                            pathToGoal.push((self.__heuristic(nextCell, goal), nextCell))
                            break

            if currentCell == goal:
                return self.__greedyParents
        return "NO WAY"


    def getGreedyParents(self):
        return self.__greedyParents

        
    def displayWithPath(self, image, path, shortPath, goal):
        mark = pygame.Surface((20,20))
        mark.fill(GREEN)
        for move in path:
            image.blit(mark, (move[1] *20, move[0] * 20))

        redMark = pygame.Surface((20,20))
        redMark.fill(RED)
        for move in shortPath:
            image.blit(redMark, (move[1] *20, move[0] *20))

        image.blit(redMark, (goal[1] *20, goal[0] *20))
        return image