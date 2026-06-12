import redis

from app.services.cache_service import CacheService


class RedisCacheService(CacheService):

    def __init__(self):

        self.client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )


    def get(self, key):

        return self.client.get(key)


    def set(self, key, value, ttl=300):

        self.client.set(
            key,
            value,
            ex=ttl
        )