

from project.app.persist import configDao
from werkzeug.contrib.cache import SimpleCache

application_config_cache = SimpleCache()


def get_config_by_key(key):
    value = application_config_cache.get(key)
    return value


def load_application_cache_from_db():

    # -- Application Config from Database --
    config_items = configDao.get_config_all()
    for c in config_items:
        application_config_cache.add(c.key, c.value)
        print("app config: " + c.key + "=" + c.value)
