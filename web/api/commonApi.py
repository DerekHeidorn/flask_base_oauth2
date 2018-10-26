
from flask import Blueprint
from flask import jsonify

from services import commonService
from werkzeug.contrib.cache import SimpleCache

api = Blueprint('common_api', __name__)

@api.route('/api/v1.0/app/version', methods=['GET'])
def getAppVersion():
    version = commonService.getConfigByKey("app.release_number")

    return jsonify({"application.version": version})




