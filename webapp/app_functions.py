# below are the functions needed for the web application and algorithms.
from pqdict import PQDict
import pickle
import multiprocessing
import sys


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


# given multiple nodes with a defined start, find the shortest path between the nodes and return the path, distance, and end node
def shortestpath(filename, start, intermediate_list):
    nodes_intermediate = intermediate_list
    path = []
    start_node = start
    # incase there are no intermediate nodes
    output_node = start
    total_distance = 0

    # print('\n\nStart node:')
    # print(start)
    # print('\nIntermediate nodes:')
    # print(intermediate_list)

    while nodes_intermediate:
        shortest_distance, temp_path, output_node = dijkstra_endlist(filename, start_node, nodes_intermediate)
        path.extend(temp_path)
        # if len(nodes_intermediate) == 0:
        #     break
        nodes_intermediate.remove(output_node)
        start_node = output_node
        total_distance = total_distance + shortest_distance

    # print('\nEnd node: ')
    # print(output_node)
    # shortest_distance, temp_path, output_node = dijkstra_endlist(filename, output_node, end)
    # path.extend(temp_path)
    # total_distance = total_distance + shortest_distance

    # print('\nPath taken:')
    # print(path)
    # print('\nRoute length: ' + str(total_distance) + 'km\n')
    return path, total_distance, output_node

# dijkstra based method from source
def searchbasedRS_source(filename, passenger_source, passenger_others, destination_others, return_dict):
    shortest_distance, temp_path, passenger_match = dijkstra_endlist(filename, passenger_source, passenger_others)
    index = passenger_others.index(passenger_match)
    destination_match = destination_others[index]
    return_dict[1] = passenger_match
    return_dict[2] = destination_match

# dijkstra based method from destinations
def searchbasedRS_destination(filename, passenger_others, destination_source, destination_others, return_dict):
    shortest_distance, temp_path, destination_match = dijkstra_endlist(filename, destination_source, destination_others)
    index = destination_others.index(destination_match)
    passenger_match = passenger_others[index]
    return_dict[1] = passenger_match
    return_dict[2] = destination_match

# this algorithm assumes the first item in passenger_nodelist and destination_list is the source
def searchbasedRS(filename, driver_nodelist, passenger_nodelist, destination_list, srp_min):
    srp = 0
    passenger_source = passenger_nodelist[0]
    passenger_others = passenger_nodelist
    passenger_others.pop(0)
    destination_source = destination_list[0]
    destination_others = destination_list
    destination_others.pop(0)
    drivers = driver_nodelist

    # starting the multiprocess for dijkstra on both source and destination
    manager = multiprocessing.Manager()
    # initializing a shared variable
    return_dict = manager.dict()

    # loop while srp requirement not met
    while srp < srp_min:
        # end if there are no other passengers
        if not passenger_others:
            break

        # start the two processes
        source_process = multiprocessing.Process(target = searchbasedRS_source, args=(filename, passenger_source, passenger_others, destination_others, return_dict))
        source_process.start()
        destination_process = multiprocessing.Process(target = searchbasedRS_destination, args=(filename, passenger_others, destination_source, destination_others, return_dict))
        destination_process.start()

        # end the other process if match is found on a process
        while True:
            if source_process.is_alive() == 0:
                print('\nMatch found from source!')
                destination_process.terminate()
                break
            if destination_process.is_alive() == 0:
                print('\nMatch found from destination!')
                source_process.terminate()
                break

        # assign the matched passenger source and destination
        passenger_match = return_dict[1]
        destination_match = return_dict[2]

        # finding closest driver
        shortest_distance, temp_path, driver_match = dijkstra_endlist(filename, passenger_source, driver_nodelist)

        # find shortest path from driver to all sources
        sources = []
        sources.extend((passenger_source, passenger_match))
        path, route_distance, end_node = shortestpath(filename, driver_match, sources)
        sources.extend((passenger_source, passenger_match))             # need to reassign sources because it gets erased after the line above(?)

        # find shortest path from end node in sources to destinations
        destinations = []
        destinations.extend((destination_source, destination_match))
        path_destination, route_distance_destination, end_node = shortestpath(filename, end_node, destinations)
        path_destination.pop(0)     #removing first item since duplicate in last item from path
        destinations.extend((destination_source, destination_match))

        # getting total path and total route distance
        path.extend(path_destination)
        route_distance = route_distance + route_distance_destination

        # getting path and path distance if no ride sharing occured for SRP computation
        source_passenger = [passenger_source, destination_source]
        withoutrs_distance, temp_path = dijkstra(filename, driver_match, passenger_source)
        withoutrs_distance_2, temp_path = dijkstra(filename, passenger_source, destination_source)
        withoutrs_distance = withoutrs_distance + withoutrs_distance_2

        # removes other passengers if done
        passenger_others.remove(passenger_match)
        destination_others.remove(destination_match)
        srp = withoutrs_distance/route_distance

        print('\nMatched passengers:')
        print(sources)
        print('\nAssigned driver:')
        print(driver_match)
        print('\nPath taken:')
        print(path)
        print('\nRoute length: ' + str(route_distance) + 'km')
        print('\nRoute length without ride sharing: ' + str(withoutrs_distance) + 'km')
        print('\nSRP:' + str(srp) + '\n')

    if srp < srp_min:
        print('\nCannot find you a match at this time!\n')
        return None, None, None, None

    else:
        return sources, destinations, path, route_distance
