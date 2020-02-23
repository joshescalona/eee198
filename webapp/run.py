from flask import Flask, render_template
import folium
import os
import json

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

    # Create markers
    folium.Marker([14.6538, 121.0685], tooltip='You are here!').add_to(folium_map),

    folium.Marker([14.655, 121.063],
              tooltip='Driver', icon=car_icon).add_to(folium_map),

    # Geojson overlay
    folium.GeoJson(route, name='route').add_to(folium_map)

    folium_map.save('templates/map.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

