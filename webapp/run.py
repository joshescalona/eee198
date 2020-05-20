from flask import Flask, render_template
import folium
import os
import json
import time
from app_functions import dijkstra, get_coordinates, dijkstra_endlist, shortestpath, searchbasedRS, grab_share, get_largest_angle

app = Flask(__name__)

@app.route('/')
def index():
    # UP Diliman coordinates
    start_coords = (14.6538, 121.0685)
    folium_map = folium.Map(location=start_coords,zoom_start=16,height='85%')

    # Geojson data
    route = os.path.join('map_data', 'route.json')

    passengers = ['5446811375','29025439','17216409']
    passenger_destinations = ['17216442','2517360527','2517360522']
    # passengers = ['17216409','30763205']
    # passenger_destinations = ['17216442','30763515']
    drivers = ['30763220','1402297896','5499240548']

    # searchbased-rs implementation ------------------
    # start_time = time.perf_counter()
    # sources, destinations, path, route_distance = searchbasedRS('adj_list_obj.pkl', drivers, passengers, passenger_destinations, 0.8)
    # end_time = time.perf_counter()
    # print('\nSearch-BasedRS time elapsed (seconds): ' + str(end_time - start_time) + '\n')
    # ------------------------------------------------

    # # grab algorithm implementation ------------------
    start_time = time.perf_counter()
    sources, destinations, path, route_distance = grab_share('adj_list_obj.pkl', drivers, passengers, passenger_destinations, 121)
    end_time = time.perf_counter()
    print('\nGrabShare Algorithm time elapsed (seconds): ' + str(end_time - start_time) + '\n')
    # # ------------------------------------------------

    driver_coordinates = get_coordinates('nodes_coordinates.pkl', drivers)
    for driver_coordinate in driver_coordinates:
            # folium.Marker(driver_coordinate, tooltip='Driver', icon=folium.Icon(color='red', icon='user')).add_to(folium_map),
             # Create custom marker icon
            car_icon = folium.features.CustomIcon('map_data/car_marker.png', icon_size=(40, 40))
            folium.Marker(driver_coordinate,icon=car_icon).add_to(folium_map),

    # add source and destination markers
    source_nodes = [passengers[0], passenger_destinations[0]]
    source_coordinates = get_coordinates('nodes_coordinates.pkl', source_nodes)
    folium.Marker(source_coordinates[0], tooltip='Source', icon=folium.Icon(color='blue', icon='chevron-up')).add_to(folium_map),
    folium.Marker(source_coordinates[1], tooltip='Destination', icon=folium.Icon(color='blue', icon='chevron-down')).add_to(folium_map),

    # print('\nLargest angle (degrees): ' + str(get_largest_angle(driver_coordinates[1], source_coordinates)))

    # add additional markers and path if match/es found
    if sources != None:
        # add path
        coordinates = get_coordinates('nodes_coordinates.pkl', path)
        way_sample=folium.PolyLine(locations=coordinates,weight=5,color = 'red')
        folium_map.add_child(way_sample)
        # Create markers for matched sources and destinations
        # All drivers will have a marker to mimic actual ride sharing applications
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

        # # Geojson overlay
        # folium.GeoJson(route, name='route').add_to(folium_map)

    folium_map.save('templates/map.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

