from flask import Flask, render_template
import folium
import os
import json
from app_functions import dijkstra, get_coordinates, dijkstra_endlist, shortestpath

app = Flask(__name__)

@app.route('/')
def index():
    # UP Diliman coordinates
    start_coords = (14.6538, 121.0685)
    folium_map = folium.Map(location=start_coords,zoom_start=16,height='85%')

    # Create custom marker icon
    car_icon = folium.features.CustomIcon('map_data/car-marker.png', icon_size=(50, 30))

    # Geojson data
    route = os.path.join('map_data', 'route.json')

    # output to the map (markers)
    # shortest_distance, path = dijkstra('adj_list_obj.pkl', '5449447770', '5383505901')
    # coordinates = get_coordinates('nodes_coordinates.pkl', path)
    path, route_distance = shortestpath('adj_list_obj.pkl', '22352470', ['17216409','5449447770'], '26082653')
    # shortest_distance, path = dijkstra('adj_list_obj.pkl', '17216409', '22352470')
    # path = shortestpath('adj_list_obj.pkl', '5449447770', ['22352470'], '5383505901')
    coordinates = get_coordinates('nodes_coordinates.pkl', path)

    way_sample=folium.PolyLine(locations=coordinates,weight=5,color = 'red')
    folium_map.add_child(way_sample)

    # Create markers
    passengers = ['17216409','5449447770','26082653']
    for passenger in passengers:
        index = path.index(passenger)
        folium.Marker(coordinates[index], tooltip='You are here!').add_to(folium_map),

    drivers = ['22352470']
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

