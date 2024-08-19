from kafka_config.producer import kafka_producer
from config.constants import get_settings
from datetime import datetime
import socketio
import uuid

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='asgi')
sio_app = socketio.ASGIApp(sio)

setting= get_settings()
connected_clients = {}

@sio.event
async def connect(sid, environ):
    user_id = str(uuid.uuid4())
    connected_clients[user_id] = sid
    print(f"User connected: {user_id}")

@sio.event
async def disconnect(sid):
    for user_id, socket_id in connected_clients.items():
        if socket_id == sid:
            del connected_clients[user_id]
            print(f"User disconnected: {user_id}")
            break

@sio.event
async def message(sid, data):
    message_payload = {
        "user_id": next((uid for uid, socket_id in connected_clients.items() if socket_id == sid), None),
        "message": data,
        "timestamp": datetime.now().isoformat()
    }

    kafka_producer.send(setting.kafka_topic, value=message_payload)
    print(f"Message sent to Kafka: {message_payload}")
