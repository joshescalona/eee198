from flask import Flask, render_template
import folium
import os
import json
from app_functions import dijkstra, get_coordinates, dijkstra_endlist, shortestpath, searchbasedRS

app = Flask(__name__)

@app.route('/')
def index():
    # UP Diliman coordinates
    start_coords = (14.6538, 121.0685)
    folium_map = folium.Map(location=start_coords,zoom_start=16,height='85%')

    # Create custom marker icon
    car_icon = folium.features.CustomIcon('map_data/car_marker_3.png', icon_size=(40, 40))

    # Geojson data
    route = os.path.join('map_data', 'route.json')

    passengers = ['17216409','5449447770','26082653']
    passenger_destinations = ['321700941','5464380760','30763205']
    drivers = ['22352470']

    # output to the map (markers)
    # path, route_distance, end_node = shortestpath('adj_list_obj.pkl', '22352470', ['17216409','5449447770','26082653'])
    sources, destinations, path, route_distance = searchbasedRS('adj_list_obj.pkl', drivers, passengers, passenger_destinations, 0.35)
    coordinates = get_coordinates('nodes_coordinates.pkl', path)

    way_sample=folium.PolyLine(locations=coordinates,weight=5,color = 'red')
    folium_map.add_child(way_sample)

    if sources != None:
        # Create markers
        ctr = 0
        for source in sources:
            index = path.index(source)
            if ctr == 0:
                icon_color = 'blue'
            elif ctr == 1:
                icon_color = 'green'
            elif ctr == 2:
                icon_color = 'orange'
            folium.Marker(coordinates[index], tooltip='Source', icon=folium.Icon(color=icon_color, icon='chevron-up')).add_to(folium_map),
            ctr+=1

        ctr = 0
        for destination in destinations:
            index = path.index(destination)
            if ctr == 0:
                icon_color = 'blue'
            elif ctr == 1:
                icon_color = 'green'
            elif ctr == 2:
                icon_color = 'orange'
            folium.Marker(coordinates[index], tooltip='Destination', icon=folium.Icon(color=icon_color, icon='chevron-down')).add_to(folium_map),
            ctr+=1

        for driver in drivers:
            index = path.index(driver)
            folium.Marker(coordinates[index],
                  tooltip='Driver', icon=car_icon).add_to(folium_map)

        # # Geojson overlay
        # folium.GeoJson(route, name='route').add_to(folium_map)

    folium_map.save('templates/map.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

