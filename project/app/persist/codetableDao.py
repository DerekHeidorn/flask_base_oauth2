
from project.app.persist import baseDao


def get_code_table(codetable, session=None):

    if session is None:
        session = baseDao.get_session()

    all_data = session.query(codetable).order_by(codetable.description).all()

    return all_data
