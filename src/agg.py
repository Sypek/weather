from statistics import mean
from utils.types import MeasurementsAgg
from dataclasses import asdict


class MeasurementsAggregator:
    def __init__(self, name: str) -> None:
        self.name = name
        self.measurements = []

    def update(self, measurement: float):
        self.measurements.append(measurement)

    @property
    def min_measurement(self) -> float:
        if self.measurements:
            return min(self.measurements)
        else:
            return 0
        
    @property
    def max_measurement(self) -> float:
        if self.measurements:
            return max(self.measurements)
        else:
            return 0
        
    @property
    def avg_measurement(self) -> float:
        if self.measurements:
            return mean(self.measurements)
        else:
            return 0
    
    def get_aggregates(self, as_dict=False): 
        agg = MeasurementsAgg(
            self.min_measurement,
            self.max_measurement,
            self.avg_measurement
        )

        if as_dict:
            return asdict(agg)
        else:
            return agg


class WeatherAggregator:
    def __init__(self) -> None:
        self.aggregators = {}

    def update(self, event):
        values = event.value
        for measurement_name, measurement_value in values.items():
            if measurement_name not in self.aggregators:
                m_agg = MeasurementsAggregator(measurement_name)
                self.add_measurement_agg(m_agg)

            self.aggregators[measurement_name].update(measurement_value)
        return self

    def add_measurement_agg(self, agg: MeasurementsAggregator):
        self.aggregators[agg.name] = agg

    def get_data(self, as_dict: bool = False) -> dict:
        data = {}

        for agg_name, agg in self.aggregators.items():
            data[agg_name] = agg.get_aggregates(as_dict)
        
        return data
