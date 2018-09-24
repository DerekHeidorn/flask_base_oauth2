
from flask import Blueprint
from flask import jsonify

from persist.configDao import getConfigAll
from werkzeug.contrib.cache import SimpleCache

api = Blueprint('common_api', __name__)
applicationCache = SimpleCache()


@api.route('/api/v1.0/app/version', methods=['GET'])
#@oauth.require_oauth('email')
def getAppVersion():
    version = applicationCache.get("app.release_number")

    return jsonify({"application.version": version})


def loadApplicationCacheFromDB():

    # -- Application Config from Database --
    configItems = getConfigAll()
    for c in configItems:
        applicationCache.add(c.key, c.value)
        print("app config: " + c.key + "=" + c.value)

