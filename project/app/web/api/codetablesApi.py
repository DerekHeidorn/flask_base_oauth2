import json
from flask import Blueprint
from flask import jsonify
from flask import abort
from werkzeug.contrib.cache import SimpleCache

from project.app.models.user import User
from project.app.models.codetables.users import CtUserStatuses, CtUserTypes
from project.app.services import codetablesService
from project.app.web.utils import dtoUtils

api = Blueprint('codetables_api', __name__)

allowableCodetableMap = {"CtUserStatuses" : CtUserStatuses, "CtUserTypes" : CtUserTypes}
codetableCache = SimpleCache()

@api.route('/api/v1.0/codetables/<codetableName>', methods=['GET'])
#@oauth.require_oauth('email')
def codetableByName(codetableName):

    allowedCodetable = allowableCodetableMap.get(codetableName)

    if allowedCodetable is not None:
        # Check cache
        cachedCodetable = codetableCache.get(codetableName)

        if(cachedCodetable is not None):
            print("\n*** CachedcodeTable: " + str(cachedCodetable))
            return jsonify(cachedCodetable)

        else:
            codetableData = codetablesService.getCodeTable(allowedCodetable)
            data = dtoUtils.codetableSerialize(codetableData)
            print("codetableData=" + str(data))
            if data:
                codetableCache.add(codetableName, data)
                return jsonify(data)

    abort(404)