from sqlalchemy import func, update, and_, or_
from datetime import datetime
from project.app.models.user import User, Friendship, FriendshipHistory
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


def get_users_by_ids(user_ids, session=None):

    all_users = session.query(User) \
        .filter(User.user_id.in_(user_ids)) \
        .all()
    return all_users


def get_public_users(session=None):
    """
    Get all users, order by Last Name

    :param session: existing db session
    :return: users.
    """
    if session is None:
        session = baseDao.get_session()

    all_users = session.query(User)\
                                   .filter(and_(User.is_private == False,  # is not private
                                                User.type_cd == 'C',  # 'C' == Customer
                                                User.status_cd == 'A'  # Active User
                                                )) \
                                    .order_by(User.alias) \
                                    .all()

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

    update(User).where(User.user_id == user_id). \
        values(failed_attempt_count=failed_count)

    session.commit()
    updated_user = get_user_by_id(user_id)

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


def add_pending_friendship(user_id, friend_user_id, session=None):
    """
    Creates and saves a new user to the database.

    :param user_id: user's id
    :param friend_user_id: the friend's user id
    :param session: database session

    """
    if session is None:
        session = baseDao.get_session()

    friendship = Friendship()
    friendship.user_id = user_id
    friendship.friend_user_id = friend_user_id
    friendship.status_cd = 'P'
    friendship.from_ts = datetime.now()

    session.add(friendship)
    session.commit()

    return friendship


def add_friendship_history(friendship, session=None):
    """
    Creates and saves a new user to the database.

    :param friendship: friendship to make history record from
    :param session: database session

    """
    if session is None:
        session = baseDao.get_session()

    friendship_history = FriendshipHistory()
    friendship_history.user_id = friendship.user_id
    friendship_history.friend_user_id = friendship.friend_user_id
    friendship_history.status_cd = friendship.status_cd
    friendship_history.from_ts = friendship.from_ts
    friendship_history.to_ts = datetime.now()

    session.add(friendship_history)
    session.commit()

    return friendship_history


def get_friendship_history_by_ids(user_id, friend_user_id, session=None):
    """
    Gets the friendship based on the id parameters

    :param user_id: The id of the user
    :param friend_user_id: The id of the friend
    :param session: existing db session
    :return: The friendship.
    """
    if session is None:
        session = baseDao.get_session()

    friendshipHistory = session.query(FriendshipHistory).filter(FriendshipHistory.user_id == user_id,
                                      FriendshipHistory.friend_user_id == friend_user_id).first()
    return friendshipHistory


def get_friendship_by_ids(user_id, friend_user_id, session=None):
    """
    Gets the friendship based on the id parameters

    :param user_id: The id of the user
    :param friend_user_id: The id of the friend
    :param session: existing db session
    :return: The friendship.
    """
    if session is None:
        session = baseDao.get_session()

    friendship = session.query(Friendship).filter(Friendship.user_id == user_id,
                                                  Friendship.friend_user_id == friend_user_id).first()
    return friendship


def get_friendships_by_user_id(user_id, session=None):
    """
    Gets the friendship based on the id parameters

    :param user_id: The id of the user
    :param session: existing db session
    :return: The friendship.
    """
    if session is None:
        session = baseDao.get_session()

    friendships = session.query(Friendship) \
                         .filter(or_(Friendship.user_id == user_id,
                                     Friendship.friend_user_id == user_id
                                     )
                                 ) \
                         .all()

    return friendships


def update_friendship_to_accepted(user_id, friend_user_id, session=None):
    if session is None:
        session = baseDao.get_session()

    friendship = get_friendship_by_ids(user_id, friend_user_id, session)

    if friendship is not None:
        friendship.status_cd = 'A'
        session.commit()
        return friendship

    return


def remove_pending_friendship(user_id, friend_user_id, session=None):
    if session is None:
        session = baseDao.get_session()

    session.query(Friendship).filter(Friendship.user_id == user_id,
                                     Friendship.friend_user_id == friend_user_id,
                                     Friendship.status_cd == 'P').delete()


def remove_accepted_friendship(user_id, friend_user_id, session=None):
    if session is None:
        session = baseDao.get_session()

    friendship = get_friendship_by_ids(user_id, friend_user_id, session)

    if friendship is not None:
        add_friendship_history(friendship, session)
        session.query(Friendship).filter(Friendship.user_id == user_id,
                                         Friendship.friend_user_id == friend_user_id,
                                         Friendship.status_cd == 'A').delete()
