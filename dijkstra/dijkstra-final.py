# this code is an implementation of dijkstra made from scratch to be compatible
# with the adjacency list created from the OSM map data

import pickle

# load adjacency list object
def load_object(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# dijkstra function
def dijkstra(graph, start, goal):
    # for matching algorithm, goal = 'driver' -> this will check any node if it is a driver node

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
        print('Shortest distance is ' + str(shortest_distance[goal]))
        print('And the path is ' + str(path))

#######################################################################################

# store loaded object to variable
adj_list = load_object("adj_list_obj.pkl")

# graph = {'a':{'b':10,'c':3},'b':{'c':1,'d':2},'c':{'b':4,'d':8,'e':2},'d':{'e':7},'e':{'d':9}}
dijkstra(adj_list, '17216409', '5369579207')
