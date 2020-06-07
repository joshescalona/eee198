# below are the functions needed for the web application and algorithms.
from pqdict import PQDict
import pickle
import multiprocessing
import sys
import math, cmath


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
    match_node = 0
    inf = float('inf')
    shortest_distances = {start: 0}                 # mapping of nodes to their dist from start
    queue_sd = PQDict(shortest_distances)           # priority queue for tracking min shortest path
    predecessors = {}                               # mapping of nodes to their direct predecessors
    unexplored = set(graph.keys())                  # unexplored nodes
    path = []

    while unexplored:                                           # nodes yet to explore
        try:
          (minNode, minDistance) = queue_sd.popitem()             # node w/ min dist d on frontier
        except KeyError:
          print('Path not reachable')
          return None, None, None
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
    nodes_intermediate = intermediate_list.copy()
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
        if (shortest_distance == None):
            path = None
            break
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
    if (path == None):
        return None, None, None
    else:
        return path, total_distance, output_node

# compute the price for a certain passenger given srp and route distance
def compute_timenprice(route_distance, srp):
    # fare = 40 + distance*13.50*SRP + time*2*SRP
    # compute time (assume 19.30 kph speed and no traffic) in minutes
    # source https://www.manilatimes.net/2019/10/11/supplements/no-end-in-sight-for-metro-manila-traffic/629952/
    route_time = (route_distance/19.30)*60
    fare = 40 + route_distance*13.50*srp + route_time*2*srp
    return route_time, fare

# dijkstra based method from source
def searchbasedRS_source(filename, passenger_source, passenger_others, destination_others, return_dict):
    shortest_distance, temp_path, passenger_match = dijkstra_endlist(filename, passenger_source, passenger_others)
    if passenger_match == None:
        return_dict[1] = None
        return_dict[2] = None
    else:
        index = passenger_others.index(passenger_match)
        destination_match = destination_others[index]
        return_dict[1] = passenger_match
        return_dict[2] = destination_match

# dijkstra based method from destinations
def searchbasedRS_destination(filename, passenger_others, destination_source, destination_others, return_dict):
    shortest_distance, temp_path, destination_match = dijkstra_endlist(filename, destination_source, destination_others)
    if destination_match == None:
        return_dict[1] = None
        return_dict[2] = None
    else:
        index = destination_others.index(destination_match)
        passenger_match = passenger_others[index]
        return_dict[1] = passenger_match
        return_dict[2] = destination_match

