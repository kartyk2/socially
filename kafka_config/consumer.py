from config.constants import get_settings
from config.log_config import Logger
from kafka import KafkaConsumer
import json

settings= get_settings()
api_logger= Logger.get_api_info_logger()
error_logger= Logger.get_error_logger()

# Kafka Consumer setup
kafka_consumer = KafkaConsumer(
    settings.kafka_topic,
    bootstrap_servers=settings.kafka_bootstrap_servers,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=settings.kafka_group_id
)

def consume_messages():
    try:
        for message in kafka_consumer:
            print("New Message")
            api_logger.info(f"Received message: {message.value}")
            kafka_consumer.commit()
    except Exception as e:
        error_logger.error(f"Error consuming messages: {e}")
