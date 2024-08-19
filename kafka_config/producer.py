from config.constants import settings
from kafka import KafkaProducer
import json

kafka_producer = KafkaProducer(
    bootstrap_servers=settings.kafka_bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


