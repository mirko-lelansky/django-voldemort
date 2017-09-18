from django.core.cache import cache
import pytest

@pytest.fixture
def django_cache():
    yield cache
    cache.clear()
