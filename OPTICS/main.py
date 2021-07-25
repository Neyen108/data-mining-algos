import math

# function to identify core points and return adjacency list with neighbours lying within epsilon radius


def is_core_point(input_list, visited, no_inputs, epsilon, min_points):
    i = 0
    adjacency_mat = dict()

    for i in range(no_inputs):
        count = 0
        nbd_list = []
        for j in range(no_inputs):
            if(abs(input_list[i][0]-input_list[j][0]) <= epsilon and abs(input_list[i][1]-input_list[j][1]) <= epsilon):
                count = count+1
                if(j != i):
                    nbd_list.append(j)
        if(count >= min_points):
            visited[i] = 1
            adjacency_mat[i] = nbd_list
        i = i+1
    return adjacency_mat

# function to calculate the core distance of each core point


def find_core_distance(input_list, adjacency_matrix, min_points):
    core_distance = dict()
    for key, val in adjacency_matrix.items():
        list_distance = []
        for i in val:
            distance = math.sqrt(
                (input_list[i][1]-input_list[key][1])**2+(input_list[i][0]-input_list[key][0])**2)
            list_distance.append(distance)
        list_distance.sort()
        core_distance[key] = list_distance[min_points-1]
    return core_distance

# function to calculate the reachability diatance of each neighbour


def find_reachability_distance(adjacency_mat, core_distance, input_list):
    reachability_distance = dict()
    for key, val in adjacency_mat.items():
        temp = dict()
        for i in val:
            distance = math.sqrt(
                (input_list[i][1]-input_list[key][1])**2+(input_list[i][0]-input_list[key][0])**2)
            if(distance < core_distance[key]):
                distance = core_distance[key]
            temp[i] = distance
        reachability_distance[key] = temp
    return reachability_distance

# main function


def main():
    no_inputs = int(input("How many inputs:"))
    epsilon = int(input("Input the radius:"))
    min_points = int(input("Input the minimum points in a circle:"))
    input_list = []
    visited = [0] * no_inputs
    print("Give Input:")
    for _i in range(no_inputs):
        x = float(input("X:"))
        y = float(input("Y:"))
        input_list.append((x, y))

    adjacency_mat = is_core_point(
        input_list, visited, no_inputs, epsilon, min_points)
    core_distance = find_core_distance(input_list, adjacency_mat, min_points)
    reachability_distance = find_reachability_distance(
        adjacency_mat, core_distance, input_list)
    print("\nThe Core points with id's are:")
    for key in adjacency_mat.keys():
        print(key, ":", input_list[key])
    print("\nNeighbours for each core point id's are:")
    for key in adjacency_mat.keys():
        print(key, ":", adjacency_mat[key])
    print("\nThe core distance for each core point id's are:")
    for key in core_distance.keys():
        print(key, ":", core_distance[key])
    print("\nThe reachability distance of each neighbour point id with every core point id's are:")
    for key in reachability_distance.keys():
        print(key, ":", reachability_distance[key])


if __name__ == "__main__":
    main()
