import matplotlib.pyplot as plot
import numpy as np

def ReadFile(file):
    dataset = []
    originalG = []
    for line in file:
        e = line.strip().split('\t')
        for i in range(len(e)):
            e[i] = float(e[i])
        originalG.append(int(e.pop(2)))
        dataset.append(e)
    return dataset, originalG


def CalculateCentroids(dsT, k):
    centroids = [[0 for i in range(len(dsT))] for j in range(k)]
    mins = []
    maxs = []
    for column in dsT:
        mins.append(min(column))
        maxs.append(max(column))
    for i in range(k):
        for j in range(len((dsT))):
            centroids[i][j] = np.round(np.random.uniform(mins[j], maxs[j]), 3)
    return centroids


def UpdateCentroids(dataset, groups, centroids):
    cont = [0 for i in range(len(centroids))]
    for i in range(len(centroids)):
        for j in range(len(centroids[i])):
            centroids[i][j] = 0
    for i in range(len(groups)):
        for j in range(len(dataset[i])):
            centroids[groups[i]][j] += dataset[i][j]
        cont[groups[i]] += 1
    for i in range(len(centroids)):
        for j in range(len(centroids[i])):
            centroids[i][j] /= cont[i]


def CalculateDistance(point, centroid):
    total = 0
    for i in range(len(point)):
        total += (point[i] - centroid[i])**2
    return total

def UpdateGroups(dataset, centroids, groups):
    change = False
    for pointIndex in range(len(dataset)):
        minimumDistance = float('+inf')
        minimumIndex = 0
        for CentroidIndex in range(len(centroids)):
            distance = CalculateDistance(dataset[pointIndex], centroids[CentroidIndex])
            if distance < minimumDistance:
                minimumDistance = distance
                minimumIndex = CentroidIndex
        if groups[pointIndex] != minimumIndex:
            change = True
            groups[pointIndex] = minimumIndex
    return change


def Graph(dsT, groups, centroids = None):
    colors = dict()
    groupcolor = [e * 50 for e in groups]
    fig, ax = plot.subplots()
    ax.scatter(dsT[0], dsT[1], c=groupcolor)
    CT = list(zip(*centroids))
    ax.scatter(CT[0], CT[1], c='red')
    plot.show()
    plot.close()


if __name__ == '__main__':
    with open('Aggregation.txt', 'r') as file:
        dataset, originalG = ReadFile(file)
    dsT = list(zip(*dataset))
    centroids = CalculateCentroids(dsT, 3)
    groups = [0 for i in dataset]
    UpdateGroups(dataset, centroids, groups)

    '''
    for i in range(100):
        changes = UpdateGroups(dataset, centroids, groups, False)
        UpdateCentroids(dataset, groups, centroids)
    '''


    changes = True
    while changes:
        UpdateCentroids(dataset, groups, centroids)
        changes = UpdateGroups(dataset, centroids, groups)
        print(changes)


    Graph(dsT, groups, centroids)