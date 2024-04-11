from datetime import datetime
import random
from src.weather import format_response


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


class MockedKafkaOutputMessage:
    def __init__(self) -> None:
        self.value = {
            'metadata': {
                'last_update': datetime.now()
            },
            'weather': {
                "temp": {
                    "min_val": 0.13477908701338026,
                    "max_val": 8.153715718683442,
                    "avg_val": 4.030835133732715
                },
                "pressure": {
                    "min_val": 81.09192808231735,
                    "max_val": 876.1916254008582,
                    "avg_val": 525.9585085918495
                },
                "humidity": {
                    "min_val": 0.6613435604324076,
                    "max_val": 0.8012037478619463,
                    "avg_val": 0.7362375068458055
                },
                "wind_speed": {
                    "min_val": 2.604153454052951,
                    "max_val": 11.407732868866695,
                    "avg_val": 7.1511959945301395
                }
            }
        }
