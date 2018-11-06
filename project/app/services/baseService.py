from flask import Blueprint


class BaseService:
    api = Blueprint('api', __name__)