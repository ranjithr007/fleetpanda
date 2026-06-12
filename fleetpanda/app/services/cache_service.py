class CacheService:

    def get(self, key: str):
        raise NotImplementedError

    def set(self, key: str, value, ttl: int = 300):
        raise NotImplementedError