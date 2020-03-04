# below are the functions needed for the web application and algorithms.

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
# returns shortest distance and path
def dijkstra(filename, start, goal):
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


# dijkstra with multiple end nodes and first end node to be popped will be the output
# returns shortest distance, path, and end node
def dijkstra_endlist(filename, start, passenger_nodelist):
    # for matching algorithm, goal = 'passenger_nodelist' -> this will check any node if it is a node with a passenger

    # store loaded object to variable
    graph = load_object(filename)

    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph
    infinity = float('inf')
    path = []
    match_node = 0

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
        if minNode in passenger_nodelist:
            match_node = minNode
            break

    currentNode = match_node
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0,start)
    if shortest_distance[match_node] != infinity:

        return shortest_distance[match_node], path, match_node


# given a list of nodes, get its corresponding coordinates and return the list
def get_coordinates(filename, node_list):
    # store loaded object to variable
    coordinates = []
    node_data = load_object(filename)

    for node in node_list:
        index_node = index_2d(node_data, node)
        coordinates.append([float(node_data[index_node][1]),float(node_data[index_node][2])])

    return coordinates


# given multiple nodes with a defined start and end, find the shortest path between the nodes and return the path
def shortestpath(filename, start, intermediate_list, end):
    nodes_intermediate = intermediate_list
    path = []
    output_node = start

    while nodes_intermediate:
        shortest_distance, temp_path, output_node = dijkstra_endlist(filename, start, nodes_intermediate)
        path.extend(temp_path)
        if len(nodes_intermediate) == 0:
            break
        nodes_intermediate.remove(output_node)

    shortest_distance, temp_path, output_node = dijkstra_endlist(filename, output_node, end)
    path.extend(temp_path)

    print(path)

    return path
