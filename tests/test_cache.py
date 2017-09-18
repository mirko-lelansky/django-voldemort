class TestVoldemortCache():
    """
    This is the test class for the VoldemortCache.
    """

    def test_simple(self, django_cache):
        """
        This method tests a simple set get round trip.
        """
        django_cache.set("key", "value")
        assert "value" == django_cache.get("key")
