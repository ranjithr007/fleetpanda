from app.tests.fakes.fake_cache import FakeCache


def test_cache_set_get():

    cache = FakeCache()

    cache.set("test", {"value": 100})

    result = cache.get("test")

    assert result["value"] == 100