from django.core.cache import cache

class Redis:
    """Redis utilities"""
    @staticmethod
    def save_data_in_redis(key, timeout=600, **kwargs):
        """Save data in Redis"""
        cache.set(key, kwargs, timeout)  

    @staticmethod
    def check_data_in_redis(key):
        """Check if data is in Redis"""
        if not cache.get(key):
            return False
        return True
    
    @staticmethod
    def get_data_from_redis(key):
        """Get data from Redis"""
        value = cache.get(key)
        return value
    
    @staticmethod
    def delete_data_from_redis(*keys):
        """Delete data from Redis"""
        for key in keys:
            cache.delete(key)

    @staticmethod
    def clear_all_data():
        """Clear all data from Redis"""
        cache.clear()
