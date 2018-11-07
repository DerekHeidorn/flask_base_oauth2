from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.app.persist.dbConfig import config

initializing_db_string = config["DB_CONNECTION_URI"]
engine_debug = config["DB_ENGINE_DEBUG"]
engine_echo = False
if engine_debug:
    engine_echo = "debug"


if not initializing_db_string:
    raise ValueError('The values specified in engine parameter has to be supported by SQLAlchemy')

print("Starting up sqlalchemy for database...")

# configure Session class with desired options
Session = sessionmaker()

# later, we create the engine
engine = create_engine(initializing_db_string, echo=engine_echo)

# associate it with our custom Session class
Session.configure(bind=engine)
print("finshed setting up sqlalchemy for database...")







