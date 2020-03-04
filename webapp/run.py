from flask import Flask, render_template
import folium
import os
import json
from algorithm_functions import dijkstra, get_coordinates

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

    shortest_distance, path = dijkstra('adj_list_obj.pkl', '5449447770', '5383505901')
    coordinates = get_coordinates('nodes_coordinates.pkl', path)

    # coordinates = [[14.6549972,121.064311],
    # [14.6549938, 121.0641616],
    # [14.6549909, 121.0640536],
    # [14.6549663, 121.0631421],
    # [14.654955,121.0627244],
    # [14.654945,121.0623539]]


    way_sample=folium.PolyLine(locations=coordinates,weight=5,color = 'red')
    folium_map.add_child(way_sample)

    # Create markers
    folium.Marker(coordinates[0], tooltip='You are here!').add_to(folium_map),

    folium.Marker(coordinates[-1],
              tooltip='Driver', icon=car_icon).add_to(folium_map),

    # # Geojson overlay
    # folium.GeoJson(route, name='route').add_to(folium_map)

    folium_map.save('templates/map.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

