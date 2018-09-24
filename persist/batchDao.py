from sqlalchemy.sql import text
from sqlalchemy.sql import column
from sqlalchemy.sql import select

from persist.baseDao import getSession
from models.batch import BatchJob


def getConfigById(id, session=None):

    if(session == None):
        session = getSession()

    configItem = session.query(BatchJob).filter(BatchJob.id == id).first()
    return configItem