
from app.persist import baseDao, userDao


def add_pending_friendship(user_uuid, friend_user_uuid):
    session = baseDao.get_session()

    user = userDao.get_user_by_uuid(user_uuid, session)
    friend_user = userDao.get_user_by_uuid(friend_user_uuid, session)

    if user is not None and friend_user is not None:
        userDao.add_pending_friendship(user.user_id, friend_user.user_id, session)
        session.commit()

    friends = get_friends_by_user_id(user.user_id)
    return friends


def remove_pending_friendship(user_uuid, friend_user_uuid):
    session = baseDao.get_session()

    user = userDao.get_user_by_uuid(user_uuid, session)
    friend_user = userDao.get_user_by_uuid(friend_user_uuid, session)

    if user is not None and friend_user is not None:
        userDao.remove_pending_friendship(user.user_id, friend_user.user_id, session)
        session.commit()

    friends = get_friends_by_user_id(user.user_id)
    return friends


def remove_accepted_friendship(user_uuid, friend_user_uuid):
    session = baseDao.get_session()

    user = userDao.get_user_by_uuid(user_uuid, session)
    friend_user = userDao.get_user_by_uuid(friend_user_uuid, session)

    if user is not None and friend_user is not None:
        userDao.remove_accepted_friendship(user.user_id, friend_user.user_id, session)
        session.commit()

    friends = get_friends_by_user_id(user.user_id)
    return friends


def get_friends_by_user_id(user_id):
    session = baseDao.get_session()

    friendships = userDao.get_friendships_by_user_id(user_id, session)
    friend_ids = []

    for friendship in friendships:
        if friendship.user_id != user_id:
            friend_ids.append(friendship.user_id)
        if friendship.friend_user_id != user_id:
            friend_ids.append(friendship.friend_user_id)

    if len(friend_ids) > 0:
        return userDao.get_users_by_ids(friend_ids, session)
    else:
        return []
