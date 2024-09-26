from commons.helper import TokenPayload, decode_jwt, get_current_user
from kafka_config.producer import kafka_producer
from config.clients import redis_client
from config.constants import get_settings
from config.database_config import DatabaseSessionsManager
from models.user import User
from datetime import datetime
import socketio
import uuid
import uvicorn

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='asgi')
sio_app = socketio.ASGIApp(sio)

settings = get_settings()

async def connect_user(user_id, sid):
    redis_client.set(f"user:{user_id}", sid)
    redis_client.set(f"socket:{sid}", user_id)
    print(f"User connected: {user_id}")

async def disconnect_user(sid):
    user_id = redis_client.get(f"socket:{sid}")
    if user_id:
        redis_client.delete(f"user:{user_id}")
        redis_client.delete(f"socket:{sid}")
        print(f"User disconnected: {user_id}")

async def mark_user_online(user: uuid.UUID):
    with DatabaseSessionsManager(settings.pg_dsn.unicode_string()) as db:
        db.query(User).filter(User.id == user).update({"is_active": True}, synchronize_session= False)
        db.commit()
        
    print("user marked online")
        
async def set_last_seen():
    pass

@sio.event
async def connect(sid, token):
    
    token_payload: TokenPayload= decode_jwt(token, settings.encoding_secret_key)
    user= token_payload.id
    
    await connect_user(user, sid)
    await mark_user_online(user)
    
@sio.event
async def disconnect(sid):
    await disconnect_user(sid)
    # mark user as  offline and set last seen 
    
@sio.event
async def message(sid, data):
    user_id = redis_client.get(f"socket:{sid}")
    if user_id:
        message_payload = {
            "user_id": user_id,
            "message": data,
            "timestamp": datetime.now().isoformat()
        }
        await sio.emit('welcome', {'message': 'Welcome to the chat!', 'user_id': user_id}, room=sid)

        try:
            kafka_producer.send(settings.kafka_topic, value=message_payload)
            kafka_producer.flush()
            print(f"Message sent to Kafka: {message_payload}")
        except Exception as e:
            print(f"Failed to send message to Kafka: {e}")

@sio.event
async def hello(sid, data):
    user_id = await redis_client.get(f"socket:{sid}")
    if user_id:
        message_payload = {
            "user_id": user_id,
            "message": data,
            "timestamp": datetime.now().isoformat()
        }
        try:
            kafka_producer.send(settings.kafka_topic, value=message_payload)
            kafka_producer.flush()
            print(f"Message sent to Kafka: {message_payload}")
        except Exception as e:
            print(f"Failed to send message to Kafka: {e}")

if __name__ == "__main__":
    uvicorn.run("chat_socket:sio_app", host='localhost', port=8001)
