from repository import *


class Controller():
    def __init__(self, r):
        self.__nr_iterations = 0
        self.__repo = r
        self.__batteryLevel = 10
        self.__maxIterations = 1000
        self.__populationSize = 100
        self.__individualSize = 10
    

    def get_map(self):
        return self.__repo.drone_map


    def set_map(self, mappy):
        self.__repo.drone_map = mappy


    def set_parameters(self, Bl, Mi, Ps, Is):
        self.__batteryLevel = Bl
        self.__maxIterations = Mi
        self.__populationSize = Ps
        self.__individualSize = Is


    def iteration(self):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parrents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors
        parents = self.__repo.get_population()
        children = Population(self.__repo.drone_map)

        for i in range(len(parents)//2):
            child1, child2 = parents[randint(0,len(parents)-1)].crossover(parents[randint(0, len(parents)-1)])
            child1.mutate()
            child2.mutate()

            children.append(child1)
            children.append(child2)

        for kid in children:
            parents.append(kid)
        parents = parents.selection(5)
        self.__repo.set_population(parents)

        sum = 0
        for i in self.__repo.get_population():
            sum += i.get_fitness()

        return sum/len(self.__repo.get_population())
        

    def stop_condition(self):
        if self.__nr_iterations == self.__maxIterations:
            return True
        return False


    def run(self):
        # until stop condition
        #    perform an iteration
        #    save the information need it for the statistics
        
        # return the results and the info for statistics
        fitness = []
        while not self.stop_condition():
            self.__nr_iterations += 1
            if self.__nr_iterations % 100 == 0:
                print("On iteration "+str(self.__nr_iterations))
            fitness.append(self.iteration())

        winning_specimen = self.__repo.get_population().get_best().get_genome()
        path = []
        pos = [0,0]
        pos[0] = 0
        pos[1] = 0
        path.append((pos[0], pos[1]))
        for step in winning_specimen:
            pos[0] += step[0]
            pos[1] += step[1]
            if not self.__repo.drone_map.check_drone_pos(pos[0], pos[1]):
                break
            path.append((pos[0], pos[1]))
        return path, fitness, self.__repo.get_population().get_best().get_fitness()
    
    
    def solver(self):
        # create the population,
        # run the algorithm
        # return the results and the statistics
        self.__repo.createPopulation(self.__populationSize, self.__individualSize)
        return self.run()
       