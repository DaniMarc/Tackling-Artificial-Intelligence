import math
import torch
from utils import *


def function(x, y):
    return math.sin(x + y / math.pi)


def getRandomValues():
    return [-20 * x + 10 for x in torch.rand(SAMPLE_SIZE)]


def getRandomPoints():
    return getRandomValues(), getRandomValues()


def createDB():
    filePath = "myDataset.dat"
    result = []
    print("GETTING RANDOM POINTS...")
    allX, allY = getRandomPoints()
    print("GENERATED!")
    i = 0
    print("GENERATING POINTS DATABASE...")
    for i in range(SAMPLE_SIZE):
        result.append((allX[i], allY[i], function(allX[i], allY[i])))
    print("JOB'S DONE!")
    torchData = torch.tensor([point for point in result])
    torch.save(torchData, filePath)



createDB()