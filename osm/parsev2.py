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
        key = []
        value = []
        include = 0
        for tag in elem.tags:
            # this if statement removes all oneway='no' tags (assume two way if no tag)
            if tag.k == 'oneway' and tag.v == 'no':
                continue
            key.append(tag.k)
            value.append(tag.v)
            # check if way has any of these wanted tags and include if so
            if (tag.k == 'highway' and tag.v =='motorway') or (tag.k == 'highway' and tag.v =='trunk') or (tag.k == 'highway' and tag.v =='motorway_link') or (tag.k == 'highway' and tag.v =='trunk_link') or (tag.k == 'highway' and tag.v =='primary') or (tag.k == 'highway' and tag.v =='primary_link') or (tag.k == 'highway' and tag.v =='secondary') or (tag.k == 'highway' and tag.v =='secondary_link') or (tag.k == 'highway' and tag.v =='tertiary') or (tag.k == 'highway' and tag.v =='tertiary_link') or (tag.k == 'highway' and tag.v =='unclassified') or (tag.k == 'highway' and tag.v =='unclassified_link') or (tag.k == 'highway' and tag.v =='residential') or (tag.k == 'highway' and tag.v =='residential_link') or (tag.k == 'highway' and tag.v =='service') or (tag.k == 'highway' and tag.v =='service_link') or (tag.k == 'highway' and tag.v =='living_street') or (tag.k == 'highway' and tag.v =='track') or (tag.k == 'highway' and tag.v =='path') or (tag.k == 'access' and tag.v =='yes') or (tag.k == 'access' and tag.v =='permissive'):
                include = 1

        if include == 1:
            self.osm_data.append([elem_type,
                                    elem.id,
                                    len(elem.tags),
                                    key,
                                    value,
                                    elem.nodes])

    def way(self, w):
        self.tag_inventory(w, "way")


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



