
from flask import Blueprint
from flask import jsonify
from flask import abort
from cacheout import Cache

from project.app.models.codetables.users import CtUserStatus, CtUserType
from project.app.services import codetablesService
from project.app.web.utils import serializeUtils
from project.app.web.schemas.generalSchema import CodeTableSchema

api = Blueprint('codetables_api', __name__)

allowable_codetable_map = {"CtUserStatus": CtUserStatus, "CtUserType": CtUserType}

_codetable_cache = Cache(maxsize=200, ttl=5 * 60)


@api.route('/api/v1.0/admin/codetables/<codetableName>', methods=['GET'])
def codetable_by_name(codetable_name):

    allowed_codetable = allowable_codetable_map.get(codetable_name)

    if allowed_codetable is not None:
        # Check cache
        cached_codetable = _codetable_cache.get(codetable_name)

        if cached_codetable is not None:
            print("\n*** CachedcodeTable: " + str(cached_codetable))
            return jsonify(cached_codetable)

        else:
            codetable_data = codetablesService.get_code_table(allowed_codetable)
            data = CodeTableSchema.dump(codetable_data, many=True)
            print("codetableData=" + str(data))
            if data:
                _codetable_cache.add(codetable_name, data)
                resp = serializeUtils.generate_response_wrapper(data)
                return jsonify(resp)

    abort(404)
