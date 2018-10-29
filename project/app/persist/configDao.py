from sqlalchemy.sql import text
from sqlalchemy.sql import column
from sqlalchemy.sql import select

from project.app.persist.baseDao import getSession
from project.app.models.common import Config


def getConfigByKey(key, session=None):

    if(session == None):
        session = getSession()

    configItem = session.query(Config).filter(Config.key == key).first()
    return configItem

def getConfigAll(session=None):

    if(session == None):
        session = getSession()

    configItems = session.query(Config).all()
    return configItems    