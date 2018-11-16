import os
from pytz import utc

from flask import Flask
from flask_cors import CORS

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from project.app.persist import infrastructure
from project.app.services import commonService, schedulerService
from project.app.web import oauth2
from project.app.web.api import commonApi, userApi, codetablesApi
from project.app.web import oauth2Workflow

global_config = {}


def create_application():

    print("Creating Application...")
    app = Flask(__name__)

    required_os_environment_settings = [
        "APP_SECRET_KEY",
        "APP_FLASK_SECRET_KEY",
        "APP_JWT_ISS",
        "APP_JWT_KEY",
        "APP_DB_CONNECTION_URI",
        "APP_DB_ENGINE_DEBUG"
    ]

    for r in required_os_environment_settings:
        if os.environ[r] is None:
            raise Exception('FATAL: Unable to find OS environment settings for : ' + r)

    app.secret_key = os.environ["APP_FLASK_SECRET_KEY"]
    app.config['OAUTH2_JWT_ISS'] = os.environ["APP_JWT_ISS"]
    app.config['OAUTH2_JWT_KEY'] = os.environ["APP_JWT_KEY"]
    app.config['OAUTH2_JWT_ALG'] = 'HS512'
    app.config['OAUTH2_JWT_EXP'] = 3800

    # load keys and DB config globally
    global_config["APP_SECRET_KEY"] = os.environ["APP_SECRET_KEY"]
    global_config["APP_JWT_KEY"] = os.environ["APP_JWT_KEY"]
    global_config["APP_FLASK_SECRET_KEY"] = os.environ["APP_FLASK_SECRET_KEY"]
    global_config["APP_DB_CONNECTION_URI"] = os.environ["APP_DB_CONNECTION_URI"]
    global_config["APP_DB_ENGINE_DEBUG"] = os.environ["APP_DB_ENGINE_DEBUG"]

    infrastructure.database_init()
    CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:4200"}})
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
    app.register_blueprint(userApi.api)
    app.register_blueprint(oauth2Workflow.api)

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
