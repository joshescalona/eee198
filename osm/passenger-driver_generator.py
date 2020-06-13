# this python script randomly generates a list of nodes to represent passenger source and destination
# and also driver location
# also outputs the generated data as an object

import pickle
import os
import pandas as pd
import random
import math
from math import sin, cos, sqrt, atan2, radians

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_object(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# get row number of item in 2d List
def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return i

# given a list of nodes, get its corresponding coordinates and return the list
def get_coordinates(filename, node_list):
    # store loaded object to variable
    coordinates = []
    node_data = load_object(filename)

    for node in node_list:
        index_node = index_2d(node_data, node)
        coordinates.append([float(node_data[index_node][1]),float(node_data[index_node][2])])

    return coordinates

# this gets the random parameters for the cases (random number of passengers and drivers and random locations clumped up vs scattered)
def get_random_parameters():
    max_passengers = 100
    max_drivers = 30
    # max_passengers = 300
    # max_drivers = 100
    # generation of passenger source and destination and drivers
    rand_pass_no = random.randint(3,max_passengers)
    # print('\nNumber of passengers: %d' % rand_pass_no)
    rand_dri_no = random.randint(1,max_drivers)
    # print('\nNumber of drivers: %d' % rand_dri_no)
    # get the minimum radius allowable for passengers and drivers
    # ratio between actual and max times the maximum radius
    # this is to prevent overcrowding when there is a large number of passengers/drivers
    min_pass_radius = math.floor(rand_pass_no/(max_passengers) * 3000)
    min_dri_radius = math.floor(rand_dri_no/(max_drivers) * 3000)
    rand_pass_radius = random.randint(min_pass_radius,3000)
    # print('\nArea radius for passengers: %d' % rand_pass_radius)
    rand_dri_radius = random.randint(min_dri_radius,3000)
    # print('\nArea radius for drivers: %d' % rand_dri_radius)

    return rand_pass_no, rand_dri_no, rand_pass_radius, rand_dri_radius

def check_radius(source_node, check_node, maximum_radius):
    # approximate radius of earth in m
    r_earth = 6373 * 1000
    source_node_0 = []
    source_node_0.append(source_node[0])
    source_coordinates = get_coordinates('nodes_coordinates.pkl', source_node_0)
    check_coordinates = get_coordinates('nodes_coordinates.pkl', check_node)

    lat1 = radians(float(source_coordinates[0][0]))
    lon1 = radians(float(source_coordinates[0][1]))
    lat2 = radians(float(check_coordinates[0][0]))
    lon2 = radians(float(check_coordinates[0][1]))
    # compute distance via formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r_earth * c

    if distance <= maximum_radius:
        return 1
    else:
        return 0

# loading the dataset
adj_list = load_object('adj_list_obj.pkl')

# initializing data to be generated
passenger_sources = []
passenger_destinations =[]
driver_locations = []
rand_pass_radii = []
rand_dri_radii = []

# loop through multiple times to get suficient data
number_of_cases = 300
print('Randomly generating passengers and drivers..')
print('Number of cases: %d' % number_of_cases)
i = 0
while i < number_of_cases:
    sources_list = []
    destinations_list = []
    drivers_list = []
    sources_list.append(random.choice(list(adj_list)))
    destinations_list.append(random.choice(list(adj_list)))
    drivers_list.append(random.choice(list(adj_list)))

    rand_pass_no, rand_dri_no, rand_pass_radius, rand_dri_radius = get_random_parameters()

    rand_pass_radii.append(rand_pass_radius)
    rand_dri_radii.append(rand_dri_radius)

    # passenger sources
    j = 0
    while j < rand_pass_no-1:
        temp_node = []
        temp_node.append(random.choice(list(adj_list)))
        if check_radius(sources_list, temp_node, rand_pass_radius) == 1:
            sources_list.extend(temp_node)
            j += 1

    # passenger destinations
    j = 0
    while j < rand_pass_no-1:
        temp_node = []
        temp_node.append(random.choice(list(adj_list)))
        if check_radius(destinations_list, temp_node, rand_pass_radius) == 1:
            destinations_list.extend(temp_node)
            j += 1

    # drivers
    j = 0
    while j < rand_dri_no-1:
        temp_node = []
        temp_node.append(random.choice(list(adj_list)))
        if check_radius(sources_list, temp_node, rand_dri_radius) == 1:
            drivers_list.extend(temp_node)
            j += 1

    passenger_sources.append(sources_list)
    passenger_destinations.append(destinations_list)
    driver_locations.append( drivers_list)
    print('Case number: %d' % (i+1) + ' done')
    i += 1


save_object(passenger_sources, "passenger_sources.pkl")
save_object(passenger_destinations, "passenger_destinations.pkl")
save_object(driver_locations, "driver_locations.pkl")
save_object(rand_pass_radii, "rand_pass_radii.pkl")
save_object(rand_dri_radii, "rand_dri_radii.pkl")

