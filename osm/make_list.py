# this python script creates a list from the extracted data from OSM
# the list contains adjacent nodes and respective distances between nodes

import pickle
import os
import csv
import pandas as pd
from math import sin, cos, sqrt, atan2, radians

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

# def load_object(filename):
#     with open(filename, 'rb') as f:
#         return pickle.load(f)

def get_node_distance(node1, node2, nodelist):
    # approximate radius of earth in km
    r_earth = 6373.0

    # get latitude and longitude of node from dataset
    breaker = 0
    for index, node in enumerate(nodelist):
        if node1 in node:
            lat1 = radians(float(nodelist[index][5]))
            lon1 = radians(float(nodelist[index][6]))
            breaker += 1

        if node2 in node:
            lat2 = radians(float(nodelist[index][5]))
            lon2 = radians(float(nodelist[index][6]))
            breaker += 1

        if breaker == 2:
            break

    # compute distance via formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r_earth * c

    return distance

# csv file name
file_node = "out_node.csv"
file_way = "out_way.csv"

# initializing the titles and rows list
# rows variables are the data we actually need
fields_node = []
rows_node = []
fields_way = []
rows_way = []

# reading csv file
with open(file_node, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields_node = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows_node.append(row)

# reading csv file
with open(file_way, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields_way = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows_way.append(row)


# making the adjacency list
adj_list = {}
# read each way
for row_num, row in enumerate(rows_way):
    # parse the nodes first of the way
    temp_nodelist = row[5].replace('[','')
    temp_nodelist = temp_nodelist.replace(']','')
    way_nodelist = temp_nodelist.split(',')
    # way_nodelist = list(map(int, way_nodelist))

    for index, node in enumerate(way_nodelist):
        addValue = {}
        addValueplus = {}
        addValueminus = {}
        two_value = 0
        # way is not oneway
        if "oneway" not in row[3]:
            # check if first node
            if index == 0:
                #get latitude and longitude of nodes
                node_distance = get_node_distance(way_nodelist[index], way_nodelist[index+1], rows_node)
                addValue[way_nodelist[index+1]] = node_distance

            # check if last node
            elif index == len(way_nodelist)-1:
                node_distance = get_node_distance(way_nodelist[index], way_nodelist[index-1], rows_node)
                addValue[way_nodelist[index-1]] = node_distance

            # add both neighbors if not end nodes
            else:
                node_distanceminus = get_node_distance(way_nodelist[index], way_nodelist[index-1], rows_node)
                node_distanceplus = get_node_distance(way_nodelist[index], way_nodelist[index+1], rows_node)
                addValueminus[way_nodelist[index-1]] = node_distanceminus
                addValueplus[way_nodelist[index+1]] = node_distanceplus
                two_value = 1

        # way is oneway
        else:
            # check if not last node
            if index != len(way_nodelist)-1:
                # get next value since ordered list -> adjacent vertex
                node_distance = get_node_distance(way_nodelist[index], way_nodelist[index+1], rows_node)
                addValue[way_nodelist[index+1]] = node_distance

        # create new if node does not exist in list yet
        if node not in adj_list:
            # adj_list[node] = []
            # adj_list[node].append(addValue)
            if two_value == 0:
                add_list = {node: addValue}
                adj_list.update(add_list)
            elif two_value == 1:
                add_list[node] = addValueminus
                add_list[node].update(addValueplus)
                adj_list.update(add_list)

        else:
            # check if nodes in addValue is already in the adj_list
            if two_value == 0:
                if frozenset(addValue.keys()) not in adj_list[node]:
                    adj_list[node].update(addValue)

            elif two_value == 1:
                if frozenset(addValueminus.keys()) not in adj_list[node]:
                    adj_list[node].update(addValueminus)
                if frozenset(addValueplus.keys()) not in adj_list[node]:
                    adj_list[node].update(addValueplus)


# converts adjacency list to csv file (horizontal mode)
with open('mycsvfile.csv', 'w') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, adj_list.keys())
    w.writeheader()
    w.writerow(adj_list)

# from horizontal to vertical (transpose of csv file)
pd.read_csv('mycsvfile.csv', header=None).T.to_csv('adj-list.csv', header=False, index=False)

# save object adj_list
save_object(adj_list, "adj_list_obj.pkl")

# store loaded object to variable
# adj_list = load_object("adj_list_obj.pkl")
# print(adj_list)

