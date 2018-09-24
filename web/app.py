
from flask import Flask
from flask_oauthlib.provider import OAuth2Provider


from services import userService
from services import codetablesService
from services import commonService



def createApplication():
    print("Creating Application...")
    app = Flask(__name__)

    commonService.loadApplicationCacheFromDB()

    # -- API registration --
    app.register_blueprint(commonService.api)
    app.register_blueprint(userService.api)
    app.register_blueprint(codetablesService.api)
    OAuth2Provider(app)

    # Information output
    for b in app.blueprints:
        print("Registered blueprints: " + b)

    for u in app.url_map.iter_rules():
        print("url_map: " + str(u) + " " + str(u.endpoint) + " " + str(u.methods))



    return app