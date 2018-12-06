
from app.persist import codetableDao, baseDao


def get_code_table(code_table_name):
    session = baseDao.get_session()
    data = codetableDao.get_code_table(session, code_table_name)

    return data
