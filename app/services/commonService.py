
from app.persist import configDao, baseDao
from cacheout import Cache

_application_config_cache = Cache(maxsize=200, ttl=5 * 60)


def get_config_by_key(key):
    session = baseDao.get_session()
    if _application_config_cache.has(key):
        value = _application_config_cache.get(key)
        return value
    else:
        c = configDao.get_config_by_key(session, key)

        if c is not None:
            _application_config_cache.add(c.key, c.value)
            return c.value
        else:
            return None


def load_application_cache_from_db():
    session = baseDao.get_session()
    # -- Application Config from Database --
    config_items = configDao.get_config_all(session)
    for c in config_items:
        _application_config_cache.add(c.key, c.value)
