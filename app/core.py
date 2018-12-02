import os
import logging
from pytz import utc

from flask import current_app, Flask, request
from flask_cors import CORS
from werkzeug.local import LocalProxy
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from project.app.persist import infrastructure
from project.app.services import commonService, schedulerService
from project.app.web import oauth2
from project.app.web import oauth2Workflow
from project.app.web import errorHandlerAdvice
from project.app.web.api import commonApi, privateUserApi, publicUserApi, adminUserApi, codetablesApi, friendshipApi


global_config = {}

# logger object for all views to use
logger = LocalProxy(lambda: current_app.logger)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


def create_application():

    print("Creating Application...")
    app = Flask(__name__)

    # Global Error handlers
    app.register_error_handler(ValidationError, errorHandlerAdvice.handle_validation_error)
    app.register_error_handler(HTTPException, errorHandlerAdvice.handle_http_exception)
    app.register_error_handler(Exception, errorHandlerAdvice.handle_error)

    required_os_environment_settings = [
        "APP_SECRET_KEY",
        "APP_FLASK_SECRET_KEY",
        "APP_JWT_ISS",
        "APP_JWT_KEY",
        "APP_DB_CONNECTION_URI",
        "APP_DB_ENGINE_DEBUG",
        "APP_MODE",
        "APP_SHARED_SECRET_KEY"
    ]

    for r in required_os_environment_settings:
        if os.environ[r] is None:
            raise Exception('FATAL: Unable to find OS environment settings for : ' + r)

    app.secret_key = os.environ["APP_FLASK_SECRET_KEY"]
    app.config['OAUTH2_JWT_ISS'] = os.environ["APP_JWT_ISS"]
    app.config['OAUTH2_JWT_KEY'] = os.environ["APP_JWT_KEY"]
    app.config['OAUTH2_JWT_ALG'] = 'HS512'
    app.config['OAUTH2_JWT_EXP'] = 3800
    app.config['APP_LOG_FILE'] = 'app.log'

    # load keys and DB config globally
    global_config["APP_MODE"] = os.environ["APP_MODE"]
    global_config["APP_SECRET_KEY"] = os.environ["APP_SECRET_KEY"]
    global_config["APP_SHARED_SECRET_KEY"] = os.environ["APP_SHARED_SECRET_KEY"]
    global_config["APP_JWT_KEY"] = os.environ["APP_JWT_KEY"]
    global_config["APP_FLASK_SECRET_KEY"] = os.environ["APP_FLASK_SECRET_KEY"]
    global_config["APP_DB_CONNECTION_URI"] = os.environ["APP_DB_CONNECTION_URI"]
    global_config["APP_DB_ENGINE_DEBUG"] = os.environ["APP_DB_ENGINE_DEBUG"]

    # -- logging --
    formatter = RequestFormatter(
        "%(asctime)s %(remote_addr)s: requested %(url)s: %(levelname)s in [%(module)s: %(lineno)d]: %(message)s"
    )

    if app.config.get("APP_LOG_FILE"):
        fh = logging.FileHandler(app.config.get("APP_LOG_FILE"))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        app.logger.addHandler(fh)

    logging_stream = logging.StreamHandler()
    logging_stream.setLevel(logging.DEBUG)
    logging_stream.setFormatter(formatter)

    app.logger.addHandler(logging_stream)
    app.logger.setLevel(logging.DEBUG)

    # setup database
    infrastructure.database_init()

    CORS(app,
         # resources={r"/api/*": {"origins": "http://127.0.0.1:4200"}},
         allow_headers=["origin", "X-Requested-With", "Content-Type", "Accept", "Accept-Encoding",
                        "Accept-Language", "Content-Language", "Authorization", "If-Modified-Since"],
         expose_headers=["Content-Disposition"],
         methods=["OPTIONS", "POST", "PUT", "GET", "DELETE"],
         origins=["http://127.0.0.1:4200", "http://localhost:4200", "http://127.0.0.1:9000", "http://127.0.0.1:9001"],
         max_age=1800)
    # CORS(app, resources=r"/api/*")
    # CORS(app)
    oauth2.init(app)

    # app_settings = os.getenv(
    #    'APP_SETTINGS',
    #    'project.server.config.DevelopmentConfig'
    # )
    # app.config.from_object(app_settings)
    
    commonService.load_application_cache_from_db()

    # scheduler initialization
    scheduler = _initialize_scheduler()
    scheduler.start()

    # -- API registration --
    app.register_blueprint(commonApi.api)
    app.register_blueprint(codetablesApi.api)
    app.register_blueprint(privateUserApi.api)
    app.register_blueprint(publicUserApi.api)
    app.register_blueprint(adminUserApi.api)
    app.register_blueprint(oauth2Workflow.api)
    app.register_blueprint(friendshipApi.api)

    # Information output
    for b in app.blueprints:
        print("Registered blueprints: " + b)

    for u in app.url_map.iter_rules():
        print("url_map: " + str(u) + " " + str(u.endpoint) + " " + str(u.methods))

    return app


def _initialize_scheduler():
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }

    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults,
                                    timezone=utc)

    scheduler.add_job(schedulerService.run_stats, 'interval', minutes=2)

    scheduler.print_jobs()

    return scheduler
