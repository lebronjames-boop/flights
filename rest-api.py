from inspect import _void
from math import dist, sqrt
import argparse
import airportsdata
import requests
from bs4 import BeautifulSoup
from art import *
import pycountry
from numpy import Infinity
import os

AIRPORT_FIXED_COORDINATES = (32.013061, 34.861835)

def get_closest_aircraft(all_aircrafts) -> dict:
    """
        Looping over all given flights dictionary
        :return: The closest one to Ben-Gurion Airport
    """
    closest_distance = [Infinity, None]
    for aircraft in all_aircrafts['response']:
        geo_indexes = (aircraft['lat'], aircraft['lng'])
        distance_from_airport = dist(geo_indexes, AIRPORT_FIXED_COORDINATES)

        if aircraft['alt'] > 0 and distance_from_airport < closest_distance[0]:
            closest_distance = [distance_from_airport, aircraft]
    return closest_distance[1]

def get_airline_company_by_iata(airline_code) -> str:
    """
        Parses an html page that gives the airline information by its IATA code
        :param airline_code: Airlines code by the IATA standard
        :return: A string of all the possible answers the site gives
    """
    raw_html = requests.get(f'https://www.iata.org/en/publications/directories/code-search/?airline.search={airline_code}').text
    soup = BeautifulSoup(raw_html, 'html.parser')
    results = soup.find_all("table", {"class": "datatable"})[0].find_all('tbody')[0].find_all('tr')
    final_result = ''
    for result in results:
        final_result += result.find_all('td')[0].text + ' / '

    return final_result[:-3]

def get_flight_time(arr_iata) -> str:
    """
        Getting the information from travelmath website and parsing its html
        :param arr_iata: Destination IATA code
        :return: The estimated flight time to the destination from Ben-Gurion.
    """
    res = requests.get(f'https://www.travelmath.com/flying-time/from/TLV/to/{arr_iata}').text
    soup = BeautifulSoup(res, 'html.parser')
    return soup.find("h3", {"id": "flyingtime"}).text

def get_flight_distance(arr_iata) -> str:
    """
        Getting the information from travelmath website and parsing its html
        :param arr_iata: Destination IATA code
        :return: The flight distance between Ben-Gurion to the airport whose iata is given, in miles and kilometers
    """
    res = requests.get(f'https://www.travelmath.com/distance/from/TLV/to/{arr_iata}').text
    soup = BeautifulSoup(res, 'html.parser')
    return soup.find("h3", {"class": "space"}).text.split('driving')[1].split('flying')[0]

def get_airport_info(iata_code) -> dict:
    """
        Getting all relevant information about the airport from the 'airportsdata' library
        :param iata_code: Airports IATA code
        :return: A dictionary of the information about the airport
    """
    airports = airportsdata.load('IATA')
    return airports[iata_code]

def get_destination_info_by_iso(iso_code) -> dict:
    """
        Getting the destination information within 'pycountry' library.
        :param iso_code: Country ISO-3166 code (alpha 2)
        :return: A dictionary with basic yet helpful information about the country
    """
    dest = pycountry.countries.get(alpha_2=iso_code)
    return dest

def print_output(flight_info, verbosity_level) -> _void:
    """
        Kinda stupid looking code but it's the prettiest way to print the output
        + includes verbosity dependencies
    """
    airport_info = get_airport_info(flight_info['arr_iata'])
    dest_info = get_destination_info_by_iso(airport_info['country'])

    full_destination = f'Destination: {airport_info["city"]}, {dest_info.name}, {(airport_info["name"] if verbosity_level > 0 else "")}'
    flight_iata_repr = flight_info['dep_iata'] + ' -> ' + flight_info['arr_iata']
    print(text2art(flight_info['flight_icao'], font="colossal") + (full_destination if verbosity_level == 0 else f'{flight_iata_repr}\n{full_destination}'))

    print('Airline company:', get_airline_company_by_iata(flight_info['airline_iata']))
    
    vertical_speed = flight_info['v_speed'] if 'v_speed' in flight_info.keys() else 0
    horizontal_speed = flight_info['speed']
    balanced_speed = sqrt(vertical_speed ** 2 + horizontal_speed ** 2)  # pitagoras formula
    speed_data = (f'Speed (absolute): {str(int(balanced_speed))} km/h') if verbosity_level == 0 or vertical_speed == 0 else \
    (f'Speed:\n   Vertical: {str(int(vertical_speed))} km/h\n    Horizontal: {str(horizontal_speed)} km/h\n    Absolute: {str(balanced_speed)}')
    print(speed_data)
    
    if verbosity_level > 0:
        print('Altitude:', flight_info['alt'], 'meters')

        try:
            distance = get_flight_distance(flight_info['arr_iata'])
        except:
            distance = None
        if distance:
            print('Flight time:', get_flight_time(flight_info['arr_iata']))
            print('Flight distance:', get_flight_distance(flight_info['arr_iata']))

    print()  #  Empty line at the end

def main():
    parser = argparse.ArgumentParser(
    description='Print the string or/and add the numbers')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    verbosity = parser.parse_args().verbose

    api_key = os.environ['FLIGHT_LABS_API_KEY']
    url = f'https://airlabs.co/api/v9/flights?dep_iata=TLV&api_key={api_key}'
    data_dict = requests.get(url=url).json()

    closest = get_closest_aircraft(data_dict)

    print_output(closest, verbosity)

if __name__ == "__main__":
    main()
