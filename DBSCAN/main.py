import queue

# Define label for differnt point group
NOISE = 0
UNASSIGNED = 0
core = -1
edge = -2


# function to find all neigbor points in radius
def neighbor_points(data, pointId, radius):
    points = []
    for i in range(len(data)):
        # Euclidian square distance
        dist = (data[i][0] - data[pointId][0])*(data[i][0] - data[pointId][0]) + \
            (data[i][1] - data[pointId][1])*(data[i][1] - data[pointId][1])
        if dist <= radius:
            points.append(i)
    return points

# DB Scan algorithom


def dbscan(data, Eps, MinPt):
    # initialize all points as unassigned
    pointlabel = [UNASSIGNED] * len(data)
    pointcount = []
    # initialize list for core/noncore point
    corepoint = []
    noncore = []

    # Find all neighbour for all point
    for i in range(len(data)):
        pointcount.append(neighbor_points(data, i, Eps))

    # Find all core point, edgepoint and noise
    for i in range(len(pointcount)):
        if (len(pointcount[i]) >= MinPt):
            pointlabel[i] = core
            corepoint.append(i)
        else:
            noncore.append(i)

    for i in noncore:
        for j in pointcount[i]:
            if j in corepoint:
                pointlabel[i] = edge

                break

    # start assigning point to cluster
    cl = 1

    # Using a Queue to put all neigbour core point in queue and find neigbour's neigbour
    visited = [0] * len(data)

    for i in range(len(pointlabel)):
        if (visited[i] == 0):
            q = queue.Queue()
            if (pointlabel[i] == core):
                pointlabel[i] = cl
                visited[i] = 1
                for x in pointcount[i]:
                    if(pointlabel[x] == core):
                        q.put(x)
                        pointlabel[x] = cl
                        visited[x] = 1
                    elif(pointlabel[x] == edge):
                        pointlabel[x] = cl
                        visited[x] = 1
                # Stop when all point in Queue has been checked
                while not q.empty():
                    neighbors = pointcount[q.get()]
                    for y in neighbors:
                        if (visited[y] == 0):
                            if (pointlabel[y] == core):
                                pointlabel[y] = cl
                                q.put(y)
                                visited[y] = 1
                            if (pointlabel[y] == edge):
                                pointlabel[y] = cl
                                visited[y] = 1
                cl = cl+1  # move to next cluster

    return pointlabel, cl


def main():
    # Set EPS and Minpoint
    epss = [0.4, 3]
    minptss = [2, 4]
    data = [(1, 2), (3, 4), (2.5, 4), (1.5, 2.5), (3, 5), (2.8, 4.5), (2.5, 4.5), (1.2, 2.5), (1, 3),
            (1, 5), (1, 2.5), (5, 6), (4, 3), (100, 100), (100.4, 100.7), (101, 103), (101.1, 100.67)]
    # Find All cluster, outliers in different setting and print results
    print("-------------------------------------------------")
    for eps in epss:
        for minpts in minptss:
            print('WHEN eps = ' + str(eps) + ' and Minpoints = '+str(minpts))
            pointlabel, cl = dbscan(data, eps, minpts)
            print('Number of clusters found: ' + str(cl-1))

            for i in range(1, cl):
                print("\nCluster: " + str(i))
                for j in range(len(pointlabel)):
                    if(pointlabel[j] == i):
                        print(data[j])

            outliers = pointlabel.count(0)
            print('\nNumber of outliers found: '+str(outliers))
            for i in range(len(pointlabel)):
                if(pointlabel[i] == 0):
                    print(data[i])
            print("-------------------------------------------------")


if __name__ == "__main__":
    main()
