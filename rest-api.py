from math import dist
import argparse
import requests
import os

from numpy import Infinity

AIRPORT_FIXED_COORDINATES = (32.013061, 34.861835)

api_key = os.environ['FLIGHT_LABS_API_KEY']
url = f'https://airlabs.co/api/v9/flights?dep_iata=TLV&api_key={api_key}'
data_dict = requests.get(url=url).json()

closest_distance = [Infinity, None]
for aircraft in data_dict['response']:
    geo_indexes = (aircraft['lat'], aircraft['lng'])
    distance_from_airport = dist(geo_indexes, AIRPORT_FIXED_COORDINATES)

    if distance_from_airport < closest_distance[0]:
        closest_distance = [distance_from_airport, aircraft]

print(closest_distance[1])
