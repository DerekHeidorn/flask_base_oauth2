from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.app.persist.dbConfig import config

initializingDBString = config["DB_CONNECTION_URI"]
engineDebug = config["DB_ENGINE_DEBUG"]
engineEcho = False
if(engineDebug): 
    engineEcho = "debug"


if not initializingDBString:
    raise ValueError('The values specified in engine parameter has to be supported by SQLAlchemy')

print("Starting up sqlalchemy for database...")

# configure Session class with desired options
Session = sessionmaker()

# later, we create the engine
engine = create_engine(initializingDBString, echo=engineEcho)

# associate it with our custom Session class
Session.configure(bind=engine)
print("finshed setting up sqlalchemy for database...")







