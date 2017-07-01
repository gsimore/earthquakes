"""
By Gabby
"""

from flask import Flask, render_template, request, jsonify
from triangulate.earthquakes import SeismicStation, StationEvent, Earthquake
import requests

app = Flask(__name__, static_url_path='')
app.debug = True


@app.route("/calculate", methods=['POST'])
def calculate():
    """
    POST Endpoint
    """

    station_address = request.form.get('station_address')

    api_key = "AIzaSyB9OX0ztoM73i9ZgUPJQQVKcmZrxSaRjts"
    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(station_address, api_key))
    api_response_dict = api_response.json()


    if api_response_dict['status'] == 'OK':
        latitude = api_response_dict['results'][0]['geometry']['location']['lat']
        longitude = api_response_dict['results'][0]['geometry']['location']['lng']

        seismic_station = SeismicStation(station_address, (latitude, longitude))
        # stations.append(seismic_station)

    s_arrival_time = request.form["s_arrival_time"]
    p_arrival_time = request.form["p_arrival_time"]
    max_amplitude = request.form["max_amplitude"]

    return jsonify(stations=stations, seismic_station=seismic_station)


@app.route("/")
def map():
    """
    Template view | Google Maps
    """
    return render_template('a-map.html', name='llamas')

stations = list()

if __name__ == "__main__":
    app.run()
