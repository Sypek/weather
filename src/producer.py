import os
import json
import random
from dataclasses import asdict
from dotenv import load_dotenv
from kafka import KafkaProducer
from time import sleep


from src.weather import get_current_weather_data, get_current_weather_data_MOCKED
from utils.types import CityLocation


load_dotenv()

KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVER')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')

city = CityLocation(
    os.getenv('CITY_NAME'),
    os.getenv('CITY_LAT'),
    os.getenv('CITY_LON'),
)

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVER],
    key_serializer=lambda v: json.dumps(v).encode('utf-8'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print(f'Producer sending to kafka topic: {KAFKA_TOPIC} on server: {KAFKA_BOOTSTRAP_SERVER}')

for i in range(30):
    # current_weather = asdict(get_current_weather_data(lat=city.lat, lon=city.lon))
    current_weather = asdict(get_current_weather_data_MOCKED(lat=city.lat, lon=city.lon))

    producer.send(
        topic=KAFKA_TOPIC,
        key={'key': city.name},
        value=current_weather
    )

    print(f'Send message: {current_weather} to kafka topic: {KAFKA_TOPIC}')
    sleep(15)