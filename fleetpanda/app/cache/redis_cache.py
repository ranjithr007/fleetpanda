import redis
import json

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1,
)


class RedisCache:

    def get(self, key):

        value = redis_client.get(key)

        if value:

            return json.loads(value)

        return None

    def set(self, key, value, ttl=300):

        redis_client.setex(key, ttl, json.dumps(value))

    def delete(self, key):

        redis_client.delete(key)


cache = RedisCache()