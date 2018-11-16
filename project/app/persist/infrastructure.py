from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.app import main

Session = sessionmaker()


def database_init():
    initializing_db_string = main.global_config["APP_DB_CONNECTION_URI"]
    engine_debug = main.global_config["APP_DB_ENGINE_DEBUG"]
    engine_echo = False
    if engine_debug.lower() == 'true':
        engine_echo = "debug"

    if not initializing_db_string:
        raise ValueError('The values specified in engine parameter has to be supported by SQLAlchemy')

    print("Starting up sqlalchemy for database...")

    # later, we create the engine
    engine = create_engine(initializing_db_string, echo=engine_echo, pool_size=40, max_overflow=0)

    # associate it with our custom Session class
    Session.configure(bind=engine)
    print("finished setting up sqlalchemy for database...")
