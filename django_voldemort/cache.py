# Copyright 2017 Mirko Lelansky <mlelansky@mail.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This module contains the django cache implementation for the voldemort cluster.
"""
from django.core.cache.backends.base import BaseCache, DEFAULT_TIMEOUT
from voldemort_client.client import VoldemortClient


class VoldemortCache(BaseCache):
    """
    This class is the django adapter for the voldemort key-value system.
    """

    def __init__(self, servers, params):
        """This is the constructor method of the class.

        Parameters
        ----------
        servers : list
            the list of (serverurl, node_id)
        params : dict
            the backend params

        Raise
        -----
        ValueError
            if the parameters not valid
        """
        super().__init__(params)
        self._client = None
        self._options = params.get("OPTIONS") or {}
        self._params = params

        if isinstance(servers, (list, tuple)):
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
        """This method adds a key-value pair on the cluster.

        Set a value in the cache if the key does not already exist. If
        timeout is given, use that timeout for the key; otherwise use the
        default cache timeout.

        Parameters
        ----------
        key : str
            the key which should be stored
        value : str
            the value of the key
        timeout : int
            the timeout value of the key
        version : int
            the version of the key

        Returns
        -------
        bool
            True if the value was stored, False otherwise
        """
        key = self.make_key(key, version)
        self._cache.add(key, value, self.get_backend_timeout(timeout))

    def clear(self):
        """Remove *all* values from the cache at once."""
        self._cache.clear()

    def delete(self, key, version=None):
        """Delete a key from the cache, failing silently.

        Parameters
        ----------
        key : str
            the key to delete
        """
        key = self.make_key(key, version)
        self._cache.delete(key)

    def get(self, key, default=None, version=None):
        """Fetch a given key from the cache.

        If the key does not exist, return default, which itself defaults
        to None.

        Parameters
        ----------
        key : str
            the key to fetch
        default : str
            the default value of the key
        version : int
            the version of the key

        Returns
        -------
        str
            the fetched value or the default value
        """
        key = self.make_key(key, version)
        val = self._cache.get(key)
        result = None
        if val is not None:
            result = val
        else:
            result = default
        return result


    def get_many(self, keys, version=None):
        """Fetch a bunch of keys from the cache.

        For certain backends (memcached, pgsql) this can be *much* faster when
        fetching multiple values. Return a dict mapping each key in keys to
        its value. If the given key is missing, it will be missing from the
        response dict.

        Parameters
        ----------
        keys : list
            the list of keys to fetch
        version : int
            the version of the keys

        Returns
        -------
        dict
            the fetched values as a dictionary
        """
        keys = [self.make_key(key, version) for key in keys]
        return self._cache.get_many(keys)

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        """Set a value in the cache.

        If timeout is given, use that timeout for the key; otherwise use the
        default cache timeout.

        Parameters
        ----------
        key : str
            the key to stored
        value : str
            the value of the key
        timeout : int
            the timeout value of the key
        version : int
            the version of the key
        """
        key = self.make_key(key, version)
        self._cache.set(key, value, self.get_backend_timeout(timeout))

    @property
    def _cache(self):
        """Implements transparent thread-safe access to a voldemort client.

        Returns
        -------
        :py:class:`voldemort_client.client.VoldemortClient`
            the cached client instance
        """
        if getattr(self, '_client', None) is None:
            self._client = VoldemortClient(self._servers, self._store_name)
        return self._client
