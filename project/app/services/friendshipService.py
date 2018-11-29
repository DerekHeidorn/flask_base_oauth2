import uuid
import time
import hashlib
from project.app.models.user import User
from project.app.persist import baseDao, userDao, securityDao, oauth2Dao
from project.app.services import emailService, encryptionService, commonService
from project.app.services.utils import userUtils


def remove_pending_friendship(user_id, friend_user_id):
    userDao.remove_pending_friendship(user_id, friend_user_id)


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
