from kafka_config.producer import kafka_producer
from datetime import datetime
import socketio
import uuid

sio = socketio.AsyncServer(cors_allowed_origins="*")
sio_app = socketio.ASGIApp(sio)

# Dictionary to keep track of connected clients
connected_clients = {}

@sio.event
async def connect(sid, environ):
    user_id = str(uuid.uuid4())  # Example user ID
    connected_clients[user_id] = sid
    print(f"User connected: {user_id}")

@sio.event
async def disconnect(sid):
    # Find and remove the user_id from connected_clients
    for user_id, socket_id in connected_clients.items():
        if socket_id == sid:
            del connected_clients[user_id]
            print(f"User disconnected: {user_id}")
            break

@sio.event
async def message(sid, data):
    # Process incoming messages and send to Kafka
    message_payload = {
        "user_id": next((uid for uid, socket_id in connected_clients.items() if socket_id == sid), None),
        "message": data,
        "timestamp": datetime.utcnow().isoformat()
    }

    kafka_producer.send('your_topic', value=message_payload)
    print(f"Message sent to Kafka: {message_payload}")
