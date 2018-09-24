from models.user import User
from persist import codetableDao
from models.codetables.users import CtUserStatuses, CtUserTypes


import json
from flask import Blueprint
from flask import jsonify
from flask import abort
from werkzeug.contrib.cache import SimpleCache

api = Blueprint('codetablesService_api', __name__)

allowableCodetableMap = {"CtUserStatuses" : CtUserStatuses, "CtUserTypes" : CtUserTypes}
codetableCache = SimpleCache()

@api.route('/api/v1.0/codetables/<codetableName>', methods=['GET'])
#@oauth.require_oauth('email')
def codetable_by_name(codetableName):

    allowedCodetable = allowableCodetableMap.get(codetableName)

    if allowedCodetable is not None:
        # Check cache
        cachedCodetable = codetableCache.get(codetableName)

        if(cachedCodetable is not None):
            print("\n*** CachedcodeTable: " + str(cachedCodetable))
            return jsonify(cachedCodetable)

        else:
            codetableData = codetableDao.get_code_table(allowedCodetable, serialize=True)
            if codetableData:
                codetableCache.add(codetableName, codetableData)
                return jsonify(codetableData)

    abort(404)