# this code extracts the needed data from an OSM XML file
# outputs are node and way data converted into a .csv format

import osmium as osm
import pandas as pd

class nodeHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []

    def tag_inventory(self, elem, elem_type):
        if len(elem.tags)==0:
            self.osm_data.append([elem_type,
                                   elem.id,
                                   0,
                                   '',
                                   '',
                                   elem.location.lat,
                                   elem.location.lon])

        else:
            key = []
            value = []
            for tag in elem.tags:
                key.append(tag.k)
                value.append(tag.v)

            self.osm_data.append([elem_type,
                                    elem.id,
                                    len(elem.tags),
                                    key,
                                    value,
                                    elem.location.lat,
                                    elem.location.lon])


    def node(self, n):
        self.tag_inventory(n, "node")


class wayHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []

    def tag_inventory(self, elem, elem_type):
        if len(elem.tags)==0:
            self.osm_data.append([elem_type,
                                   elem.id,
                                    0,
                                    '',
                                    '',
                                   elem.nodes])

        else:
            key = []
            value = []
            for tag in elem.tags:
                # this if statement removes all oneway='no' tags (assume two way if no tag)
                if tag.k == 'oneway' and tag.v == 'no':
                  continue
                key.append(tag.k)
                value.append(tag.v)

            self.osm_data.append([elem_type,
                                    elem.id,
                                    len(elem.tags),
                                    key,
                                    value,
                                    elem.nodes])

    def way(self, w):
        self.tag_inventory(w, "way")


## relation handler not needed at the moment ##
# class relationHandler(osm.SimpleHandler):
#     def __init__(self):
#         osm.SimpleHandler.__init__(self)
#         self.osm_data = []

#     def tag_inventory(self, elem, elem_type):
#         for tag in elem.tags:
#             self.osm_data.append([elem_type,
#                                    elem.id,
#                                    len(elem.tags),
#                                    tag.k,
#                                    tag.v])

#     def relation(self, r):
#         self.tag_inventory(r, "relation")


#get all the nodes and information needed
node_handler = nodeHandler()
# scan the input file and fills the handler list accordingly
node_handler.apply_file("up-diliman.osm")

# transform the list into a pandas DataFrame
data_colnames = ['type', 'id', 'ntags', 'tagkey', 'tagvalue','lat','lon']
df_osm = pd.DataFrame(node_handler.osm_data, columns=data_colnames)
#convert pandas DataFrame to .csv file
df_osm.to_csv('out_node.csv', encoding='utf-8', index=False)

#get all the way data and information needed
way_handler = wayHandler()
# scan the input file and fills the handler list accordingly
way_handler.apply_file("up-diliman.osm")

# transform the list into a pandas DataFrame
data_colnames = ['type', 'id', 'ntags', 'tagkey', 'tagvalue', 'nodes']
df_osm = pd.DataFrame(way_handler.osm_data, columns=data_colnames)
#convert pandas DataFrame to .csv file
df_osm.to_csv('out_way.csv', encoding='utf-8', index=False)


# example git add for github