# this algorithm assumes the first item in passenger_nodelist and destination_list is the source
def searchbasedRS(filename, driver_nodelist, passenger_nodelist, destination_list, srp_min):
    passenger_source = passenger_nodelist[0]
    passenger_others = passenger_nodelist.copy()
    passenger_others.pop(0)
    destination_source = destination_list[0]
    destination_others = destination_list.copy()
    destination_others.pop(0)
    drivers = driver_nodelist.copy()

    # starting the multiprocess for dijkstra on both source and destination
    manager = multiprocessing.Manager()
    # initializing a shared variable
    return_dict = manager.dict()

    sources = [passenger_source]
    destinations = [destination_source]
    #loop for at most 3 matches
    for i in range(2):
        # loop while srp requirement not met
        viable_match = 0
        if not passenger_others or not destination_others:
                break
        srp_list_temp = []
        while not viable_match:
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
            if return_dict[1] == None:
                print('\nPath not reachable!\n')
                return None, None, None
            passenger_match = return_dict[1]
            destination_match = return_dict[2]


            # finding closest driver
            shortest_distance, temp_path, driver_match = dijkstra_endlist(filename, passenger_source, driver_nodelist)
            if shortest_distance == None:
                print('\nPath not reachable!\n')
                return None, None, None

            # find shortest path from driver to all sources
            sources.append(passenger_match)
            path_temp, route_distance, end_node = shortestpath(filename, driver_match, sources)
            if path_temp == None:
                print('\nPath not reachable!\n')
                return None, None, None

            # find shortest path from end node in sources to destinations
            destinations.append(destination_match)
            path_destination, route_distance_destination, end_node = shortestpath(filename, end_node, destinations)
            if path_destination == None:
                print('\nPath not reachable!\n')
                return None, None, None
            path_destination.pop(0)     #removing first item since duplicate in last item from path

            # getting total path and total route distance
            path_temp.extend(path_destination)
            route_distance = route_distance + route_distance_destination

            # getting path and path distance if no ride sharing occured for all passengers for SRP computation
            for i in range(len(sources)):
                withoutrs_distance, temp_path = dijkstra(filename, driver_match, sources[i])
                withoutrs_distance_2, temp_path = dijkstra(filename, sources[i], end_node)          # distance calculated is until the end of total shared distance
                withoutrs_distance = withoutrs_distance + withoutrs_distance_2
                srp = withoutrs_distance/route_distance
                srp_list_temp.append(srp)

            # removes other passengers if done
            passenger_others.remove(passenger_match)
            destination_others.remove(destination_match)

            viable_match = 1
            i = 0
            while i < len(srp_list_temp):
                if srp_list_temp[i] < srp_min:
                    viable_match = 0
                    # pop the latest and find another match
                    sources.pop(len(srp_list_temp)-1)
                    destinations.pop(len(srp_list_temp)-1)
                    srp_list_temp.clear()
                    path_temp.clear()
                i += 1
            if path_temp:
                path = path_temp.copy()
                srp_list = srp_list_temp.copy()

            # end if there are no other passengers
            if not passenger_others or not destination_others:
                break

    if len(sources) == 1:
        print('\nCannot find you a match at this time!\n')
        return None, None, None

    else:
        f = open("searchbased_results.txt", "a")
        print('\nMatched passengers:')
        print(sources)
        print('\nCorresponding destinations:')
        print(destinations)
        print('\nAssigned driver:')
        print(driver_match)
        print('\nPath taken:')
        print(path)
        print('\nRoute length: ' + str(route_distance) + 'km')
        f.write('Route distance: ' + str(route_distance) + '\n')
        route_time, fare = compute_timenprice(route_distance, srp_list[0])
        print('\nApproximate route time: %.2f minutes' % route_time)
        f.write('Route time: ' + str(route_time) + '\n')
        f.write('Number of passengers: ' + str(len(sources))+'\n')
        print('\nPrice of trip: Php %.2f' % fare)
        f.write('Fare: ' + str(fare) + '\n')
        print('\nSRPs:' + str(srp_list))
        for srp in srp_list:
            f.write('SRPs: ' + str(srp) + '\n')
        return sources, destinations, path
        f.close()

# this function gets the largest angle that includes all the nodes given a center and peripheral nodes
def get_largest_angle(center, peripheral):
    peripheral_radius = [complex(z[0]-center[0], z[1]-center[1]) for z in peripheral]
    peripheral_angle = [cmath.phase(z) for z in peripheral_radius]                     #in radians [-pi to pi]

    # converting all to positive [0, 2pi] instead of [-pi, pi]
    i = 0
    while i < len(peripheral_angle):
        if peripheral_angle[i] < 0:
            peripheral_angle[i] = peripheral_angle[i] + 2*(math.pi)
        peripheral_angle[i] = math.degrees(peripheral_angle[i])
        i += 1

    peripheral_angle.sort()
    # getting difference between adjacent angles
    diff_adjacent = []
    i = 0
    while i < len(peripheral_angle):
        if i == len(peripheral_angle) - 1:
            adj_diff = 360 - peripheral_angle[i] + peripheral_angle[0]
        else:
            adj_diff = peripheral_angle[i+1] - peripheral_angle[i]
        diff_adjacent.append(adj_diff)
        i += 1

    # print(peripheral_angle)
    # print(diff_adjacent)
    # max angle is the opposite angle of the largest angle difference between adjacent
    max_angle = 360 - max(diff_adjacent)

    return max_angle           #in degrees

