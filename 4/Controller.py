import numpy as np
from copy import deepcopy
from domain.Map import Map
from domain.Ant import Ant
from utilities import Util

class Controller():
    def __init__(self):
        self.map = Map()
        self.pheromoneMatrix = []
        for i in range(self.map.n):
            self.pheromoneMatrix.append([])
            for j in range(self.map.m):
                self.pheromoneMatrix[-1].append([])
                for direction in Util.v:
                    neigh = [i + direction[0], j + direction[1]]
                    if not self.map.isWall(neigh):
                        if self.map.surface[neigh[0]][neigh[1]] == 2:
                            self.pheromoneMatrix[-1][-1].append([5 for _ in range(Util.maxSensorCapacity + 1)])
                        else:
                            self.pheromoneMatrix[-1][-1].append([1.0] + [0 for _ in range(Util.maxSensorCapacity)])
                    else:
                        self.pheromoneMatrix[-1][-1].append([0 for _ in range(Util.maxSensorCapacity + 1)])
        self.initialPheromoneMatrix = deepcopy(self.pheromoneMatrix)


    def epoch(self):
        population = []
        for i in range(Util.numberOfAnts):
            ant = Ant(self.map)
            population.append(ant)
        
        for i in range(self.map.battery):
            for ant in population:
                ant.addMove(self.pheromoneMatrix)
        for i in range(self.map.n):
            for j in range(self.map.m):
                for direction in Util.v:
                    for spent in range(Util.maxSensorCapacity + 1):
                        self.pheromoneMatrix[i][j][Util.v.index(direction)][spent] *= (1- Util.rho)
                        self.pheromoneMatrix[i][j][Util.v.index(direction)][spent] += Util.rho * self.initialPheromoneMatrix[i][j][Util.v.index(direction)][spent]
        best_ant = population[max([[population[i].fitness(), i] for i in range(len(population))])[1]]
        best_fitness = best_ant.fitness()

        for ant in population:
            ant_fitness = ant.fitness()
            for i in range(len(ant.path) - 1):
                x = ant.path[i]
                y = ant.path[i+1]
                direction_index = Util.v.index((y[0] - x[0], y[1] - x[1]))
                self.pheromoneMatrix[x[0]][x[1]][direction_index][y[2]] += (ant_fitness + 1) / (best_fitness + 1)
        return best_ant, np.mean([ant.fitness() for ant in population])


    def computeACO(self):
        solution_ant = None
        fitnesses = []
        for i in range(Util.numberOfEpochs):
            print(i, end=" ")
            current_ant, fitness = self.epoch()
            fitnesses.append(fitness)
            if solution_ant is None or solution_ant.fitness() < current_ant.fitness():
                solution_ant = current_ant
        print(solution_ant.fitness())
        return solution_ant, fitnesses