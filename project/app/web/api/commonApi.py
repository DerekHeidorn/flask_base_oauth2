
from flask import Blueprint
from flask import jsonify
from project.app.services import commonService

api = Blueprint('common_api', __name__)


@api.route('/api/v1.0/app/version', methods=['GET'])
def get_app_version():
    version = commonService.get_config_by_key("app.release_number")

    return jsonify({"application.version": version})
