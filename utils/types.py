from dataclasses import dataclass

@dataclass
class CityLocation:
    name: str
    lat: float
    lon: float


@dataclass
class Weather:
    temp: float
    pressure: float
    humidity: float
    wind_speed: float


@dataclass
class MeasurementsAgg:
    min_val: float
    max_val: float
    avg_val: float