import requests
import os

api_key = os.environ['FLIGHT_LABS_API_TOKEN']
params = [
        "arr_iata=TLV",
        "flight_status=active"
        ]

host = f'https://app.goflightlabs.com/flights?access_key={api_key}&{"&".join(params)}'
print(host)
#bgn_flights = requests
