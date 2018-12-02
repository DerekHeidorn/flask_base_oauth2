
from app.persist import codetableDao


def get_code_table(code_table_name):

    data = codetableDao.get_code_table(code_table_name)

    return data
