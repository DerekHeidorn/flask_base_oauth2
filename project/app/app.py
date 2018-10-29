
from flask import Flask
from flask_oauthlib.provider import OAuth2Provider
from flask_cors import CORS

from project.app.services import commonService
from project.app.web.api import userApi, codetablesApi, commonApi, authApi

def createApplication():
    print("Creating Application...")
    app = Flask(__name__)
    CORS(app)

    commonService.loadApplicationCacheFromDB()

    # -- API registration --
    app.register_blueprint(userApi.api)
    app.register_blueprint(codetablesApi.api)
    app.register_blueprint(commonApi.api)
    app.register_blueprint(authApi.api)
    OAuth2Provider(app)

    # Information output
    for b in app.blueprints:
        print("Registered blueprints: " + b)

    for u in app.url_map.iter_rules():
        print("url_map: " + str(u) + " " + str(u.endpoint) + " " + str(u.methods))

    return app