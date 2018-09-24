from persist.infrastructure import db_session_maker


def getSession():
    return db_session_maker()