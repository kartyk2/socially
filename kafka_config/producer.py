from kafka import KafkaProducer
from config.constants import get_settings
import json

def create_kafka_producer():
    settings = get_settings()
    return KafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

kafka_producer = create_kafka_producer()