import redis
import os
redis_client = redis.Redis(
    host=os.getenv('redis_host', 'localhost'),
    port=int(os.getenv('redis_port', 6379)),
    decode_responses=True,
    )