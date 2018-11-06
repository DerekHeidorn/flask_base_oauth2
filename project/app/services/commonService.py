

from project.app.persist.configDao import getConfigAll
from werkzeug.contrib.cache import SimpleCache

applicationConfigCache = SimpleCache()


def getConfigByKey(key):
    value = applicationConfigCache.get(key)
    return value


def loadApplicationCacheFromDB():

    # -- Application Config from Database --
    configItems = getConfigAll()
    for c in configItems:
        applicationConfigCache.add(c.key, c.value)
        print("app config: " + c.key + "=" + c.value)

