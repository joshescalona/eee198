# below are the functions needed for the web application and algorithms.
from pqdict import PQDict
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
def dijkstra(filename, start, end):
    # store loaded object to variable
    graph = load_object(filename)
    inf = float('inf')
    shortest_distances = {start: 0}                 # mapping of nodes to their dist from start
    queue_sd = PQDict(shortest_distances)           # priority queue for tracking min shortest path
    predecessors = {}                               # mapping of nodes to their direct predecessors
    unexplored = set(graph.keys())                  # unexplored nodes
    path = []

    while unexplored:                                           # nodes yet to explore
        (minNode, minDistance) = queue_sd.popitem()             # node w/ min dist d on frontier
        shortest_distances[minNode] = minDistance               # est dijkstra greedy score
        unexplored.remove(minNode)                              # remove from unexplored
        if minNode == end: break                                # end if goal already reached

        # now consider the edges from minNode with an unexplored head -
        # we may need to update the dist of unexplored successors
        for neighbor in graph[minNode]:                               # successors to v
            if neighbor in unexplored:                          # then neighbor is a frontier node
                minDistance = shortest_distances[minNode] + graph[minNode][neighbor]
                if minDistance < queue_sd.get(neighbor, inf):
                    queue_sd[neighbor] = minDistance
                    predecessors[neighbor] = minNode                   # set/update predecessor

    currentNode = end
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessors[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0,start)
    if shortest_distances[end] != inf:
        return shortest_distances[end], path


# dijkstra with multiple end nodes and first end node to be popped will be the output
# returns shortest distance, path, and end node
def dijkstra_endlist(filename, start, passenger_nodelist):
    # for matching algorithm, goal = 'passenger_nodelist' -> this will check any node if it is a node with a passenger

    # store loaded object to variable
    graph = load_object(filename)
    inf = float('inf')
    shortest_distances = {start: 0}                 # mapping of nodes to their dist from start
    queue_sd = PQDict(shortest_distances)           # priority queue for tracking min shortest path
    predecessors = {}                               # mapping of nodes to their direct predecessors
    unexplored = set(graph.keys())                  # unexplored nodes
    path = []

    while unexplored:                                           # nodes yet to explore
        (minNode, minDistance) = queue_sd.popitem()             # node w/ min dist d on frontier
        shortest_distances[minNode] = minDistance               # est dijkstra greedy score
        unexplored.remove(minNode)                              # remove from unexplored
        if minNode in passenger_nodelist:
             match_node = minNode
             break                                              # end if goal already reached

        # now consider the edges from minNode with an unexplored head -
        # we may need to update the dist of unexplored successors
        for neighbor in graph[minNode]:                               # successors to v
            if neighbor in unexplored:                          # then neighbor is a frontier node
                minDistance = shortest_distances[minNode] + graph[minNode][neighbor]
                if minDistance < queue_sd.get(neighbor, inf):
                    queue_sd[neighbor] = minDistance
                    predecessors[neighbor] = minNode                   # set/update predecessor

    currentNode = match_node
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessors[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0,start)
    if shortest_distances[match_node] != inf:
        return shortest_distances[match_node], path, match_node

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
    start_node = start
    # incase there are no intermediate nodes
    output_node = start

    while nodes_intermediate:
        shortest_distance, temp_path, output_node = dijkstra_endlist(filename, start_node, nodes_intermediate)
        path.extend(temp_path)
        if len(nodes_intermediate) == 0:
            break
        nodes_intermediate.remove(output_node)
        start_node = output_node

    shortest_distance, temp_path, output_node = dijkstra_endlist(filename, output_node, end)
    path.extend(temp_path)

    return path

def searchbasedRS(driver_nodelist, passenger_nodelist, destination_list):

# find match, find driver, compute shortest path, check SRP
# return matched passengers, path, and price
