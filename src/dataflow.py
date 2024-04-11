import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import json

from bytewax.dataflow import Dataflow
import bytewax.operators as op
import bytewax.operators.window as win
from bytewax.connectors.stdio import StdOutSink
from bytewax.connectors.kafka import operators as kop
from bytewax.connectors.kafka import KafkaSinkMessage, KafkaSourceMessage, KafkaSink

from src.agg import WeatherAggregator

load_dotenv(override=True)

KAFKA_TOPIC_INPUT=os.getenv('KAFKA_TOPIC_INPUT')
KAFKA_BOOTSTRAP_SERVER_INPUT=os.getenv('KAFKA_BOOTSTRAP_SERVER_INPUT')

KAFKA_TOPIC_OUTPUT=os.getenv('KAFKA_TOPIC_OUTPUT')
KAFKA_BOOTSTRAP_SERVER_OUTPUT=os.getenv('KAFKA_BOOTSTRAP_SERVER_OUTPUT')

WINDOW_ALIGN_TO = datetime.now(timezone.utc)
WINDOW_LENGTH = timedelta(seconds=60)

print(' --- CONFIG ---')
print(f'KAFKA_TOPIC_INPUT: {KAFKA_TOPIC_INPUT}')
print(f'KAFKA_TOPIC_OUTPUT: {KAFKA_TOPIC_OUTPUT}')
print(f'KAFKA_BOOTSTRAP_SERVER_INPUT: {KAFKA_BOOTSTRAP_SERVER_INPUT}')
print(f'KAFKA_BOOTSTRAP_SERVER_OUTPUT: {KAFKA_BOOTSTRAP_SERVER_OUTPUT}')

def process_kafka_input(msg: KafkaSourceMessage) -> KafkaSinkMessage:
    key = json.loads(msg.key)['key']
    value = json.loads(msg.value)
    topic = msg.topic
    timestamp_ms = msg.timestamp[1]
    timestamp_s = datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc)

    return KafkaSinkMessage(
        key=key,
        value=value,
        topic=topic,
        timestamp=timestamp_s
    )


def prepare_output(inputs):
    metadata, window_agg = inputs
    return (metadata, window_agg.get_data(as_dict=True))


def prepare_output_to_kafka(inputs):
    key, (metadata, values) = inputs

    output_value = {
        'metadata': {
            'open_time': metadata.open_time.isoformat(),
            'close_time': metadata.close_time.isoformat()
        },
        'weather': values
    }

    return KafkaSinkMessage(
        key,
        value=json.dumps(output_value),
        topic=KAFKA_TOPIC_OUTPUT
    )


flow = Dataflow('WeatherProcessing')

kafka_input = kop.input(
    step_id='Input', 
    flow=flow, 
    brokers=[KAFKA_BOOTSTRAP_SERVER_INPUT],
    topics=[KAFKA_TOPIC_INPUT],
    )

stream = op.map(
    step_id='ProcessKafkaInput',
    up=kafka_input.oks,
    mapper=process_kafka_input
)

keyed_stream = op.key_on(
    step_id='KeyedStream',
    up=stream,
    key=lambda msg: msg.key
)

clock = win.EventClockConfig(
    lambda msg: msg.timestamp,
    wait_for_system_duration=timedelta(seconds=0)
)

windower = win.TumblingWindow(
    length=WINDOW_LENGTH,
    align_to=WINDOW_ALIGN_TO
)

window_fold = win.fold_window(
    step_id='Aggregate',
    up=keyed_stream,
    clock=clock,
    windower=windower,
    builder=WeatherAggregator,
    folder=WeatherAggregator.update
)

output = op.map_value('PrepareOutput', window_fold, prepare_output)

kafka_ouput = op.map('PrepareKafkaOuput', output, prepare_output_to_kafka)

kop.output('KafkaOutput', kafka_ouput, brokers=[KAFKA_BOOTSTRAP_SERVER_OUTPUT], topic=KAFKA_TOPIC_OUTPUT)
