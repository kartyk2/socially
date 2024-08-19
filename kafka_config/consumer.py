from config.constants import settings
from kafka import KafkaConsumer
import json

# Kafka Consumer setup
kafka_consumer = KafkaConsumer(
    settings.kakfa_topic,
    bootstrap_servers=settings.kakfa_host_server,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

for message in kafka_consumer:
    print(f"Received message: {message.value}")
