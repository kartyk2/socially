from config.constants import settings
from kafka import KafkaProducer
import json

kafka_producer = KafkaProducer(
    bootstrap_servers=settings.kakfa_host_server,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


