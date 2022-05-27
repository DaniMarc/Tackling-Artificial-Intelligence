from Controller import Controller
from utilities import *
from Gui import *
import numpy as np
import matplotlib.pyplot as plt


def drawPlot(data):
    arr = np.array(data)
    m = np.mean(arr, axis=0)
    std = np.std(arr, axis=0)
    means = []
    stddev = []
    means.append(m)
    stddev.append(std)
    plt.plot(means)
    plt.plot(stddev)
    plt.plot(data)
    plt.show()


def main():
    battery = Util.batteryCapacity
    c = Controller()
    # ant = c.computeACO()
    ant, fitnesses = c.computeACO()
    drawPlot(fitnesses)
    print("Average: "+str(np.average(fitnesses)))
    print("Standard deviaton: "+str(np.std(fitnesses)))
    moving_drone(c.map, ant.path)



main()