# this function is the implementation of the GrabShare algorithm
def grab_share(filename, driver_nodelist, passenger_nodelist, destination_list, angle_max):
    passenger_source = passenger_nodelist[0]
    passenger_others = passenger_nodelist.copy()
    passenger_others.pop(0)
    destination_source = destination_list[0]
    destination_others = destination_list.copy()
    destination_others.pop(0)
    drivers = driver_nodelist.copy()

    sources = [passenger_source]
    destinations = [destination_source]

    # for matching with angle
    center = [passenger_source]
    center_coordinates = get_coordinates('nodes_coordinates.pkl', center)
    peripheral = []
    srp_list = []

    angle = 0
    # look for 2 matches
    i = 0
    while i < len(passenger_others):
        peripheral.extend([passenger_others[i], destination_others[i]])
        peripheral.append(destination_source)
        peripheral_coordinates = get_coordinates('nodes_coordinates.pkl', peripheral)
        angle = get_largest_angle(center_coordinates[0], peripheral_coordinates)
        if angle <= angle_max:
            break
        peripheral.clear()
        i += 1

    # look for 3rd match
    j = 0
    angle_2 = 0
    while j < len(passenger_others):
        if i == j:
            j += 1
            continue
        peripheral.extend([passenger_others[j], destination_others[j]])
        peripheral_coordinates = get_coordinates('nodes_coordinates.pkl', peripheral)
        angle_2 = get_largest_angle(center_coordinates[0], peripheral_coordinates)
        if angle_2 <= angle_max:
            break
        peripheral.remove(passenger_others[j])
        peripheral.remove(destination_others[j])
        j += 1

    if angle_2 <= angle_max:
        angle = angle_2

    if angle > angle_max:
        print('\nCannot find you a match at this time!\n')
        return None, None, None

    else:
        # assign the matched passenger sources and destinations
        if len(peripheral) == 3:    # 1 match only
            sources.extend([peripheral[0]])
            destinations.extend([peripheral[1]])

        if len(peripheral) == 5:    # 2 matches only
            sources.extend([peripheral[0], peripheral[3]])
            destinations.extend([peripheral[1], peripheral[4]])

        print(peripheral)
        print(sources)
        print(destinations)
        # finding closest driver
        shortest_distance, temp_path, driver_match = dijkstra_endlist(filename, passenger_source, driver_nodelist)
        if shortest_distance == None:
            print('\nPath not reachable!\n')
            return None, None, None

        # find shortest path from driver to all sources
        path, route_distance, end_node = shortestpath(filename, driver_match, sources)
        if path == None:
            print('\nPath not reachable!\n')
            return None, None, None

        # find shortest path from end node in sources to destinations
        path_destination, route_distance_destination, end_node = shortestpath(filename, end_node, destinations)
        if path_destination == None:
            print('\nPath not reachable!\n')
            return None, None, None
        path_destination.pop(0)     #removing first item since duplicate in last item from path

        # getting total path and total route distance
        path.extend(path_destination)
        route_distance = route_distance + route_distance_destination

        # getting path and path distance if no ride sharing occured for all passengers for SRP computation
        for i in range(len(sources)):
            withoutrs_distance, temp_path = dijkstra(filename, driver_match, sources[i])
            withoutrs_distance_2, temp_path = dijkstra(filename, sources[i], end_node)          # distance calculated is until the end of total shared distance
            withoutrs_distance = withoutrs_distance + withoutrs_distance_2
            srp = withoutrs_distance/route_distance
            srp_list.append(srp)

        f = open("grabshare_results.txt", "a")
        print('\nMatched passengers:')
        print(sources)
        print('\nCorresponding destinations:')
        print(destinations)
        print('\nAssigned driver:')
        print(driver_match)
        print('\nPath taken:')
        print(path)
        print('\nRoute length: ' + str(route_distance) + 'km')
        route_time, fare = compute_timenprice(route_distance, srp_list[0])
        print('\nApproximate route time: %.2f minutes' % route_time)
        print('\nPrice of trip: Php %.2f' % fare)
        print('\nSRPs:' + str(srp_list))
        print('\nAngle: ' + str(angle))
        f.write('Route distance: ' + str(route_distance) + '\n')
        f.write('Route time: ' + str(route_time) + '\n')
        f.write('Number of passengers: ' + str(len(sources))+'\n')
        f.write('Fare: ' + str(fare) + '\n')
        for srp in srp_list:
            f.write('SRPs: ' + str(srp) + '\n')
        f.write('Angle: ' + str(angle) + '\n')
        f.close()
        return sources, destinations, path


