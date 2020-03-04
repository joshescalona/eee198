# this code is an implementation of dijkstra made from scratch to be compatible
# with the adjacency list created from the OSM map data
# returns shortest distance and path

import pickle

# load adjacency list object
def load_object(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# get row number of item in 2d List
def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return i

# dijkstra function
def dijkstra(filename, start, goal):
    # for matching algorithm, goal = 'driver' -> this will check any node if it is a driver node

    # store loaded object to variable
    graph = load_object(filename)

    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph
    infinity = float('inf')
    path = []

    # set all node distances to infinity
    for node in unseenNodes:
        shortest_distance[node] = infinity

    # set starting point distance to 0
    shortest_distance[start] = 0

    while unseenNodes:
        minNode = None

        # check node in graph with shortest distance and start there
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node

        # check if current shortest distance is greater than minNode + weight
        for childNode, weight in graph[minNode].items():
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[minNode]
                predecessor[childNode] = minNode

        unseenNodes.pop(minNode)
        # end loop if goal node is reached
        # we dont need to loop through all vertices
        if minNode == goal:
            break

    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0,start)
    if shortest_distance[goal] != infinity:

        return shortest_distance[goal], path


def get_coordinates(filename, node_list):
    # store loaded object to variable
    coordinates = []
    node_data = load_object(filename)

    for node in node_list:
        index_node = index_2d(node_data, node)
        coordinates.append([float(node_data[index_node][1]),float(node_data[index_node][2])])

    return coordinates


