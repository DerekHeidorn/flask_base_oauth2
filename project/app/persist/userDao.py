from sqlalchemy import func

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

    return new_user.id


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


def get_user(user_id, session=None):
    """
    Gets the User based on the id parameter

    :param user_id: The id of the user which needs to be loaded
    :param session: existing db session
    :return: The user.
    """
    if session is None:
        session = baseDao.get_session()

    user = session.query(User).filter(User.id == user_id).first()
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

    user = session.query(User).filter(User.username == username).first()
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

    query = session.query(func.count(User.id)).filter(User.username == username)
    if exclude_user_id is not None:
        query.filter(User.id != exclude_user_id)

    count = query.scalar()

    return count == 0


def update_user(user_id, user_to_be_updated):
    updated_user = None
    session = baseDao.get_session()

    user = get_user(user_id, session=session)
    if user is None:
        return updated_user

    user.firstName = user_to_be_updated["firstName"]
    user.lastName = user_to_be_updated["lastName"]
    user.username = user_to_be_updated["username"]

    session.commit()
    updated_user = get_user(user_id)

    return updated_user


def delete_user(user_id):
    id_value = int(user_id)
    if id_value < 0:
        raise ValueError("Parameter [id] should be a positive number!")

    if id_value > 0:
        session = baseDao.get_session()
        items_deleted = session.query(User).filter(User.id == id_value).delete()
        return items_deleted > 0

    return False
