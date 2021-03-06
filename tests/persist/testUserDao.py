import uuid
from datetime import datetime
from tests.persist.baseTest import BaseTest
from tests.helpers import commonHelper
from tests.utils import randomUtil
from app.persist import userDao, baseDao
from app.models.user import User


class UserDaoTestCase(BaseTest):

    def test_get_user_by_username(self):
        session = baseDao.get_session()

        print("running test_get_user_by_username...")
        created_user = commonHelper.create_public_user()

        user = userDao.get_user_by_username(session, created_user.username)
        self.assertEquals(created_user.username, user.username)

    def test_add_user(self):
        session = baseDao.get_session()

        new_user = User()
        new_user.alias = randomUtil.random_string(8, 30)
        new_user.first_name = randomUtil.random_string(6, 6)
        new_user.last_name = randomUtil.random_string(10, 10)
        new_user.username = randomUtil.random_username()
        new_user.user_uuid = uuid.uuid4()
        new_user.status_cd = 'A'
        new_user.type_cd = '1'
        new_user.is_private = False
        new_user.failed_attempt_count = 0
        new_user.created_ts = datetime.now()
        new_user.last_attempts_ts = datetime.now()
        new_user.private_key = randomUtil.random_string(32, 32)
        new_user.password_salt = randomUtil.random_string(32, 32)
        new_user.password_hash = randomUtil.random_string(32, 32)  # Fake Hash

        user_id = userDao.add_user(session, new_user)
        self.assertTrue(user_id > 0)

    def test_add_friendship(self):
        session = baseDao.get_session()

        print("running test_add_friendship...")
        created_user_1 = commonHelper.create_public_user()
        created_user_2 = commonHelper.create_public_user()

        friendship = userDao.add_pending_friendship(session, created_user_1.user_id, created_user_2.user_id)
        print("friendship=" + str(friendship))
        self.assertEqual(friendship.user_id, created_user_1.user_id)
        self.assertEqual(friendship.friend_user_id, created_user_2.user_id)

    def test_friendship_history(self):
        session = baseDao.get_session()

        print("running test_add_friendship...")
        created_user_1 = commonHelper.create_public_user()
        created_user_2 = commonHelper.create_public_user()

        friendship = userDao.add_pending_friendship(session, created_user_1.user_id, created_user_2.user_id)
        print("friendship=" + str(friendship))
        self.assertEqual(friendship.user_id, created_user_1.user_id)
        self.assertEqual(friendship.friend_user_id, created_user_2.user_id)

        userDao.update_friendship_to_accepted(session, created_user_1.user_id, created_user_2.user_id)

        userDao.remove_accepted_friendship(session, created_user_1.user_id, created_user_2.user_id)

        friendship_history = userDao.get_friendship_history_by_ids(session, created_user_1.user_id, created_user_2.user_id)

        print("friendship_history=" + str(friendship_history))

        self.assertEqual(friendship_history.user_id, created_user_1.user_id)
        self.assertEqual(friendship_history.friend_user_id, created_user_2.user_id)
        self.assertEqual(friendship_history.status_cd, 'A')
        self.assertTrue(friendship_history.to_ts is not None)

        friendship = userDao.get_friendship_by_ids(session, friendship_history.user_id, created_user_1.user_id)
        self.assertTrue(friendship is None)
