
from flask import Blueprint
from flask import jsonify
from flask import abort
from werkzeug.contrib.cache import SimpleCache

from project.app.models.codetables.users import CtUserStatus, CtUserType
from project.app.services import codetablesService
from project.app.web.utils import serializeUtils

api = Blueprint('codetables_api', __name__)

allowable_codetable_map = {"CtUserStatus": CtUserStatus, "CtUserType": CtUserType}
codetable_cache = SimpleCache()


@api.route('/api/v1.0/admin/codetables/<codetableName>', methods=['GET'])
def codetable_by_name(codetable_name):

    allowed_codetable = allowable_codetable_map.get(codetable_name)

    if allowed_codetable is not None:
        # Check cache
        cached_codetable = codetable_cache.get(codetable_name)

        if cached_codetable is not None:
            print("\n*** CachedcodeTable: " + str(cached_codetable))
            return jsonify(cached_codetable)

        else:
            codetable_data = codetablesService.get_code_table(allowed_codetable)
            data = serializeUtils.serialize_codetable(codetable_data)
            print("codetableData=" + str(data))
            if data:
                codetable_cache.add(codetable_name, data)
                return jsonify(data)

    abort(404)
