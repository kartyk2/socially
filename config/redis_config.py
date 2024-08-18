import redis
from config.constants import get_settings

settings= get_settings()
redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)