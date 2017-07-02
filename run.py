"""
By Gabby
"""

from flask import Flask, render_template, request, jsonify
from triangulate.earthquakes import SeismicStation, StationEvent, Earthquake
import requests
from triangulate.exceptions import SeismicError

app = Flask(__name__, static_url_path='')
app.debug = True


@app.route("/calculate", methods=['POST'])
def calculate():
    """
    POST Endpoint
    """

    station_data = request.json.get('station_data', None)

    if station_data is None:
        return jsonify(status=f'Invalid request: {request.json}')

    stations = dict()
    for station_name, station_attributes in station_data.items():
        address = station_attributes['name']
        latitude = float(station_attributes['latitude'])
        longitude = float(station_attributes['longitude'])

        p_arrival_time = station_attributes['p_arrival_time']
        s_arrival_time = station_attributes['s_arrival_time']
        max_amplitude = float(station_attributes['max_amplitude'])

        station = SeismicStation(address, (latitude, longitude))

        try:
            event = StationEvent(p_arrival_time, s_arrival_time, max_amplitude)
        except ValueError:
            return jsonify(status="error", message="invalid time format")

        station.add_event(event)
        stations[station.name] = station

    earthquake = Earthquake(*stations.values())
    try:
        lat, lon = earthquake.calc_epicenter()
    except SeismicError as e:
        return jsonify(status="error", message=e.message)

    epicenter = {'lat': lat, 'lon': lon}

    return jsonify(status='success', epicenter=epicenter)


@app.route('/geocode', methods=['POST'])
def geocode():
    station_address = request.json.get('entry', None)
    if station_address is None:
        return jsonify(status="error", message="invalid request parameters, pass entry")

    api_key = "AIzaSyB9OX0ztoM73i9ZgUPJQQVKcmZrxSaRjts"
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={station_address}&key={api_key}'
    api_response = requests.get(url)
    api_response_dict = api_response.json()

    if api_response_dict['status'] == 'OK':
        return jsonify(status="success", result=api_response_dict)
    else:
        return jsonify(status="error", message="something went wrong with geocoding.")


@app.route("/")
def map():
    """
    Template view | Google Maps
    """
    return render_template('a-map.html', name='llamas')

stations = list()

if __name__ == "__main__":
    app.run()
