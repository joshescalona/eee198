# this python script creates a list from the extracted data from OSM
# this assumes that the edge weights between each node is equal

# importing csv module
import csv
import pandas as pd

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
    #way_nodelist = list(map(int, way_nodelist))

    for index, node in enumerate(way_nodelist):
        addValue = []
        # way is not oneway
        if "oneway" not in row[3]:
            # check if first node
            if index == 0:
                addValue = way_nodelist[index+1]

            # check if last node
            elif index == len(way_nodelist)-1:
                addValue = way_nodelist[index-1]

            # add both neighbors if not end nodes
            else:
                 addValue = [way_nodelist[index-1], way_nodelist[index+1]]

        # way is oneway
        else:
            # check if not last node
            if index != len(way_nodelist)-1:
                # get next value since ordered list -> adjacent vertex
                addValue = way_nodelist[index+1]

        # create new if node does not exist in list yet
        if node not in adj_list and addValue:
            adj_list[node] = []
            adj_list[node].append(addValue)

        else:
            # checks if addValue is a list for iteration of adjacent nodes
            if isinstance(addValue, list):
                for value in addValue:
                    if value not in adj_list[node]:
                        adj_list[node].append(value)

            else:
                # checks if adj_list[node] is already a list for iteration of nodes
                if isinstance(adj_list[node], list):
                    if addValue not in adj_list[node]:
                        adj_list[node].append(addValue)
                else:
                    if addValue != adj_list[node]:
                        adj_list[node].append(addValue)

# converts adjacency list to csv file (horizontal mode)
with open('mycsvfile.csv', 'w') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, adj_list.keys())
    w.writeheader()
    w.writerow(adj_list)

# from horizontal to vertical (transpose of csv file)
pd.read_csv('mycsvfile.csv', header=None).T.to_csv('adj-list.csv', header=False, index=False)
