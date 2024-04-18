import os
import json
from dataclasses import asdict
from dotenv import load_dotenv
from kafka import KafkaProducer
from time import sleep


from src.weather import get_current_weather_data
from utils.mocks import get_current_weather_data_MOCKED
from utils.types import CityLocation


load_dotenv(override=True)

KAFKA_BOOTSTRAP_SERVER_INPUT = os.getenv('KAFKA_BOOTSTRAP_SERVER_INPUT')
KAFKA_TOPIC_INPUT = os.getenv('KAFKA_TOPIC_INPUT')

print('Kafka config: ')
print(f'KAFKA_BOOTSTRAP_SERVER_INPUT: {KAFKA_BOOTSTRAP_SERVER_INPUT}')
print(f'KAFKA_TOPIC_INPUT: {KAFKA_TOPIC_INPUT}')

city = CityLocation(
    os.getenv('CITY_NAME'),
    os.getenv('CITY_LAT'),
    os.getenv('CITY_LON'),
)

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVER_INPUT],
    key_serializer=lambda v: json.dumps(v).encode('utf-8'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(2, 0, 2)  # version of kafka-python package
)

print(f'Producer sending to kafka topic: {KAFKA_TOPIC_INPUT} on server: {KAFKA_BOOTSTRAP_SERVER_INPUT}')

for i in range(30):
    # current_weather = asdict(get_current_weather_data(lat=city.lat, lon=city.lon))
    current_weather = asdict(get_current_weather_data_MOCKED(lat=city.lat, lon=city.lon))

    producer.send(
        topic=KAFKA_TOPIC_INPUT,
        key={'key': city.name},
        value=current_weather
    )

    print(f'Send message: {current_weather} to kafka topic: {KAFKA_TOPIC_INPUT}')
    sleep(15)