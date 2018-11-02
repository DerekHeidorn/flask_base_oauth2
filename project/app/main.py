
from flask import Flask
from flask_cors import CORS

from project.app.services import commonService
from project.app.web import oauth2
from project.app.web.api import userApi, codetablesApi, commonApi, authApi
from project.app.web import oauth2Workflow
from authlib.specs.rfc7518.jwk_algorithms import JWK_ALGORITHMS

def createApplication():

    

    print("Creating Application...")
    app = Flask(__name__)
    app.secret_key = "MySuperSecretKey"

    app.config['OAUTH2_JWT_ISS'] = 'https://localhost:9000'
    app.config['OAUTH2_JWT_KEY'] = 'MySuperSecretJwtKey'
    app.config['OAUTH2_JWT_ALG'] = 'HS512'
    app.config['OAUTH2_JWT_EXP'] = 3800

    CORS(app)
    oauth2.init(app)


    #app_settings = os.getenv(
    #    'APP_SETTINGS',
    #    'project.server.config.DevelopmentConfig'
    #)
    #app.config.from_object(app_settings)
    
    commonService.loadApplicationCacheFromDB()

    # -- API registration --
    app.register_blueprint(userApi.api)
    app.register_blueprint(codetablesApi.api)
    app.register_blueprint(commonApi.api)
    app.register_blueprint(authApi.api)
    app.register_blueprint(oauth2Workflow.bp)

    # Information output
    for b in app.blueprints:
        print("Registered blueprints: " + b)

    for u in app.url_map.iter_rules():
        print("url_map: " + str(u) + " " + str(u.endpoint) + " " + str(u.methods))

    return app