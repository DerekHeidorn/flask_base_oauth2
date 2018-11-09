
from werkzeug.contrib.cache import SimpleCache
from project.app.persist import configDao

application_config_cache = SimpleCache()


def get_config_by_key(key):
    value = application_config_cache.get(key)

    if value is None:
        c = configDao.get_config_by_key(key)

        if c is not None:
            application_config_cache.add(c.key, c.value)

    return value


def load_application_cache_from_db():

    # -- Application Config from Database --
    config_items = configDao.get_config_all()
    for c in config_items:
        application_config_cache.add(c.key, c.value)
        print("app config: " + c.key + "=" + c.value)
