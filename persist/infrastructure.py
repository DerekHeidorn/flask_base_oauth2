from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
from persist.dbConfig import config

initializingDBString = config["DB_CONNECTION_URI"]
engineDebug = config["DB_ENGINE_DEBUG"]
engineEcho = False
if(engineDebug): 
    engineEcho = "debug"


if not initializingDBString:
    raise ValueError('The values specified in engine parameter has to be supported by SQLAlchemy')

db_engine = create_engine(initializingDBString, echo=engineEcho)
db_session_maker = sessionmaker(bind=db_engine)







