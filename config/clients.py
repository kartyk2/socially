import redis
from config.constants import get_settings
from vonage import Client


settings= get_settings()
redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)
sms_client= Client(settings.api_key, settings.api_secret)
