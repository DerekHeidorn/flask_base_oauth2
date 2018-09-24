from sqlalchemy.sql import text
from sqlalchemy.sql import column
from sqlalchemy.sql import select

from persist.baseDao import getSession


def get_code_table(codetable, serialize=False, session=None):

    if(session == None):
        session = getSession()

    all_data = session.query(codetable).order_by(codetable.description).all()

    if serialize:
        return [o.serialize() for o in all_data]
    else:
        return all_data

