from sqlalchemy import func, update, and_, or_
from datetime import datetime
from app.models.user import User, Friendship, FriendshipHistory
from app.persist import baseDao


def add_user(session, new_user):
    """
    Creates and saves a new user to the database.

    :param new_user: new User record
    :param session: database session

    """
    session.add(new_user)
    session.commit()

    return new_user.user_id


def get_users(session):
    """
    Get all users, order by Last Name

    :param session: existing db session
    :return: users.
    """
    all_users = session.query(User).order_by(User.lastName).all()

    return all_users


def get_users_by_ids(session, user_ids):

    all_users = session.query(User) \
        .filter(User.user_id.in_(user_ids)) \
        .all()
    return all_users


def get_public_users(session):
    """
    Get all users, order by Last Name

    :param session: existing db session
    :return: users.
    """
    all_users = session.query(User) \
        .filter(and_(User.is_private == False,  # is not private
                     User.type_cd == 'C',  # 'C' == Customer
                     User.status_cd == 'A'  # Active User
                     )) \
        .order_by(User.alias) \
        .all()

    return all_users


def get_user_by_id(session, user_id):
    """
    Gets the User based on the id parameter

    :param user_id: The id of the user which needs to be loaded
    :param session: existing db session
    :return: The user.
    """
    user = session.query(User).filter(User.user_id == user_id).first()
    return user


def get_user_by_uuid(session, user_uuid):
    """
    Gets the User based on the username parameter

    :param user_uuid: The uuid of the user which needs to be loaded
    :param session: existing db session
    :return: The user.
    """
    user = session.query(User).filter(User.user_uuid == user_uuid).first()
    return user


def get_user_by_alias(session, alias):
    """
    Gets the User based on the username parameter

    :param alias: The alias of the user
    :param session: existing db session
    :return: The user.
    """
    user = session.query(User).filter(func.lower(User.alias) == func.lower(alias)).first()
    return user


def get_user_by_username(session, username):
    """
    Gets the User based on the username parameter

    :param username: The username of the user which needs to be loaded
    :param session: existing db session
    :return: The user.
    """
    user = session.query(User).filter(func.lower(User.username) == func.lower(username)).first()
    return user


def is_username_unique(session, username, exclude_user_id=None):
    """
    Gets the User based on the username parameter

    :param username: The username of the user which needs to be loaded
    :param exclude_user_id: exclude the current user
    :param session: existing db session
    :return: The user.
    """
    # TODO
    query = session.query(func.count(User.user_id)).filter(func.lower(User.username) == func.lower(username))
    if exclude_user_id is not None:
        query.filter(User.user_id != exclude_user_id)

    count = query.scalar()

    return count == 0


def is_alias_unique(session, alias, exclude_user_id=None):
    """
    Gets the User based on the username parameter

    :param alias: The alias of the user w
    :param exclude_user_id: exclude the current user
    :param session: existing db session
    :return: The user.
    """
    query = session.query(func.count(User.user_id)).filter(func.lower(User.alias) == func.lower(alias))
    if exclude_user_id is not None:
        query.filter(User.user_id != exclude_user_id)

    count = query.scalar()

    return count == 0


def update_user_login_access(session, user_id, failed_count):

    update(User).where(User.user_id == user_id). \
        values(failed_attempt_count=failed_count)

    session.commit()
    updated_user = get_user_by_id(session, user_id)

    return updated_user


def update_user(session, user):
    session.commit()
    updated_user = get_user_by_id(session, user.user_id)

    return updated_user


def delete_user(session, user_id):
    id_value = int(user_id)
    if id_value < 0:
        raise ValueError("Parameter [id] should be a positive number!")

    if id_value > 0:
        items_deleted = session.query(User).filter(User.user_id == id_value).delete()
        return items_deleted > 0

    return False


def get_user_count(session):
    row_count = session.query(func.count(User.user_id)).scalar()
    return row_count


def add_pending_friendship(session, user_id, friend_user_id):
    """
    Creates and saves a new user to the database.

    :param user_id: user's id
    :param friend_user_id: the friend's user id
    :param session: database session

    """
    friendship = Friendship()
    friendship.user_id = user_id
    friendship.friend_user_id = friend_user_id
    friendship.status_cd = 'P'
    friendship.from_ts = datetime.now()

    session.add(friendship)
    session.commit()

    return friendship


def add_friendship_history(session, friendship):
    """
    Creates and saves a new user to the database.

    :param friendship: friendship to make history record from
    :param session: database session

    """
    friendship_history = FriendshipHistory()
    friendship_history.user_id = friendship.user_id
    friendship_history.friend_user_id = friendship.friend_user_id
    friendship_history.status_cd = friendship.status_cd
    friendship_history.from_ts = friendship.from_ts
    friendship_history.to_ts = datetime.now()

    session.add(friendship_history)
    session.commit()

    return friendship_history


def get_friendship_history_by_ids(session, user_id, friend_user_id):
    """
    Gets the friendship based on the id parameters

    :param user_id: The id of the user
    :param friend_user_id: The id of the friend
    :param session: existing db session
    :return: The friendship.
    """
    friendship_history = session.query(FriendshipHistory).filter(FriendshipHistory.user_id == user_id,
                                                                 FriendshipHistory.friend_user_id == friend_user_id)\
                                                         .first()
    return friendship_history


def get_friendship_by_ids(session, user_id, friend_user_id):
    """
    Gets the friendship based on the id parameters

    :param user_id: The id of the user
    :param friend_user_id: The id of the friend
    :param session: existing db session
    :return: The friendship.
    """

    friendship = session.query(Friendship).filter(Friendship.user_id == user_id,
                                                  Friendship.friend_user_id == friend_user_id).first()
    return friendship


def get_friendships_by_user_id(session, user_id):
    """
    Gets the friendship based on the id parameters

    :param user_id: The id of the user
    :param session: existing db session
    :return: The friendship.
    """

    friendships = session.query(Friendship) \
                         .filter(or_(Friendship.user_id == user_id,
                                     Friendship.friend_user_id == user_id
                                     )
                                 ) \
                         .all()

    return friendships


def update_friendship_to_accepted(session, user_id, friend_user_id):

    friendship = get_friendship_by_ids(session, user_id, friend_user_id)

    if friendship is not None:
        friendship.status_cd = 'A'
        session.commit()
        return friendship

    return


def remove_pending_friendship(session, user_id, friend_user_id):

    session.query(Friendship).filter(Friendship.user_id == user_id,
                                     Friendship.friend_user_id == friend_user_id,
                                     Friendship.status_cd == 'P').delete()


def remove_accepted_friendship(session, user_id, friend_user_id):

    friendship = get_friendship_by_ids(session, user_id, friend_user_id)

    if friendship is not None:
        add_friendship_history(session, friendship)
        session.query(Friendship).filter(Friendship.user_id == user_id,
                                         Friendship.friend_user_id == friend_user_id,
                                         Friendship.status_cd == 'A').delete()
