from sqlalchemy.sql import text
from sqlalchemy.sql import column
from sqlalchemy.sql import select

from persist.baseDao import getSession


def getCodeTable(codetable, session=None):

    if(session == None):
        session = getSession()

    all_data = session.query(codetable).order_by(codetable.description).all()

    return all_data

