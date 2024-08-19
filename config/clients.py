import redis
from config.constants import _settings
from vonage import Client


settings= _settings()
redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)
sms_client= Client(settings.api_key, settings.api_secret)
