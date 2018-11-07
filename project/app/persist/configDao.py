
from project.app.persist import baseDao
from project.app.models.common import Config


def get_config_by_key(key, session=None):

    if session is None:
        session = baseDao.get_session()

    configItem = session.query(Config).filter(Config.key == key).first()
    return configItem


def get_config_all(session=None):

    if session is None:
        session = baseDao.get_session()

    config_items = session.query(Config).all()
    return config_items