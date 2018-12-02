
from app.persist import configDao
from cacheout import Cache

_application_config_cache = Cache(maxsize=200, ttl=5 * 60)


def get_config_by_key(key):

    if _application_config_cache.has(key):
        value = _application_config_cache.get(key)
        return value
    else:
        c = configDao.get_config_by_key(key)

        if c is not None:
            _application_config_cache.add(c.key, c.value)
            return c.value
        else:
            return None


def load_application_cache_from_db():

    # -- Application Config from Database --
    config_items = configDao.get_config_all()
    for c in config_items:
        _application_config_cache.add(c.key, c.value)
