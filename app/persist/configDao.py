
from app.models.common import Config


def get_config_by_key(session, key):

    config_item = session.query(Config).filter(Config.key == key).first()
    return config_item


def get_config_all(session):

    config_items = session.query(Config).all()
    return config_items
