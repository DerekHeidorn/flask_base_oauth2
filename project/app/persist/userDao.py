from sqlalchemy import func, update

from project.app.models.user import User
from project.app.persist import baseDao


def add_user(new_user, session=None):
    """
    Creates and saves a new user to the database.

    :param new_user: new User record
    :param session: database session

    """
    if session is None:
        session = baseDao.get_session()

    session.add(new_user)
    session.commit()

    return new_user.user_id


def get_users(session=None):
    """
    Get all users, order by Last Name

    :param session: existing db session
    :return: users.
    """
    if session is None:
        session = baseDao.get_session()

    all_users = session.query(User).order_by(User.lastName).all()

    return all_users


def get_user_by_id(user_id, session=None):
    """
    Gets the User based on the id parameter

    :param user_id: The id of the user which needs to be loaded
    :param session: existing db session
    :return: The user.
    """
    if session is None:
        session = baseDao.get_session()

    user = session.query(User).filter(User.user_id == user_id).first()
    return user 


def get_user_by_uuid(user_uuid, session=None):
    """
    Gets the User based on the username parameter

    :param user_uuid: The uuid of the user which needs to be loaded
    :param session: existing db session
    :return: The user.
    """

    if session is None:
        session = baseDao.get_session()

    user = session.query(User).filter(User.user_uuid == user_uuid).first()
    return user


def get_user_by_alias(alias, session=None):
    """
    Gets the User based on the username parameter

    :param alias: The alias of the user
    :param session: existing db session
    :return: The user.
    """

    if session is None:
        session = baseDao.get_session()

    user = session.query(User).filter(func.lower(User.alias) == func.lower(alias)).first()
    return user


def get_user_by_username(username, session=None):
    """
    Gets the User based on the username parameter

    :param username: The username of the user which needs to be loaded
    :param session: existing db session
    :return: The user.
    """

    if session is None:
        session = baseDao.get_session()

    user = session.query(User).filter(func.lower(User.username) == func.lower(username)).first()
    return user


def is_username_unique(username, exclude_user_id=None, session=None):
    """
    Gets the User based on the username parameter

    :param username: The username of the user which needs to be loaded
    :param exclude_user_id: exclude the current user
    :param session: existing db session
    :return: The user.
    """

    if session is None:
        session = baseDao.get_session()

    query = session.query(func.count(User.user_id)).filter(func.lower(User.username) == func.lower(username))
    if exclude_user_id is not None:
        query.filter(User.user_id != exclude_user_id)

    count = query.scalar()

    return count == 0


def is_alias_unique(alias, exclude_user_id=None, session=None):
    """
    Gets the User based on the username parameter

    :param alias: The alias of the user w
    :param exclude_user_id: exclude the current user
    :param session: existing db session
    :return: The user.
    """

    if session is None:
        session = baseDao.get_session()

    query = session.query(func.count(User.user_id)).filter(func.lower(User.alias) == func.lower(alias))
    if exclude_user_id is not None:
        query.filter(User.user_id != exclude_user_id)

    count = query.scalar()

    return count == 0

def update_user_login_access(user_id, failed_count, session):

    stmt = update(User).where(User.user_id == user_id). \
        values(failed_attempt_count=failed_count)

    session.commit()
    updated_user = get_user_by_id(user.user_id)

    return updated_user


def update_user(user, session):
    session.commit()
    updated_user = get_user_by_id(user.user_id)

    return updated_user


def delete_user(user_id):
    id_value = int(user_id)
    if id_value < 0:
        raise ValueError("Parameter [id] should be a positive number!")

    if id_value > 0:
        session = baseDao.get_session()
        items_deleted = session.query(User).filter(User.user_id == id_value).delete()
        return items_deleted > 0

    return False


def get_user_count(session=None):
    if session is None:
        session = baseDao.get_session()
    row_count = session.query(func.count(User.user_id)).scalar()
    return row_count
