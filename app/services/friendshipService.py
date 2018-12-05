
from app.persist import baseDao, userDao
from app import core


def add_pending_friendship(user_uuid, friend_user_uuid):
    session = baseDao.get_session()

    user = userDao.get_user_by_uuid(user_uuid, session)
    friend_user = userDao.get_user_by_uuid(friend_user_uuid, session)

    if user is not None and friend_user is not None:
        userDao.add_pending_friendship(user.user_id, friend_user.user_id, session)
        session.commit()

    return friend_user


def update_friendship_to_accepted(user_uuid, friend_user_uuid):
    session = baseDao.get_session()

    user = userDao.get_user_by_uuid(user_uuid, session)
    friend_user = userDao.get_user_by_uuid(friend_user_uuid, session)

    if user is not None and friend_user is not None:
        userDao.update_friendship_to_accepted(user.user_id, friend_user.user_id, session)
        session.commit()

    return friend_user


def remove_pending_friendship(user_uuid, friend_user_uuid):
    session = baseDao.get_session()

    user = userDao.get_user_by_uuid(user_uuid, session)
    friend_user = userDao.get_user_by_uuid(friend_user_uuid, session)

    if user is not None and friend_user is not None:
        userDao.remove_pending_friendship(user.user_id, friend_user.user_id, session)
        session.commit()

    return friend_user


def remove_accepted_friendship(user_uuid, friend_user_uuid):
    session = baseDao.get_session()

    user = userDao.get_user_by_uuid(user_uuid, session)
    friend_user = userDao.get_user_by_uuid(friend_user_uuid, session)

    if user is not None and friend_user is not None:
        userDao.remove_accepted_friendship(user.user_id, friend_user.user_id, session)
        session.commit()

    return friend_user


def get_friendships_by_user_id(user_id):
    return userDao.get_friendships_by_user_id(user_id)


def get_friends_by_user_id(user_id):
    session = baseDao.get_session()

    friendships = userDao.get_friendships_by_user_id(user_id, session)
    pending_friend_request_ids = []
    pending_friend_ids = []
    accepted_friend_ids = []

    for friendship in friendships:
        if friendship.status_cd == 'P':  # Pending friend request
            if friendship.user_id == user_id:  # user initiated request
                pending_friend_request_ids.append(friendship.friend_user_id)
            elif friendship.friend_user_id == user_id:  # user needs to accept these users to be friends
                pending_friend_ids.append(friendship.user_id)

        elif friendship.status_cd == 'A':

            if friendship.user_id != user_id:
                accepted_friend_ids.append(friendship.user_id)
            elif friendship.friend_user_id != user_id:
                accepted_friend_ids.append(friendship.friend_user_id)

    core.logger.debug("pending_friend_request_ids=" + str(pending_friend_request_ids))
    core.logger.debug("pending_friend_ids=" + str(pending_friend_ids))
    core.logger.debug("accepted_friend_ids=" + str(accepted_friend_ids))

    pending_friend_requests = list()
    pending_friends = list()
    accepted_friends = list()

    if len(pending_friend_request_ids) > 0:
        pending_user_requests = userDao.get_users_by_ids(pending_friend_request_ids, session)
        for u in pending_user_requests:
            pending_friend_requests.append(u)

    if len(pending_friend_ids) > 0:
        pending_users = userDao.get_users_by_ids(pending_friend_ids, session)
        for u in pending_users:
            pending_friends.append(u)

    if len(accepted_friend_ids) > 0:
        accepted_users = userDao.get_users_by_ids(accepted_friend_ids, session)
        for u in accepted_users:
            accepted_friends.append(u)

    return {"pending_friend_requests": pending_friend_requests,
            "pending_friends": pending_friends,
            "accepted_friends": accepted_friends}
