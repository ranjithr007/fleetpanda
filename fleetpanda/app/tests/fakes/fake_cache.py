from app.services.cache_service import CacheService


class FakeCache(CacheService):

    def __init__(self):

        self.data = {}


    def get(self, key):

        return self.data.get(key)


    def set(self, key, value, ttl=300):

        self.data[key] = value
        return True