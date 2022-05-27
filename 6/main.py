import csv
import random
import numpy as np
import matplotlib.pyplot as plt

numberOfClusters = 4;
iterations = 10

def readPoints(fileName):
    result = {}
    points = []
    with open(fileName) as csv_file:
        spam_reader = csv.reader(csv_file)
        for row in spam_reader:
            if row[0] == 'label':
                continue
            points.append((float(row[1]), float(row[2])))
            result[(float(row[1]), float(row[2]))] = row[0]
    return result, points


def selectInitialCentroids(elements, k=numberOfClusters):
    result = []
    for cluster in range(k):
        result.append(random.choice(elements))
    return result


def euclideanDistance(A, B):
    return np.linalg.norm(np.array(A) - np.array(B))


def assignPointsToCentroid(points, centroids):
    assignedLabel = {}
    for centroid in centroids:
        assignedLabel[centroid] = []

    for point in points:
        minDistance = np.inf
        for centroid in centroids:
            if euclideanDistance(point, centroid) < minDistance:
                assignedLabel[centroid].append(point)
                minDistance = euclideanDistance(point, centroid)
    return assignedLabel


def computeMeanX(points):
    return np.mean([point[0] for point in points])


def computeMeanY(points):
    return np.mean([point[1] for point in points])


def recomputeCentroid(clusters, centroids):
    newCentroids = []

    for centroid in clusters.keys():
        currentCluster = clusters[centroid]
        newCentroid = (computeMeanX(currentCluster), computeMeanY(currentCluster))
        newCentroids.append(newCentroid)

    return newCentroids


def conditionToStopKMean(centroids, newCentroids):
    if centroids == newCentroids:
        return True
    return False


def finalPlot(assignedLabels):
    colors = ['red', 'green', 'blue', 'yellow']
    index = 0
    for key in assignedLabels:
        plt.scatter(
            [point[0] for point in assignedLabels[key]],
            [point[1] for point in assignedLabels[key]],
            c=colors[index]
        )
        index += 1

    plt.scatter([centroid[0] for centroid in assignedLabels], [centroid[1] for centroid in assignedLabels], c='black')
    plt.show()


def giveValueToEachCentroid(assignedLabels):
    centroids = list(assignedLabels.keys())
    centroidA = min(centroids, key=lambda x: x[0])
    centroids.remove(centroidA)

    centroidC = max(centroids, key=lambda x: x[0])
    centroids.remove(centroidC)

    centroidD = min(centroids, key=lambda x: x[1])
    centroids.remove(centroidD)

    return {centroidA: 'A', centroids[0]: 'B', centroidC: 'C', centroidD: 'D'}


def statistics(assignedLabels, initialData, mappedCentroids):
    correctlyComputed = 0
    correctForLabel = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    totalForLabel = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    totalInitialLabel = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for key, value in assignedLabels.items():
        for val in value:
            if initialData[val] == mappedCentroids[key]:
                correctlyComputed += 1
                correctForLabel[initialData[val]] += 1
            totalForLabel[mappedCentroids[key]] += 1
            totalInitialLabel[initialData[val]] += 1

    accuracyIndex = correctlyComputed / len(initialData)
    print(">>>Accuracy index:", accuracyIndex, "\n")

    precision = {}
    rappel = {}
    score = {}
    for key in ['A', 'B', 'C', 'D']:
        precision[key] = correctForLabel[key] / totalForLabel[key]
        rappel[key] = correctForLabel[key] / totalInitialLabel[key]
        score[key] = 2 * precision[key] * rappel[key] / (precision[key] + rappel[key] + 1)

    print(">>>Precision:", precision, "\n")
    print(">>>Rappel:", rappel, "\n")
    print(">>>Score:", score, "\n")


def main():
    data, points = readPoints("dataset.csv")
    finalLabels = {}
    finalDunnIndex = -np.inf
    for iteration in range(iterations):
        random.seed(iteration * 25 + 956 / (iteration+1))
        centroids = selectInitialCentroids(points)

        assignedLabel = assignPointsToCentroid(points, centroids)
        newCentroids = recomputeCentroid(assignedLabel, centroids)
        while not conditionToStopKMean(centroids, newCentroids):
            centroids = newCentroids
            assignedLabel = assignPointsToCentroid(points, centroids)
            newCentroids = recomputeCentroid(assignedLabel, centroids)
        
        interClusterDistance = min(
            [euclideanDistance(centroids[a], centroids[b]) for a in range(len(centroids)) for b in
             range(a + 1, len(centroids))])
        intraClusterDistance = max([euclideanDistance(point, centroid) for centroid in assignedLabel.keys() for point in
                                    assignedLabel[centroid]])
        currentDunnIndex = interClusterDistance / intraClusterDistance
        print("\t>The dunn index for iteration ", iteration, " is: ", currentDunnIndex)
        if finalDunnIndex < currentDunnIndex:
            finalDunnIndex = currentDunnIndex
            finalLabels = assignedLabel
        finalPlot(assignedLabel)
    finalPlot(finalLabels)
    statistics(finalLabels, data, giveValueToEachCentroid(finalLabels))



main()