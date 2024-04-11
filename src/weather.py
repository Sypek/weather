import os
from dotenv import load_dotenv
import requests
from utils.types import Weather
import random

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_WEATHER_URL = os.getenv('API_WEATHER_URL')


def format_response(response: dict) -> Weather:
    return Weather(
        temp=response['main']['temp'],
        pressure=response['main']['pressure'],
        humidity=response['main']['humidity'],
        wind_speed=response['wind']['speed'],
    )

def get_current_weather_data(lat: int, lon: int):
    url = API_WEATHER_URL
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(url, params)
        response.raise_for_status()
        return format_response(response.json())
    except requests.exceptions.RequestException as e:
        print(e)


def get_current_weather_data_MOCKED(lat: int, lon: int):
    mocked_response = {
        'main': {
            'temp': random.random() * 10,
            'pressure': random.random() * 1000,
            'humidity': random.random()
        },
        'wind': {
            'speed': random.random() * 15
        }
    }
    return format_response(mocked_response)