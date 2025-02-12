import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

try:
    redis_client.ping()
    print("Connected to Redis!")
    redis_client.flushdb()
    print("Redis cache cleared!")
except redis.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
