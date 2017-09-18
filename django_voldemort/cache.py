from django.core.cache.backends.base import BaseCache, DEFAULT_TIMEOUT
from voldemort_client.client import VoldemortClient


class VoldemortCache(BaseCache):
    """
    This class is the django adapter for the voldemort key-value system.
    """

    def __init__(self, servers, params):
        """
        This is the constructor method of the class.

        :param servers: the list of (serverurl, node_id)
        :type servers: list of tuple
        :param params: the backend params
        :type params: dict
        """
        super().__init__(params)
        self._options = params.get("OPTIONS") or {}
        self._params = params

        if isinstance(servers, list) or isinstance(servers, tuple):
            if isinstance(servers, tuple):
                self._servers = [servers]
            else:
                self._servers = servers
        else:
            raise ValueError("The servers must be pass as tuple or list of tuple.")

        if "store_name" in self._options:
            self._store_name = self._options.get("store_name")
        else:
            raise ValueError("You must give an store_name.")

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        """
        Set a value in the cache if the key does not already exist. If
        timeout is given, use that timeout for the key; otherwise use the
        default cache timeout.

        Return True if the value was stored, False otherwise.
        """
        key = self.make_key(key, version)
        self._cache.add(key, value, self.get_backend_timeout(timeout))

    def clear(self):
        """
        Remove *all* values from the cache at once.
        """
        self._cache.clear()

    def delete(self, key, version=None):
        """
        Delete a key from the cache, failing silently.
        """
        key = self.make_key(key, version)
        self._cache.delete(key)

    def get(self, key, default=None, version=None):
        """
        Fetch a given key from the cache. If the key does not exist, return
        default, which itself defaults to None.
        """
        key = self.make_key(key, version)
        val = self._cache.get(key)
        if val is not None:
            return val
        else:
            return default

    def get_many(self, keys, version=None):
        """
        Fetch a bunch of keys from the cache. For certain backends (memcached,
        pgsql) this can be *much* faster when fetching multiple values.

        Return a dict mapping each key in keys to its value. If the given
        key is missing, it will be missing from the response dict.
        """
        keys = [self.make_key(key, version) for key in keys]
        result = self._cache.get_many(keys)

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        """
        Set a value in the cache. If timeout is given, use that timeout for the
        key; otherwise use the default cache timeout.
        """
        key = self.make_key(key, version)
        self._cache.set(key, value, self.get_backend_timeout(timeout))

    @property
    def _cache(self):
        """
        Implements transparent thread-safe access to a voldemort client.
        """
        if getattr(self, '_client', None) is None:
            self._client = VoldemortClient(self._servers, self._store_name)
        return self._client

