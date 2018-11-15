import uuid
from datetime import datetime
from project.tests.persist.baseTest import BaseTest
from project.tests.helpers import commonHelper
from project.tests.utils import randomUtil
from project.app.persist import userDao
from project.app.models.user import User


class UserDaoTestCase(BaseTest):

    def test_get_user_by_username(self):
        print("running test_get_user_by_username...")
        created_user = commonHelper.create_public_user()

        user = userDao.get_user_by_username(created_user.username)
        self.assertEquals(created_user.username, user.username)

    def test_add_user(self):

        new_user = User()
        new_user.first_name = randomUtil.random_string(6, 6)
        new_user.last_name = randomUtil.random_string(10, 10)
        new_user.username = randomUtil.random_username()
        new_user.user_uuid = uuid.uuid4()
        new_user.status_cd = 'A'
        new_user.type_cd = '1'
        new_user.failed_attempt_count = 0
        new_user.last_attempts_ts = datetime.now()
        new_user.private_key = randomUtil.random_string(32, 32)
        new_user.password_salt = randomUtil.random_string(32, 32)
        new_user.password_hash = randomUtil.random_string(32, 32)  # Fake Hask

        user_id = userDao.add_user(new_user)
        self.assertTrue(user_id > 0)
