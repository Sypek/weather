import os
import json
from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv(override=True)

KAFKA_BOOTSTRAP_SERVER_OUTPUT = os.getenv('KAFKA_BOOTSTRAP_SERVER_OUTPUT')
KAFKA_TOPIC_OUTPUT = os.getenv('KAFKA_TOPIC_OUTPUT')

consumer = KafkaConsumer(
    KAFKA_TOPIC_OUTPUT,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVER_OUTPUT,
    value_deserializer=lambda v: json.loads(v),
    auto_offset_reset='earliest'
)